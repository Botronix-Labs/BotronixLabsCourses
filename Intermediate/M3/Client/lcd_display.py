from machine import Pin, SPI, PWM
import framebuf
import time

class LCDDisplay(framebuf.FrameBuffer):
    def __init__(self, bl_pin=13, dc_pin=8, rst_pin=12, mosi_pin=11, sck_pin=10, cs_pin=9):
        self.width = 240
        self.height = 240

        # Backlight
        self.bl = PWM(Pin(bl_pin))
        self.bl.freq(1000)
        self.bl.duty_u16(32768)

        # SPI Pins
        self.cs = Pin(cs_pin, Pin.OUT)
        self.dc = Pin(dc_pin, Pin.OUT)
        self.rst = Pin(rst_pin, Pin.OUT)

        # SPI setup
        self.spi = SPI(1, baudrate=100_000_000, polarity=0, phase=0,
                       sck=Pin(sck_pin), mosi=Pin(mosi_pin), miso=None)

        # Frame buffer
        self.buffer = bytearray(self.width * self.height * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)

        # Color shortcuts (BGR format)
        self.red   = 0x07E0
        self.green = 0x001F
        self.blue  = 0xF800
        self.white = 0xFFFF
        self.black = 0x0000

        # Initialize
        self._init_display()
        self.fill(self.white)
        self.show()

    def _write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def _write_data(self, data):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([data]))
        self.cs(1)

    def _init_display(self):
        self.rst(1)
        self.rst(0)
        time.sleep_ms(50)
        self.rst(1)
        time.sleep_ms(50)

        self._write_cmd(0x36)
        self._write_data(0x70)

        self._write_cmd(0x3A)
        self._write_data(0x05)

        for cmd, data in [
            (0xB2, [0x0C, 0x0C, 0x00, 0x33, 0x33]),
            (0xB7, [0x35]),
            (0xBB, [0x19]),
            (0xC0, [0x2C]),
            (0xC2, [0x01]),
            (0xC3, [0x12]),
            (0xC4, [0x20]),
            (0xC6, [0x0F]),
            (0xD0, [0xA4, 0xA1])
        ]:
            self._write_cmd(cmd)
            for d in data:
                self._write_data(d)

        # Gamma correction
        self._write_cmd(0xE0)
        for val in [0xD0, 0x04, 0x0D, 0x11, 0x13, 0x2B, 0x3F,
                    0x54, 0x4C, 0x18, 0x0D, 0x0B, 0x1F, 0x23]:
            self._write_data(val)

        self._write_cmd(0xE1)
        for val in [0xD0, 0x04, 0x0C, 0x11, 0x13, 0x2C, 0x3F,
                    0x44, 0x51, 0x2F, 0x1F, 0x1F, 0x20, 0x23]:
            self._write_data(val)

        self._write_cmd(0x21)  # Invert
        self._write_cmd(0x11)  # Sleep out
        time.sleep_ms(120)
        self._write_cmd(0x29)  # Display on

    def show(self):
        self._write_cmd(0x2A)  # X address
        self._write_data(0x00)
        self._write_data(0x00)
        self._write_data(0x00)
        self._write_data(0xEF)

        self._write_cmd(0x2B)  # Y address
        self._write_data(0x00)
        self._write_data(0x00)
        self._write_data(0x00)
        self._write_data(0xEF)

        self._write_cmd(0x2C)  # Write RAM
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
