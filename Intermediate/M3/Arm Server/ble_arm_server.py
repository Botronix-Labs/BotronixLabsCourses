import bluetooth
from ble_advertising import advertising_payload
from micropython import const

# UUIDs for the robot arm BLE service
_UART_SERVICE_UUID = bluetooth.UUID("7E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_RX_CHAR = (bluetooth.UUID("7E400002-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_WRITE)
_UART_TX_CHAR = (bluetooth.UUID("7E400003-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_NOTIFY)
_UART_SERVICE = (_UART_SERVICE_UUID, (_UART_TX_CHAR, _UART_RX_CHAR))

class BLEArmServer:
    def __init__(self, ble, on_rx_callback):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        self._connections = set()
        self._rx_buffer = bytearray()
        self._on_rx = on_rx_callback

        # Register the service
        ((self._tx_handle, self._rx_handle),) = self._ble.gatts_register_services((_UART_SERVICE,))

        # Setup advertisement payload
        self._payload = advertising_payload(name="PicoArm", services=[_UART_SERVICE_UUID])
        self._advertise()

    def _irq(self, event, data):
        if event == 1:  # CONNECT
            conn_handle, _, _ = data
            print(f"â Connected: {conn_handle}")
            self._connections.add(conn_handle)

        elif event == 2:  # DISCONNECT
            conn_handle, _, _ = data
            print(f"ð Disconnected: {conn_handle}")
            self._connections.discard(conn_handle)
            self._advertise()

        elif event == 3:  # WRITE
            conn_handle, attr_handle = data
            if attr_handle == self._rx_handle:
                msg = self._ble.gatts_read(self._rx_handle)
                print(f"ð¨ Received: {msg}")
                if self._on_rx:
                    self._on_rx(msg.decode().strip())

    def send(self, data):
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._tx_handle, data)

    def _advertise(self):
        # Try to decode the advertised name from the payload
        adv_name = "<Unknown>"
        try:
            # BLE type for Complete Local Name is 0x09
            i = 0
            while i < len(self._payload):
                length = self._payload[i]
                type_ = self._payload[i + 1]
                if type_ == 0x09:
                    adv_name = self._payload[i + 2:i + 1 + length].decode("utf-8")
                    break
                i += 1 + length
        except Exception as e:
            print("â ï¸ Failed to parse advertising name:", e)

        print(f"ð¢ Advertising as: {adv_name}")
        self._ble.gap_advertise(500_000, adv_data=self._payload)