from string import digits
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import Core_func as core

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import sympy as sp

class BisectionMethodFrame:

    def __init__(self):
        self.df = pd.DataFrame(
            columns=["k", "a", "b", "c", "f(a)", "f(b)", "f(c)", "interval_length"]
        )

    def add_row(self, n, a, b, c, fa, fb, fc):
        new_row = {
            "n": n,
            "a": a,
            "b": b,
            "c": c,
            "f(a)": fa,
            "f(b)": fb,
            "f(c)": fc,
            "interval_length": b - a
        }

        self.df.loc[len(self.df)] = new_row

    def print(self, digits=6):
        print(self.df.round(digits))
    
def BisectionMethod_pri(f, a, b, eps,digits=6, verbose=True):
    assert isinstance(f, core.Function), "f phải là object của class Function"
    assert a < b, "cần a < b"
    assert eps > 0, "eps phải > 0"
    assert f.is_root_interval(a, b, interval_type="open"), "a,b phải là khoảng cách li nghiệm"

    frame = BisectionMethodFrame()

    n = math.ceil(math.log2((b - a) / eps))

    for i in range(n):
        x = (a + b) / 2
        fa = f.evaluate(a)
        fb = f.evaluate(b)
        fx = f.evaluate(x)

        frame.add_row(i, a, b, x, fa, fb, fx)

        if fx == 0:
            if verbose:
                frame.print()
            return x, frame.df

        elif f.is_opposite_signs(a, x):
            b = x
        else:
            a = x

    root = (a + b) / 2

    if verbose:
        frame.print(digits)

    return root, frame.df

def BisectionMethod_post(f, a, b, eps,digits=6 ,verbose=True):
    assert isinstance(f, core.Function), "f phải là object của class Function"
    assert a < b, "cần a < b"
    assert eps > 0, "eps phải > 0"
    assert f.is_root_interval(a, b, interval_type="open"), "a,b phải là khoảng cách li nghiệm"

    frame = BisectionMethodFrame()
    i = 0

    while True:
        x = (a + b) / 2
        fa = f.evaluate(a)
        fb = f.evaluate(b)
        fx = f.evaluate(x)

        frame.add_row(i, a, b, x, fa, fb, fx)

        if fx == 0:
            if verbose:
                frame.print()
            return x, frame.df

        elif f.is_opposite_signs(a, x):
            b = x
        else:
            a = x

        if abs(b - a) < eps:
            break

        i += 1

    root = (a + b) / 2

    if verbose:
        frame.print(digits)

    return root, frame.df


