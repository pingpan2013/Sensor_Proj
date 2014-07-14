#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import pandas as pd     # used to convert datetime64 to datetime
import csv

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
            print self.data

    def genGraph_(self):
        x = np.array([(1.0, 2, '2012-01-01'), (2.0, 3, '2013-01-01'), (5.0, 5, '2014-01-01')], 
                    dtype=[('mois', float), ('temp', int), ('date', 'datetime64[D]')])
    
        '''test load and sace'''
        np.save('./graph_data/testArray', x)
        t = np.load('./graph_data/testArray.npy').view(np.recarray)
        print t.dtype 

        fig, ax = plt.subplots(1)
        ax.plot(pd.to_datetime(t.date), t.mois)
        ax.plot(pd.to_datetime(t.date), t.temp)
        fig.autofmt_xdate()
        ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
        plt.title('fig.autofmt_xdate fixes the labels')

        plt.show()
    
    def genDtype(self):
        '''Get the data type, always put DATE in the last '''
        for i in xrange(len(self.data[0])):
            if i != len(self.data[0]) - 1:
                self.dtype.append((str(self.data[0][i]), '<f8'))
            else:
                self.dtype.append((self.data[0][i], 'datetime64[D]'))
        
        print "Data Type: " + str(self.dtype)


    def genGraph(self):
        '''Generate the graph according to the data'''
        self.genDtype()
        x = np.array(self.data, dtype=self.dtype) 
        np.save('./graph_data/data', x)
        t = np.load('./graph_data/data.npy').view(np.recarray)
        print t.dtype 



def main():
    filename = 'test.csv'
    dtype=[('mois', float), ('temp', int), ('date', 'datetime64[D]')]
    
    gg = Gen_Graph(filename) 
    gg.readData()
    gg.genGraph()


    print "Done"




if __name__ == "__main__":
    main()



