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
        self.graph.set_ylim(0, 3)
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
    fig.canvas.set_window_title("Water tank state")
    fig.subplots_adjust(hspace=.8)

    ax = fig.add_subplot(2, 1, 1)
    ax.set_title("SCADA State")
    ax.set_ylabel("State")
    ax.set_xlabel("Time")

    ax2 = fig.add_subplot(2, 1, 2)
    ax2.set_title("Tank State")
    ax2.set_ylabel("State")
    ax2.set_xlabel("Time")

    fig2 = plt.figure()
    fig2.canvas.set_window_title("Pump - Valve state")
    fig2.subplots_adjust(hspace=.8)
    
    ax3 = fig2.add_subplot(2,2,1)
    ax3.set_title("Scada Pump")
    ax3.set_ylabel("State")
    ax3.set_xlabel("Time")
    
    ax4 = fig2.add_subplot(2, 2, 2)
    ax4.set_title("Scada Valve")
    ax4.set_xlabel("Time")
    
    ax5 = fig2.add_subplot(2,2,3)
    ax5.set_title("Tank Pump")
    ax5.set_ylabel("State")
    ax5.set_xlabel("Time")
    
    ax6 = fig2.add_subplot(2, 2, 4)
    ax6.set_title("Tank Valve")
    ax6.set_xlabel("Time")
    
    fig3 = plt.figure()
    fig3.canvas.set_window_title("Sensors state")
    fig3.subplots_adjust(hspace=.8)
    
    ax7 = fig3.add_subplot(2,1,1)
    ax7.set_title("Sensor High")
    ax7.set_ylabel("State")
    ax7.set_xlabel("Time")
    
    ax8 = fig3.add_subplot(2, 1, 2)
    ax8.set_title("Sensor Low")
    ax8.set_ylabel("State")
    ax8.set_xlabel("Time")
    
    ax.grid()
    ax2.grid()
    ax3.grid()
    ax4.grid()
    ax5.grid()
    ax6.grid()
    ax7.grid()
    ax8.grid()    

    line, = ax.plot([], [], lw=2)
    line2,  = ax2.plot([], [], lw=2)
    line3,  = ax3.plot([], [], lw=2)
    line4,  = ax4.plot([], [], lw=2)
    line5,  = ax5.plot([], [], lw=2)
    line6,  = ax6.plot([], [], lw=2)
    line7,  = ax7.plot([], [], lw=2)
    line8,  = ax8.plot([], [], lw=2)

    state_plot = DrawPlot('SCADA/state.csv', ax, line, 0)
    r_state_plot = DrawPlot('Tank/real_state.csv', ax2, line2, 0)
    pump_plot = DrawPlot('SCADA/pump.csv', ax3, line3, 0)
    valve_plot = DrawPlot('SCADA/valve.csv', ax4, line4, 0)
    r_pump_plot = DrawPlot('Tank/pump.csv', ax5, line5, 0)
    r_valve_plot = DrawPlot('Tank/valve.csv', ax6,  line6, 0)
    sensor_high = DrawPlot('Tank/sensor.csv', ax7,  line7, 1)
    sensor_low = DrawPlot('Tank/sensor.csv', ax8,  line8, 0)

    ani = animation.FuncAnimation(fig, state_plot.run, state_plot.data_gen, blit=False, interval=1000,repeat=False, init_func=state_plot.init)
    ani2 = animation.FuncAnimation(fig, r_state_plot.run, r_state_plot.data_gen, blit=False, interval=1000,repeat=False, init_func=r_state_plot.init)
    ani3 = animation.FuncAnimation(fig2, pump_plot.run, pump_plot.data_gen, blit=False, interval=1000,repeat=False, init_func=pump_plot.init)
    ani4 = animation.FuncAnimation(fig2, valve_plot.run, valve_plot.data_gen, blit=False, interval=1000,repeat=False, init_func=valve_plot.init)
    ani5 = animation.FuncAnimation(fig2, r_pump_plot.run, r_pump_plot.data_gen, blit=False, interval=1000,repeat=False, init_func=r_pump_plot.init)
    ani6 = animation.FuncAnimation(fig2, r_valve_plot.run, r_valve_plot.data_gen, blit=False, interval=1000,repeat=False, init_func=r_valve_plot.init)
    ani7 = animation.FuncAnimation(fig3, sensor_high.run, sensor_high.data_gen, blit=False, interval=1000,repeat=False, init_func=sensor_high.init)
    ani8 = animation.FuncAnimation(fig3, sensor_low.run, sensor_low.data_gen, blit=False, interval=1000,repeat=False, init_func=sensor_low.init)
    
    plt.show()

if __name__ == "__main__":
    main()
