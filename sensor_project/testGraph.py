#!/usr/bin/python



import matplotlib.pyplot as plt
import numpy as np

def test1():
    a = np.linspace(0, 10, 100)
    b = np.exp(-a)

    plt.plot(a, b)
    plt.show()

def test2():

