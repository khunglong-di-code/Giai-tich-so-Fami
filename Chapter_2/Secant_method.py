from math import *
from sympy import *

# ===================================================================================
# Code cho phương pháp Dây cung
# Input : f(x) trong pt f(x)=0; khoảng cách ly ban đầu (a,b); sai số epsilon
# Output: nghiệm gần đúng và bảng lặp
# ===================================================================================

class daycung_oop:
    def __init__(self, a_0, b_0, eps, expr, digits=10):
        x = symbols("x")
        self.func = sympify(expr)
        self.a_0 = a_0
        self.b_0 = b_0
        self.eps = eps
        self.digits = digits  # số chữ số sau dấu phẩy khi hiển thị

        f = self.func
        self.sym_df = [
            f,
            diff(f, x),
            diff(f, x, 2)
        ]

        self.df = [
            lambdify(x, self.sym_df[0], "math"),
            lambdify(x, self.sym_df[1], "math"),
            lambdify(x, self.sym_df[2], "math"),
        ]

    # Kiểm tra dữ liệu đầu vào
    def __checkInputValidity(self):
        a = self.a_0
        b = self.b_0
        f = self.df[0]

        if a >= b:
            print("Khoảng cách ly không hợp lệ: cần a < b")
            return False

        if f(a) == 0:
            print(f"Phương trình có nghiệm đúng x = {a}")
            return False

        if f(b) == 0:
            print(f"Phương trình có nghiệm đúng x = {b}")
            return False

        if f(a) * f(b) > 0:
            print("Khoảng cách ly không hợp lệ, không tồn tại nghiệm duy nhất trong [a, b]")
            return False

        return True

    def __Daycung(self):
        eps = self.eps
        a = self.a_0
        b = self.b_0
        digits = self.digits

        f = self.df[0]
        f1 = self.df[1]
        f2 = self.df[2]

        # Chọn mút cố định đúng theo tiêu chuẩn dây cung:
        # nếu f(a) * f''(a) > 0 thì giữ a cố định, ngược lại giữ b cố định
        if f(a) * f2(a) > 0:
            d = a
            x = b
        else:
            d = b
            x = a

        # Tính xi
        Min = min(abs(f1(a)), abs(f1(b)))
        Max = max(abs(f1(a)), abs(f1(b)))

        if Min == 0:
            xi = 1
        else:
            xi = (Max - Min) / Min

        # format động theo digits
        x_fmt = f"{{:<10}}{{:<22.{digits}f}}{{:<22}}"
        err_fmt = f"{{:<10}}{{:<22.{digits}f}}{{:<22.{digits}f}}"

        print("{:<10}{:<22}{:<22}".format("Lần lặp", "x", "|x - x_old| * xi"))

        lan_lap = 0
        print(x_fmt.format(lan_lap, x, "---"))

        while True:
            lan_lap += 1
            x_old = x
            x = x_old - (d - x_old) / (f(d) - f(x_old)) * f(x_old)
            sai_so = abs(x - x_old) * xi

            print(err_fmt.format(lan_lap, x, sai_so))

            if sai_so <= eps:
                return x

    def Solve(self):
        if not self.__checkInputValidity():
            return None
        return self.__Daycung()


# ===================================================================================
# Chương trình chính

expr = "2**x - 5*x + sin(x)"
a = -2.2
b = -2.15
eps = 0.0005
digits = 6   # tùy chọn số chữ số sau dấu phẩy

solver = daycung_oop(a, b, eps, expr, digits)
nghiem = solver.Solve()

if nghiem is not None:
    print(f"\nNghiệm gần đúng là: {nghiem:.{digits}f}")