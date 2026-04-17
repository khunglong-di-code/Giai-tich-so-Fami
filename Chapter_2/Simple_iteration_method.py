from math import *
from sympy import *
import numpy as np
import pandas as pd

class Simple_iter_class:
    def __init__ (self, expr1, expr2, a, b, eps, x0):

        self.x = symbols("x")

        self.expr1 = sympify(expr1)
        self.expr2 = sympify(expr2)
        self.f = lambdify(self.x, self.expr1, "numpy")
        self.g = lambdify(self.x, self.expr2, "numpy")
        self.a = a
        self.b = b
        self.eps = eps
        self.x0 = x0

        self.expr2_df = diff(self.expr2, self.x)
        self.g1 = lambdify(self.x, self.expr2_df, "numpy")
 
        self.rows = [] # Kết quả các lần lặp
        self.df = None
# ----------------------------------------------------------------------
# Tính q = max |g'(x)| trên [a,b]
# ----------------------------------------------------------------------
    def __get_q_numeric(self, a, b, N=10000):
        xs = np.linspace(a, b, N + 1)

        try:
            vals = np.array(np.abs(self.g1(xs)), dtype=float)
        except Exception:
            return None

        if np.any(np.isnan(vals)) or np.any(np.isinf(vals)):
            return None

        return float(np.max(vals))
    
# ----------------------------------------------------------------------
# Kiểm tra g([a,b]) có nằm trong [a,b] không
# ----------------------------------------------------------------------
    def __check_mapping(self, a, b, N=2000):
        xs = np.linspace(a, b, N + 1)

        try:
            vals = np.array(self.g(xs), dtype=float)
        except Exception:
            return None

        if np.any(np.isnan(vals)) or np.any(np.isinf(vals)):
            return None

        if np.all(vals >= a) and np.all(vals <= b):
            return True

        return False

# ----------------------------------------------------------------------
# Kiểm tra điều kiện đầu vào
# ----------------------------------------------------------------------
    def __check(self, a, b, x0):

        f = self.f

        if f(a) == 0:
            print(f"Phương trình có nghiệm đúng x = {a}")
            return a

        if f(b) == 0:
            print(f"Phương trình có nghiệm đúng x = {b}")
            return b

        if f(a) * f(b) >= 0:
            print("Khoảng cách ly không hợp lệ: f(a)*f(b) >= 0")
            return None

        if x0 < a or x0 > b:
            print("Điểm khởi tạo x0 phải nằm trong khoảng [a, b]")
            return None

        mapping_ok = self.__check_mapping(a, b)
        if mapping_ok is None:
            print("Không kiểm tra được điều kiện g(x) thuộc [a,b] trên [a,b]")
            return None
        if mapping_ok is False:
            print("Hàm g(x) không ánh xạ [a,b] vào [a,b]")
            return None

        q = self.__get_q_numeric(a, b)
        if q is None:
            print("Không tính được q = max |g'(x)| trên [a,b]")
            return None

        if not (0 < q < 1):
            print(f"Hàm g(x) không thỏa điều kiện co vì q = {q:.10f} không thuộc (0,1)")
            return None

        return q

# ----------------------------------------------------------------------
# In thông tin bài toán
# ----------------------------------------------------------------------

    def show_info(self):
        print("================================ THÔNG TIN BÀI TOÁN ================================")
        print(f"f(x)  = {self.expr1}")
        print(f"g(x)  = {self.expr2}")
        print(f"g'(x) = {self.expr2_df}")
        print(f"Khoảng [a, b] = [{self.a}, {self.b}]")
        print(f"x0 = {self.x0}")
        print(f"epsilon = {self.eps}")

        q = self.__get_q_numeric(self.a, self.b)
        if q is None:
            print("q = Không tính được")
        else:
            print(f"q = max |g'(x)| trên [{self.a}, {self.b}] xấp xỉ = {q:.10f}")

        mapping_ok = self.__check_mapping(self.a, self.b)
        if mapping_ok is True:
            print("Điều kiện ánh xạ: g([a,b]) ⊂ [a,b]")
        elif mapping_ok is False:
            print("Điều kiện ánh xạ: g([a,b]) không nằm trong [a,b]")
        else:
            print("Điều kiện ánh xạ: không kiểm tra được")

        print("====================================================================================")


