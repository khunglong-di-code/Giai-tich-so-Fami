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



