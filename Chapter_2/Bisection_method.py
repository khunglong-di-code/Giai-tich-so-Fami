import math
from sympy import *
import sys
import pandas as pd

#===================================================================================
#
#   Code cho PP chia đôi. 
#       * Input: f(x) = 0; khoảng cách ly (a, b); sai số epsilon
#       * Output: Nghiệm gần đúng và bảng lặp
#       * Phương pháp: Chia đôi (Bisection)
#       * Sai số: solve_ver1 dùng Hậu nghiệm |x_n - x_{n-1}| ≤ ε (nếu tính sai số tương đối thì bắt buộc phải dùng sai số hậu nghiệm)
#                 solve_ver2 dùng Hậu nghiệm (b - a) ≤ ε (đây là điều kiện chặt hơn và tốt hơn, nên ưu tiên dùng)
#       * Ghi chú: Yêu cầu f(a)*f(b) < 0 để đảm bảo hội tụ
#
#===================================================================================


class Bisection_class:
    def __init__(self, expr, a, b, eps):
        self.expr = sympify(expr)
        self.f = lambdify(symbols("x"), self.expr, "math")
        self.a = a
        self.b = b
        self.eps = eps
        self.rows = [] # Kết quả các lần lặp
        self.df = None
    
    # Method theo Sai số: Hậu nghiệm |x_n - x_{n-1}| ≤ ε (cái này thường không chặt bằng cái thứ 2)
    def solve_ver1(self):
        a = self.a
        b = self.b
        eps = self.eps
        f = self.f
        self.rows = []
        self.df = None

        if f(a) == 0:
            print(f"Phương trình có nghiệm đúng x = {a}")
            return a

        if f(b) == 0:
            print(f"Phương trình có nghiệm đúng x = {b}")
            return b

        if f(a) * f(b) >= 0:
            print("Khoảng cách li nghiệm không hợp lệ")
            return None
        
        x_old = (a + b) / 2
        k = 1

        while True:
            # Tính f(x_old) và xác định dấu của nó cho bảng
            fx_old = f(x_old)

            if fx_old > 0:
                sign_fx = "+"
            elif fx_old < 0:
                sign_fx = "-"
            else:
                sign_fx = "0"

            self.rows.append({
                "k": k,
                "a(k-1)": a,
                "b(k-1)": b,
                "xk": x_old,
                "sgn(f(xk))": sign_fx })

            # phần thuật toán chính (tính sai số tuyệt đối)

            if f(a) * f(x_old) < 0:
                b = x_old
            elif f(a) * f(x_old) > 0:
                a = x_old
            else:
                print(f"Phương trình có nghiệm đúng x = {x_old}")
                return x_old
    
            x_new = (a + b) / 2
            delta = abs(x_new - x_old)

            if delta <= eps:
                self.df = pd.DataFrame(self.rows) 
                return x_new
            
            x_old = x_new        
            k += 1

    # Method theo Sai số: Hậu nghiệm |x_n - x_{n-1}| ≤ ε
    def solve_ver2(self):
        a = self.a
        b = self.b
        eps = self.eps
        f = self.f

        self.rows = []
        self.df = None

        # Kiểm tra đầu vào
        if f(a) == 0:
            return a
        if f(b) == 0:
            return b
        if f(a) * f(b) >= 0:
            print("Khoảng cách ly không hợp lệ")
            return None

        k = 1

        while (b - a) > eps:
            x = (a + b) / 2
            fx = f(x)

            sign_fx = "+" if fx > 0 else "-" if fx < 0 else "0"

            self.rows.append({
                "k": k,
                "a(k)": a,
                "b(k)": b,
                "xk": x,
                "sgn(f(xk))": sign_fx
            })

            if fx == 0:
                return x
            elif f(a) * fx < 0:
                b = x
            else:
                a = x

            k += 1

        x_final = (a + b) / 2
        self.df = pd.DataFrame(self.rows)
        return x_final





""" ===================================================================================

Mẫu chạy chương trình

# Đặt biểu thức
expr = "x**3 - x - 2"

# Đặt khoảng cách ly [a, b]
a = 1
b = 2

# Đặt sai số (0.5 x 10^-3)
eps = 5e-4

# Tạo đối tượng
solver = Bisection_class(expr, a, b, eps)

# Giải phương trình
root = solver.solve()

# In kết quả
print("Nghiệm gần đúng:", root)

# In bảng lặp với làm tròn 6 chữ số sau dấu phẩy
print("\nBảng các lần lặp:")
pd.set_option('display.float_format', '{:.6f}'.format)
print(solver.df.round(6))
# Hằng số e trong sympy là exp(1) hoặc E, nên nếu muốn dùng e trong biểu thức thì phải viết là exp(1) hoặc E, không được viết là e như trong math. Ví dụ: expr = "exp(1)**x - cos(2*x)" hoặc expr = "E**x - cos(2*x)"
 =================================================================================== """

expr = "x**5 - 3*x**3 + 2*x - x + 5"
a = -2
b = -1.8
eps = 5e-4

solver = Bisection_class(expr, a, b, eps)
root = solver.solve_ver2()

print("Nghiệm gần đúng:", root)
print("\nBảng các lần lặp:")

pd.set_option('display.float_format', '{:.3f}'.format)
print(solver.df.round(3))
