import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
import sympy as sp

class BisectionMethod:
    def __init__ (self, func,a,b,tol,n,num, epsilon):
        self.func = func
        self.a = a #cận trái
        self.b = b #cận phải
        self.tol = tol #sai số
        self.n = n #số lần lặp
        self.num = num #số chữ số đáng tin
        self.epsilon = epsilon #sai số cho trước
