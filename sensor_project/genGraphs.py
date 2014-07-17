#!/usr/bin/python

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd     # used to convert datetime64 to datetime
import csv
import sys
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA


class Gen_Graph:
    def __init__(self, _filename):
        self.filename = _filename
        self.data = []
        self.dtype = []

    def readData(self):
        '''Read the data from .csv file'''
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                self.data.append(tuple(row))    
        return self.data

    def genDtype(self):
        '''Get the data type, always put DATE in the last '''
        for i in xrange(len(self.data[0])):
            if i != len(self.data[0]) - 1:
                self.dtype.append((str(self.data[0][i]), '<f8'))
            else:
                self.dtype.append((self.data[0][i], '<M8[s]'))
        
        print "Data Type: " + str(self.dtype)
        print '=============================================================='
	
    def uniqueish_color(self):
        '''Randomly select a color'''
        return plt.cm.gist_ncar(np.random.random())

    def genGraph(self):
        '''Generate the graph with unique y axis'''
        self.genDtype()
        x = np.array(self.data[1:], dtype=self.dtype) 
        np.save('./graph_data/data', x)
        t = np.load('./graph_data/data.npy').view(np.recarray)
        fig, ax = plt.subplots(1)

        '''Drawing multiple lines in one graph'''
        for label in self.data[0]:
            if label != 'Time':
                dtype = t['{0}'.format(label)]
                ax.plot(pd.to_datetime(t.Time), dtype)
        ax.set_xlabel(' date ')
        
        '''Formatting the date'''
        fig.autofmt_xdate()
        ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
        plt.title('Sensor Data Flow')
        
        '''Create the labels for different lines'''
        labels = list(self.data[0][:-1])
        plt.legend(labels, loc='lower left')

        plt.show()

    def genGraph_m(self):
        '''Generate the graph with multiple y axises'''
        self.genDtype()
        x = np.array(self.data[1:], dtype=self.dtype) 
        np.save('./graph_data/data', x)
        t = np.load('./graph_data/data.npy').view(np.recarray)
        fig = plt.figure()
        fig.subplots_adjust(right=0.75)
        ax = fig.add_subplot(111)

        '''Drawing multiple lines with different y axises in one graph'''
        lines = []
        labels = list(self.data[0][:-1])
        
        for num in xrange(len(self.data[0]) - 1):
            label = labels[num]
            if num == 0:
                dtype = t['{0}'.format(label)]
                line1, = ax.plot(pd.to_datetime(t.Time), dtype, color=self.uniqueish_color())
                lines.append(line1)
                ax.set_ylabel(label)
                ax.set_xlabel('Date')
            elif label != 'Time':
                dtype = t['{0}'.format(label)]
                par = ax.twinx()
                line2, = par.plot(pd.to_datetime(t.Time), dtype, color=self.uniqueish_color())
                lines.append(line2)
                par.set_ylabel(label)

        '''Formatting the date'''
        fig.autofmt_xdate()
        ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
        plt.title('Sensor Data Flow')
        
        '''Create the labels for different lines'''
        ax.legend(lines, labels, loc='lower left')
        plt.draw()
        plt.show()

    def test(self):
        # To make things reproducible...
        np.random.seed(1977)
        fig, ax = plt.subplots()
       
        # Twin the x-axis twice to make independent y-axes.
        axes = [ax, ax.twinx(), ax.twinx()]

        # Make some space on the right side for the extra y-axis.
        fig.subplots_adjust(right=0.75)

        # Move the last y-axis spine over to the right by 20% of the width of the axes
        axes[-1].spines['right'].set_position(('axes', 1.2))

        # To make the border of the right-most axis visible, we need to turn the frame
        # on. This hides the other plots, however, so we need to turn its fill off.
        axes[-1].set_frame_on(True)
        axes[-1].patch.set_visible(False)

        # And finally we get to plot things...
        colors = ('Green', 'Red', 'Blue')
        for ax, color in zip(axes, colors):
            data = np.random.random(1) * np.random.random(10)
            ax.plot(data, marker='o', linestyle='none', color=color)
            ax.set_ylabel('%s Thing' % color, color=color)
            ax.tick_params(axis='y', colors=color)
            axes[0].set_xlabel('X-axis')

        plt.show()


def main():
    if len(sys.argv) != 2:
        print "Error with the parameters! Please specify the file path!"
        sys.exit(2)
    filename = sys.argv[1]
    
    gg = Gen_Graph(filename) 
    
    data = gg.readData()
    print "Original Data: "
    for i in data:
        print i
    print '=============================================================='
    
    gg.genGraph_m()

    print "Finished Drawing!"

if __name__ == "__main__":
    main()



