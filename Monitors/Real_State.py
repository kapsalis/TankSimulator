import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv
import time

class DrawPlot:
    def __init__(self, file_name, graph, ln):
        self.file = file_name
        self.xdata, self.ydata = [], []
        self.graph = graph
        self.line = ln
        
    def init(self):
        self.graph.set_ylim(-1, 3)
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
                state = int(row[0])

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
    fig.canvas.set_window_title("Real State")
    ax = fig.add_subplot(2, 1, 1)
    ax.set_title("Water Tank Real State")
    ax.set_xlabel("Time")
    ax.set_ylabel("State")
    ax.grid()

    line, = ax.plot([], [], lw=2)


    state_plot = DrawPlot('Tank/real_state.csv', ax, line)

    ani = animation.FuncAnimation(fig, state_plot.run, state_plot.data_gen, blit=False, interval=1000,repeat=False, init_func=state_plot.init)
    plt.show()

if __name__ == "__main__":
    main()
