# plot_mpu_data.py (run this on your PC)
import serial
import matplotlib.pyplot as plt
from collections import deque

# Update this to your Pico's port (check Thonny or Device Manager)
PORT = 'COM13'
BAUD = 115200

# Create buffers
max_len = 100
pitch_vals = deque([0]*max_len, maxlen=max_len)
roll_vals = deque([0]*max_len, maxlen=max_len)
gx_vals = deque([0]*max_len, maxlen=max_len)

# Set up plot
plt.ion()
fig, ax = plt.subplots()
pitch_line, = ax.plot(pitch_vals, label='Pitch (°)')
roll_line, = ax.plot(roll_vals, label='Roll (°)')
gx_line, = ax.plot(gx_vals, label='Gyro X (°/s)')

ax.set_ylim(-190, 190)
ax.legend()
ax.set_title("MPU-9255 Sensor Data (Real-Time)")
ax.set_ylabel("Angle / Velocity")
ax.set_xlabel("Time")

# Start serial connection
with serial.Serial(PORT, BAUD, timeout=1) as ser:
    while True:
        try:
            line = ser.readline().decode().strip()
            if line:
                parts = line.split(",")
                if len(parts) == 5:
                    pitch, roll, gx, gy, gz = map(float, parts)
                    pitch_vals.append(pitch)
                    roll_vals.append(roll)
                    gx_vals.append(gx)

                    pitch_line.set_ydata(pitch_vals)
                    roll_line.set_ydata(roll_vals)
                    gx_line.set_ydata(gx_vals)

                    pitch_line.set_xdata(range(len(pitch_vals)))
                    roll_line.set_xdata(range(len(roll_vals)))
                    gx_line.set_xdata(range(len(gx_vals)))

                    ax.relim()
                    ax.autoscale_view()
                    plt.pause(0.01)
        except Exception as e:
            print("Error:", e)

