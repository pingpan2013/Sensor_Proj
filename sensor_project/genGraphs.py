#!/usr/bin/python

# Desc: Generate graphs for a given .csv file
#       Used python matplotlib library, get the file path as a parameter from the terminal
# 
# Date: 07/14/2014 
# Version: 1.0

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import pandas as pd     # used to convert datetime64 to datetime
import csv
import sys

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

    def genGraph(self):
        '''Generate the graph according to the data'''
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
        
        '''Formatting the date'''
        fig.autofmt_xdate()
        ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
        plt.title('Sensor Data Flow')
        
        '''Create the labels for different lines'''
        labels = list(self.data[0][:-1])
        plt.legend(labels, loc='lower left')

        plt.show()

def main():
    if len(sys.argv) != 2:
        print "Please specify the file path!"
        sys.exit(2)
    filename = sys.argv[1]
    
    gg = Gen_Graph(filename) 
    
    data = gg.readData()
    print "Original Data: "
    for i in data:
        print i
    print '=============================================================='
    
    gg.genGraph()

    print "Finished Drawing!"

if __name__ == "__main__":
    main()



