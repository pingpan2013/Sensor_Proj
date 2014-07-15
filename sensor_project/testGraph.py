#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import pandas as pd     # used to convert datetime64 to datetime
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA


def test():
    fig, ax1 = plt.subplots()
    t = np.arange(0.01, 10.0, 0.01)
    s1 = np.exp(t)
    ax1.plot(t, s1, 'b-')
    ax1.set_xlabel('time (s)')
    # Make the y-axis label and tick labels match the line color.
    ax1.set_ylabel('exp', color='b')
    for tl in ax1.get_yticklabels():
        tl.set_color('b')

    ax2 = ax1.twinx()
    s2 = np.sin(2*np.pi*t)
    ax2.plot(t, s2, 'r.')
    ax2.set_ylabel('sin', color='r')
    for tl in ax2.get_yticklabels():
        tl.set_color('r')
   
    ax3 = ax1.twinx()
    a = np.linspace(0, 10, 100)
    b = np.exp(-a)
    #ax3.plot(a, b)
    #ax3.set_ylabel('test', color='g')

    plt.show()
    

def test0():
    x = [1, 2, 3, 4, 5]
    y = [1, 2, 3, 4, 5]
    ax1 = plt.subplot(111)
    ax1.plot(x, y)
    plt.show()


def test1():
    a = np.linspace(0, 10, 100)
    b = np.exp(-a)
    plt.plot(a, b)
    plt.show()


def test2():
    np.save('./graph_data/123', np.array([[1, 2, 3], [4, 5, 6]]))
    print np.load('./graph_data/123.npy')


def test3():
    t = np.arange(0, 10, 0.01)
    ax1 = plt.subplot(311)
    ax1.plot(t, np.sin(2*np.pi*t))
    ax2 = plt.subplot(212, sharex=ax1)
    ax2.plot(t, np.sin(4*np.pi*t))
    plt.show()


def test4():
    x = np.linspace(0, 2*np.pi, 400)
    y = np.sin(x**2)

    f, (ax1, ax2) = plt.subplots(2, 1, sharey=True)
    ax1.plot(x, y)
    ax1.set_title("Sharing Y axis")
    ax2.scatter(x, y)
    
    plt.show()


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

def test6():
    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust(right=0.75)

    par1 = host.twinx()
    par2 = host.twinx()

    offset = 60
    new_fixed_axis = par2.get_grid_helper().new_fixed_axis
    par2.axis["right"] = new_fixed_axis(loc="right",
                                        axes=par2,
                                        offset=(offset, 0))

    par2.axis["right"].toggle(all=True)

    host.set_xlim(0, 2)
    host.set_ylim(0, 2)

    host.set_xlabel("Distance")
    host.set_ylabel("Density")
    par1.set_ylabel("Temperature")
    par2.set_ylabel("Velocity")

    p1, = host.plot([0, 1, 2], [0, 1, 2], label="Density")
    p2, = par1.plot([0, 1, 2], [0, 3, 2], label="Temperature")
    p3, = par2.plot([0, 1, 2], [50, 30, 15], label="Velocity")

    par1.set_ylim(0, 4)
    par2.set_ylim(1, 65)

    host.legend()

    host.axis["left"].label.set_color(p1.get_color())
    par1.axis["right"].label.set_color(p2.get_color())
    par2.axis["right"].label.set_color(p3.get_color())

    plt.draw()
    plt.show()

    #plt.savefig("Test")


test6()





