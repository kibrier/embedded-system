# read ECG data using arduino and show live-view of data.
import serial
from matplotlib import pyplot as plt
from matplotlib import animation


arduino = serial.Serial(port='/dev/ttyACM0',baudrate=115200, timeout=1)
Nsamp = 500
fig = plt.figure(figsize=(10, 5))
ax = plt.axes(xlim=(0,Nsamp), ylim=(280, 420))
# ax.get_xaxis().set_visible(False)

plt.title('ECG Real-Time Data')
plt.xlabel('Time [' + str(Nsamp/250) + " second window]")
plt.ylabel('Amplitude')
ax.grid(True)

graph, = ax.plot([], [], 'b')

t = list(range(0, Nsamp))
dat = []

for i in range(0, Nsamp):
    dat.append(0)

def init():
    graph.set_data([], [])
    return graph,

def animate(i):
    global t, dat
    #while arduino.in_waiting() == 0:
    #    pass
    ard_reading = arduino.readline().decode("utf-8")
    print(ard_reading)
    if ard_reading == '!':
        pass
    else:
        dat.append(float(ard_reading))
        dat.pop(0)
        graph.set_data(t, dat)
        return graph,

anim = animation.FuncAnimation(fig, animate, init_func=init, interval=1, blit=True)

plt.show()