# ----------------------------------------------------------------------
# Lặp đơn theo công thức sai số tiên nghiệm
# ----------------------------------------------------------------------
    def solve_tien_nghiem(self):
        a = self.a
        b = self.b
        x0 = self.x0
        eps = self.eps
        g = self.g

        self.rows = []
        self.df = None

        check = self.__check(a, b, x0)
        if check is None:
            print("Đầu vào không hợp lệ, không thể giải.")
            return None

        if isinstance(check, (float, int)) and check == a and self.f(a) == 0:
            return check
        if isinstance(check, (float, int)) and check == b and self.f(b) == 0:
            return check

        q = self.__get_q_numeric(a, b)
        x1 = float(g(x0))

        if abs(x1 - x0) < 1e-15:
            n = 1
            self.rows.append({
                "k": 0,
                "x_k": x0,
                "|x_k - x_{k-1}|": 0.0,
                "n": n
            })
            self.df = pd.DataFrame(self.rows)
            print(f"Theo công thức sai số tiên nghiệm, nghiệm gần đúng là x = {x0}")
            print(f"n = {n}")
            return x0

        A = ((1 - q) * eps) / abs(x1 - x0)
        n = ceil(log(A) / log(q))
        if n < 1:
            n = 1

        print("Theo công thức sai số tiên nghiệm--------------------------------------")
        print(f"q = {q:.10f}")
        print(f"epsilon = {eps}")
        print(f"A = ((1-q)*epsilon)/|x1-x0| = {A:.10f}")
        print(f"n = {n}")

        self.rows.append({
            "k": 0,
            "x_k": x0,
            "|x_k - x_{k-1}|": 0.0,
            "n": n
        })

        delta1 = abs(x1 - x0)
        self.rows.append({
            "k": 1,
            "x_k": x1,
            "|x_k - x_{k-1}|": delta1,
            "n": n
        })

        x = x1
        for i in range(2, n + 1):
            x_prev = x
            x = float(g(x))
            delta = abs(x - x_prev)

            self.rows.append({
                "k": i,
                "x_k": x,
                "|x_k - x_{k-1}|": delta,
                "n": n
            })

        self.df = pd.DataFrame(self.rows)
        return x
# ----------------------------------------------------------------------
# Lặp đơn theo công thức sai số hậu nghiệm
# ----------------------------------------------------------------------
    def solve_hau_nghiem(self):
        a = self.a
        b = self.b
        x0 = self.x0
        eps = self.eps
        g = self.g

        self.rows = []
        self.df = None

        check = self.__check(a, b, x0)
        if check is None:
            print("Đầu vào không hợp lệ, không thể giải.")
            return None

        if isinstance(check, (float, int)) and check == a and self.f(a) == 0:
            return check
        if isinstance(check, (float, int)) and check == b and self.f(b) == 0:
            return check

        q = self.__get_q_numeric(a, b)

        eps0 = ((1 - q) / q) * eps

        print("Theo công thức sai số hậu nghiệm--------------------------------------")
        print(f"q = {q:.10f}")
        print(f"epsilon = {eps}")
        print(f"epsilon0 = ((1-q)/q)*epsilon = {eps0:.10f}")

        x_old = x0
        self.rows.append({
            "k": 0,
            "x_k": x_old,
            "|x_k - x_{k-1}|": 0.0,

        })

        k = 1
        while True:
            x_new = float(g(x_old))
            delta = abs(x_new - x_old)

            self.rows.append({
                "k": k,
                "x_k": x_new,
                "|x_k - x_{k-1}|": delta,
            })

            if delta <= eps0:
                self.df = pd.DataFrame(self.rows)
                return x_new

            x_old = x_new
            k += 1
        
""" ===================================================================================

Mẫu chạy chương trình
expr1 = "E**(-x) - x"
expr2 = "E**(-x)"
a = 0.0
b = 1.0
x0 = 0.5
eps = 5e-4

solver = Simple_iter_class(expr1, expr2, a, b, eps, x0)

solver.show_info()

root1 = solver.solve_tien_nghiem()
print("\nKết quả theo tiên nghiệm:", root1)
print(solver.df.round(6))

root2 = solver.solve_hau_nghiem()
print("\nKết quả theo hậu nghiệm:", root2)
print(solver.df.round(6))

=================================================================================== """
expr1 = "E**x - 10*x + 7"
expr2 = "ln(10*x - 7)"
a = 3
b = 4
x0 = 3.5
eps = 5e-8

solver = Simple_iter_class(expr1, expr2, a, b, eps, x0)

solver.show_info()

# root1 = solver.solve_tien_nghiem()
# print("\nKết quả theo tiên nghiệm:", f"{root1:.10f}")
# print(solver.df.round(10))

pd.set_option('display.float_format', '{:.8f}'.format)

root2 = solver.solve_hau_nghiem()
print("\nKết quả theo hậu nghiệm:", f"{root2:.8f}")
print(solver.df.round(8))

