import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import sympy as sp
from sympy.calculus.util import continuous_domain
def create_interval(a, b, interval_type:str = None):
    # Khởi tạo khoảng a,b
    """
    kiểm tra xem hàm có liên tục trên đoạn a,b không
    open - (a,b)
    None - [a,b]
    Lopen - (a,b]
    Ropen - [a,b)
    """
    assert any(t in ['open', None, 'Lopen', 'Ropen'] for t in [interval_type]), "interval_type phải là 'open', None, 'Lopen' hoặc 'Ropen'"

    if interval_type == "open":
        interval = sp.Interval.open(a, b) #(a,b)            
    elif interval_type == None:             
        interval = sp.Interval(a, b) #[a,b]
    elif interval_type == "Ropen":
        interval = sp.Interval.Ropen(a, b) #[a,b)
    elif interval_type == "Lopen":
        interval = sp.Interval.Lopen(a, b) #(a,b]   
    return interval


class Function:
    #Biểu diễn hàm số và các phương thức liên quan
    def __init__ (self, expr_str):
        self.expr_str = expr_str
        self.x = sp.symbols('x')
        self.expr = sp.sympify(expr_str) #chuyển chuỗi biểu thức thành biểu thức sympy
        self.func = sp.lambdify(self.x, self.expr, 'numpy') #chuyển biểu thức sympy thành hàm số có thể tính toán được với numpy

    def evaluate(self, x):
        # Tính giá trị của hàm tại x
        return self.func(x) 
    
    def is_opposite_signs(self, a, b):
        #kiểm tra xem hàm có đổi dấu giữa a và b không
        if self.evaluate(a) * self.evaluate(b) < 0:
            return True
        return False

    def is_continuous(self,a,b,interval_type:str = None):
        #kiểm tra xem hàm có liên tục trên đoạn a,b không
        domain = continuous_domain(self.expr, self.x, sp.S.Reals) #tập liên tục của hàm trên R
        interval = create_interval(a, b, interval_type)
        return interval.is_subset(domain) #kiểm tra xem khoảng có phải là tập con của miền liên tục không   
    
    def is_monotonic(self, a, b, interval_type:str = None):
        #kiểm tra xem hàm có đơn điệu trên đoạn a,b không
        interval = create_interval(a, b, interval_type)
        return sp.is_monotonic(self.expr, interval, self.x)

    def is_root_interval(self, a, b, interval_type:str = None):
        #kiểm tra xem a,b có phải là khoảng cách li nghiệm không
        if self.is_opposite_signs(a, b) and self.is_continuous(a, b, interval_type) and self.is_monotonic(a, b, interval_type):
            return True
        return False
    
    