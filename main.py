import sys
import os

sys.path.append(os.path.dirname(__file__))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import sympy as sp

import Core_func as core
from Chapter_2.Bisection_method import BisectionMethod_pri, BisectionMethod_post

def main():

    f = core.Function("x**3 - x - 2")

    root, df = BisectionMethod_pri(f, 1, 2, 1e-6)

    print("Root:", root)
    print(df)


if __name__ == "__main__":
    main()