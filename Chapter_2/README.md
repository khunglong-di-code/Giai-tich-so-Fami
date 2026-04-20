# Chương 2: Giải gần đúng f(x) = 0, x ∈ R

- f(x) = 0 là hàm phi tuyến.
- n là số lần lặp

** Các dạng của bài toán **
Dạng 1: Cho f(x), n. Tính Xn, ΔXn (δXn).
Dạng 2: Cho f(x), ε. Tính n, Xn thỏa mãn ΔXn < ε (δXn < ε).

** Khoảng cách ly nghiệm **
- Là khoảng cách có duy nhât 1 nghiệm của phương trình.

** Định lý điều kiện đủ **
- f(X) liên tục
- f(x) đơn điệu
- f(x) trái dấu ở hai đầu mút
=> (a,b) là khoảng cách ly nghiệm.

## Chú ý khi nhập hàm với SymPy

Khi sử dụng SymPy để xử lý biểu thức toán học trong code (như `sympify(expr)`), cần chú ý cú pháp để tránh lỗi:

- **Biến**: Sử dụng `x` làm biến chính (định nghĩa bằng `symbols("x")`).
- **Lũy thừa**: Dùng `**` thay vì `^` (ví dụ: `x**2` thay vì `x^2`).
- **Hằng số e**: Dùng `exp(1)` hoặc `E` thay vì `e` (ví dụ: `exp(1)**x` hoặc `E**x`).
- **Hàm toán học**: Sử dụng cú pháp SymPy chuẩn:
  - `sin(x)`, `cos(x)`, `tan(x)`, `cot(x)` (cotan), `log(x)` (log tự nhiên - ln), `exp(x)`, `sqrt(x)`, `pi`, `E`, etc.
  - Ví dụ: `sin(2*x)`, `log(x + 1)`, `exp(-x)`, `cot(x)`.
- **Phân số và biểu thức phức tạp**: Dùng `/` cho chia, `()` để nhóm (ví dụ: `(x**2 - 1)/(x + 1)`).
- **Tránh lỗi phổ biến**:
  - Không dùng `e` (như trong math), vì SymPy không nhận diện.
  - Đảm bảo biểu thức hợp lệ; nếu không, `sympify` sẽ báo lỗi.
 
- **Ví dụ biểu thức hợp lệ**:
  - Đa thức: `"x**3 - x - 2"`
  - Siêu việt: `"exp(1)**x - cos(2*x)"` hoặc `"E**x - cos(2*x)"`
  - Phức tạp: `"sin(x) - x/2"` hoặc `"x - tan(x)"`


## Các phương pháp và file trong Chapter 2

### Phương pháp chia đôi (Bisection_method.py)
- **solve_ver0_tiennghiem()**: Tính trước số lần lặp n dựa trên sai số tiên nghiệm (log2((b-a)/ε)), lặp đúng n lần.
- **solve_ver1_tuyetdoi()**: Dùng sai số hậu nghiệm tuyệt đối |x_n - x_{n-1}| ≤ ε.
- **solve_ver1_tuongdoi()**: Dùng sai số hậu nghiệm tương đối |(x_n - x_{n-1})/x_n| ≤ ε.
- **solve_ver2_tuyetdoi()**: Dừng khi độ rộng khoảng (b - a) ≤ ε.

### Phương pháp dây cung (Secant_method_sieuviet.py)
- **solve_ver1_tuyetdoi()**: Dùng sai số hậu nghiệm |f(x_n)| / m1 ≤ ε (m1 = min |f'(x)| trên [a,b]).
- **solve_ver2_tuyetdoi()**: Dùng sai số hậu nghiệm |(M1 - m1)/m1| * |x_n - x_{n-1}| ≤ ε (M1 = max |f'(x)| trên [a,b]).
- **solve_ver2_tuongdoi()**: Dùng sai số hậu nghiệm tương đối |(x_n - x_{n-1})/x_n| ≤ ε / xi (xi = (M1 - m1)/m1).

### Phương pháp Newton (Newton_method.py)
- **solve_ver1()**: Dùng sai số hậu nghiệm |f(x_n)| / m1 ≤ ε (m1 = min |f'(x)| trên [a,b]).
- **solve_ver2_tuyetdoi()**: Dùng sai số hậu nghiệm (M2 / (2*m1)) * |x_n - x_{n-1}|^2 ≤ ε (M2 = max |f''(x)| trên [a,b]).
- **solve_ver2_tuongdoi()**: Dùng sai số hậu nghiệm tương đối |(x_n - x_{n-1})/x_n| ≤ ε / xi (xi = (M1 - m1)/m1).


### Phương pháp lặp đơn (Fixed_point_iteration.py)
Phương pháp biến đổi f(x) = 0 thành x = g(x), rồi lặp x_{k+1} = g(x_k) cho đến hội tụ. Yêu cầu g(x) là ánh xạ co (q = max |g'(x)| < 1 trên [a,b]) và g([a,b]) ⊂ [a,b].

**Chú ý đầu vào**: Người dùng phải tự tìm và nhập g(x) sao cho thỏa điều kiện co (không phải code tự động biến đổi). Nếu không, phương pháp không hội tụ.

- **solve_tien_nghiem()**: Tính trước số lần lặp n dựa trên sai số tiên nghiệm (q^n / (1-q) * |x1 - x0| ≤ ε), lặp đúng n lần.
- **solve_hau_nghiem()**: Dùng sai số hậu nghiệm (q / (1-q)) * |x_n - x_{n-1}| ≤ ε, lặp cho đến thỏa.

Tất cả phương thức đều trả về nghiệm gần đúng và bảng lặp (DataFrame), với kiểm tra khoảng hợp lệ và xử lý trường hợp đặc biệt.

