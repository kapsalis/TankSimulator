import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv
import time

class DrawPlot:
    def __init__(self, file_name, graph, ln, col):
        self.file = file_name
        self.xdata, self.ydata = [], []
        self.graph = graph
        self.line = ln
        self.col = col
        
    def init(self):
        self.graph.set_ylim(-0.5, 1.5)
        self.graph.set_xlim(0, 60)
        del self.xdata[:]
        del self.ydata[:]
        self.line.set_data(self.xdata, self.ydata)
        return self.line,
    
    def data_gen(self, t=-1):
        state = 0
        while True:
            state_file = open(self.file,'r')
            reader = csv.reader(state_file)

            for row in reader: 
                state = int(row[self.col])

            state_file.close();
            
            t += 1
            yield t, state

    def run(self, data):
        # update the data
        t, y = data
        self.xdata.append(t)
        self.ydata.append(y)
        xmin, xmax = self.graph.get_xlim()

        if t >= xmax:
            self.graph.set_xlim(xmin+30, xmax+30)
            self.graph.figure.canvas.draw()
        self.line.set_data(self.xdata, self.ydata)

        return self.line,

def main():
    fig = plt.figure()
    fig.canvas.set_window_title("Tank")
    fig.subplots_adjust(hspace=.5)

    ax = fig.add_subplot(4, 1, 1)
    ax.set_title("Sensor_High")
    ax.set_ylabel("State")
    ax.grid()

    ax2 = fig.add_subplot(4, 1, 2)
    ax2.set_title("Sensor_Low")
    ax2.grid()

    ax3 = fig.add_subplot(4, 1, 3)
    ax3.set_title("Pump State")
    ax3.set_ylabel("State")
    ax3.grid()

    ax4 = fig.add_subplot(4, 1, 4)
    ax4.set_title("Valve State")
    ax4.set_xlabel("Time")
    ax4.grid()

    line, = ax.plot([], [], lw=2)
    line2,  = ax2.plot([], [], lw=2)
    line3,  = ax3.plot([], [], lw=2)
    line4,  = ax4.plot([], [], lw=2)

    sensor_low_plot = DrawPlot('Tank/sensor.csv', ax, line, 1)
    sensor_high_plot = DrawPlot('Tank/sensor.csv', ax2, line2, 0)
    pump_plot = DrawPlot('Tank/pump.csv', ax3, line3, 0)
    valve_plot = DrawPlot('Tank/valve.csv', ax4, line4, 0)

    ani = animation.FuncAnimation(fig, sensor_low_plot.run, sensor_low_plot.data_gen, blit=False, interval=1000,repeat=False, init_func=sensor_low_plot.init)
    ani2 = animation.FuncAnimation(fig, pump_plot.run, pump_plot.data_gen, blit=False, interval=1000,repeat=False, init_func=pump_plot.init)
    ani3 = animation.FuncAnimation(fig, valve_plot.run, valve_plot.data_gen, blit=False, interval=1000,repeat=False, init_func=valve_plot.init)
    ani4 = animation.FuncAnimation(fig, sensor_high_plot.run, sensor_high_plot.data_gen, blit=False, interval=1000,repeat=False, init_func=sensor_high_plot.init)

    plt.show()

if __name__ == "__main__":
    main()
