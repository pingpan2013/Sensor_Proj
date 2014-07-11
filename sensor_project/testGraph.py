#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import pandas as pd     # used to convert datetime64 to datetime

'''Basic Drawing'''
def test0():
    x = [1, 2, 3, 4, 5]
    y = [1, 2, 3, 4, 5]
    ax1 = plt.subplot(111)
    ax1.plot(x, y)
    plt.show()


'''Simple drawing'''
def test1():
    a = np.linspace(0, 10, 100)
    b = np.exp(-a)
    plt.plot(a, b)
    plt.show()


'''test np.save np.array'''
def test2():
    np.save('./graph_data/123', np.array([[1, 2, 3], [4, 5, 6]]))
    print np.load('./graph_data/123.npy')


'''Test subplot'''
def test3():
    t = np.arange(0, 10, 0.01)
    ax1 = plt.subplot(311)
    ax1.plot(t, np.sin(2*np.pi*t))
    ax2 = plt.subplot(212, sharex=ax1)
    ax2.plot(t, np.sin(4*np.pi*t))
    plt.show()


'''Test subplots'''
def test4():
    x = np.linspace(0, 2*np.pi, 400)
    y = np.sin(x**2)

    f, (ax1, ax2) = plt.subplots(2, 1, sharey=True)
    ax1.plot(x, y)
    ax1.set_title("Sharing Y axis")
    ax2.scatter(x, y)
    
    plt.show()


'''Test date format and recarray'''
def test5():
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

test0()





