#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import pandas as pd     # used to convert datetime64 to datetime
import csv

class Gen_Graph:
    def __init__(self, _filename, _dtype):
        self.filename = _filename
        self.data = []
        self.dType = _dtype

    def readData(self):
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                self.data.append(tuple(row))
            print self.data

    def genGraph_():
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

    def genGraph():
        x = np.array(self.data, dtype=dType) 
        np.save('./graph_data/data', x)
        
        


def main():
    filename = 'test.csv'
    dtype=[('mois', float), ('temp', int), ('date', 'datetime64[D]')]
    
    gg = Gen_Graph(filename, dtype) 
    gg.readData()





if __name__ == "__main__":
    main()



