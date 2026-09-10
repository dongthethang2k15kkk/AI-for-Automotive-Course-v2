# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Đề thi cuối khóa — AI Course v2 (BK-AUTO)
#
# Bấm chạy ô bên dưới để bắt đầu. Bài thi gồm 20 câu trắc nghiệm, nộp xong tự
# chuyển sang bài viết code.


# %%
import os
import sys
import urllib.request

REPO_RAW = "https://raw.githubusercontent.com/dongthethang2k15kkk/AI-for-Automotive-Course-v2/main"

os.makedirs("tests", exist_ok=True)
open(os.path.join("tests", "__init__.py"), "w").close()
for ten_file in ("runner.py", "test_final.py", "de_thi_cau_hoi.py", "giao_dien_thi.py"):
    urllib.request.urlretrieve(f"{REPO_RAW}/tests/{ten_file}", os.path.join("tests", ten_file))

if os.getcwd() not in sys.path:
    sys.path.insert(0, os.getcwd())

# Xoa cache module cu neu o nay da tung chay trong phien nay - tranh dung ban
# cu trong RAM du file tren dia da tai moi.
for ten_module in ("tests.giao_dien_thi", "tests.de_thi_cau_hoi", "tests.test_final", "tests.runner", "tests"):
    sys.modules.pop(ten_module, None)

from tests.giao_dien_thi import chay_bai_thi

chay_bai_thi()

# %% [markdown]
# ### Nộp bài
#
# Kết quả chỉ nằm trong phiên làm bài. Chụp màn hình bảng điểm tổng kết.
#
# `File > Save a copy in GitHub`, chọn repo của bạn, đường dẫn `final/final_test.ipynb`.
#
# Chúc mừng bạn đã hoàn thành khoá AI Course v2 tại BK-AUTO!

# %% [markdown]
# ---
# ### Phụ lục — bản chữ của đề
#
# Dùng khi giao diện ở trên không dựng được.
#
# **Câu 1:** Đâu là cách khai báo một hằng số cấu hình hệ thống (theo quy ước) trong Python?
# A. `const MAX_SPEED = 40`　B. `MAX_SPEED = 40`　C. `let MAX_SPEED = 40`　D. `final MAX_SPEED = 40`
#
# **Câu 2:** Cho `lidar_data = [1.2, 2.5, 3.1, 0.8, 4.5]`. Cú pháp nào để lấy 3 giá trị cuối cùng?
# A. `lidar_data[2:5]`　B. `lidar_data[-3:]`　C. `lidar_data[:-3]`　D. Cả A và B đều đúng.
#
# **Câu 3:** `config = {"mode": "auto", "speed": 20}`. Lệnh nào sau đây sẽ gây ra lỗi?
# A. `config["speed"] = 30`　B. `config.update({"camera": "on"})`　C. `config.add("sensor", "lidar")`　D. `config["mode"] = "manual"`
#
# **Câu 4:** Kết quả của biểu thức `True and False or not False` là gì?
# A. `True`　B. `False`　C. `None`　D. Lỗi cú pháp (Syntax Error)
#
# **Câu 5:** Khối lệnh `finally` trong cấu trúc `try...except` hoạt động như thế nào?
# A. Chỉ chạy khi khối `try` có lỗi.　B. Chỉ chạy khi khối `except` không bắt được lỗi.
# C. Luôn luôn chạy, bất kể có lỗi hay không.　D. Chỉ chạy khi không có lỗi nào xảy ra.
#
# **Câu 6:** Từ khóa nào dùng để bỏ qua lần đọc hiện tại và chuyển ngay sang lần lặp tiếp theo nếu dữ liệu bị nhiễu?
# A. `break`　B. `pass`　C. `continue`　D. `return`
#
# **Câu 7:** Phát biểu nào đúng về tham số mặc định (default arguments)?
# A. Phải đặt trước các tham số không có giá trị mặc định.　B. Phải đặt sau cùng trong danh sách tham số.
# C. Không thể thay đổi giá trị khi gọi hàm.　D. Một hàm chỉ được phép có tối đa một tham số mặc định.
#
# **Câu 8:** Tham số `self` trong các phương thức của một Class có ý nghĩa gì?
# A. Trỏ đến lớp cha.　B. Từ khóa khai báo biến toàn cục.
# C. Trỏ đến chính đối tượng (instance) đang gọi phương thức.　D. Đại diện cho `__init__`.
#
# **Câu 9:** Để biến `__trang_thai_dong_co` trở thành private, nguyên lý nào của OOP đang được áp dụng?
# A. Kế thừa　B. Đóng gói (Encapsulation)　C. Đa hình　D. Trừu tượng
#
# **Câu 10:** Hàm `super().__init__()` dùng trong Lớp con nhằm mục đích gì?
# A. Khởi tạo lại toàn bộ phương thức của Lớp con.　B. Gọi hàm khởi tạo của Lớp cha để kế thừa thuộc tính nền tảng.
# C. Xóa các thuộc tính của Lớp cha.　D. Kiểm tra Lớp cha có tồn tại hay không.
#
# **Câu 11:** `Camera_Module` kế thừa từ `Sensor` và định nghĩa lại `read_data()`. Tính chất nào đang thể hiện?
# A. Ghi đè phương thức (Method Overriding) - biểu hiện của Đa hình.　B. Đóng gói dữ liệu.
# C. Nạp chồng phương thức (Overloading).　D. Biến tĩnh.
#
# **Câu 12:** Lập lịch tác vụ theo nguyên tắc "lệnh nào đến trước xử lý trước" — cấu trúc nào phù hợp?
# A. Stack　B. Queue　C. Set　D. Graph
#
# **Câu 13:** Ngăn xếp (Stack) hoạt động theo nguyên lý nào?
# A. FIFO　B. LIFO　C. Random Access　D. Key-Value Pair
#
# **Câu 14:** Big O của Tìm kiếm nhị phân trên mảng đã sắp xếp là bao nhiêu?
# A. O(1)　B. O(n)　C. O(log n)　D. O(n²)
#
# **Câu 15:** Điều kiện dừng (Base Case) trong Đệ quy có vai trò gì?
# A. Làm thuật toán chạy nhanh hơn.　B. Tránh tràn bộ nhớ (Stack Overflow) do gọi vô hạn.
# C. Reset lại biến toàn cục.　D. Trả về giá trị mặc định nếu đầu vào sai.
#
# **Câu 16:** Xung đột (Collision) trong Bảng băm xảy ra khi nào?
# A. Bảng băm hết dung lượng.　B. Hai khóa khác nhau bị hàm băm trả về cùng một chỉ mục.
# C. Xóa một phần tử không tồn tại.　D. Cập nhật giá trị của một khóa đã có.
#
# **Câu 17:** Một Node trong Cây không có bất kỳ Node con nào thì gọi là gì?
# A. Gốc (Root)　B. Nhánh (Branch)　C. Cạnh (Edge)　D. Lá (Leaf)
#
# **Câu 18:** Trong BST, quy tắc sắp xếp Node con so với Node cha là gì?
# A. Trái lớn hơn, phải nhỏ hơn.　B. Cả hai đều lớn hơn.
# C. Trái nhỏ hơn, phải lớn hơn.　D. Sắp xếp ngẫu nhiên.
#
# **Câu 19:** Biểu diễn bản đồ Waypoint đã biết trước khoảng cách giữa các điểm nối — nên dùng cấu trúc nào?
# A. Đồ thị vô hướng không trọng số.　B. Đồ thị có trọng số (Weighted Graph).
# C. Danh sách liên kết đơn.　D. Bảng băm.
#
# **Câu 20:** Kỹ thuật lưu kết quả bài toán con đã giải để không tính lại trong DP gọi là gì?
# A. Memoization　B. Recursion　C. Backtracking　D. Linear Probing
#
# **Phần 2 — Bài thực hành:** viết hàm `gop_khung_thoi_gian(intervals)` nhận list các
# khung `[start, end]`, gộp mọi khung chồng chéo, trả về lịch trình đã gộp sắp theo
# `start` tăng dần. `[[1, 3], [2, 6], [8, 10]]` → `[[1, 6], [8, 10]]`. `[[1, 4], [4, 5]]`
# → `[[1, 5]]`. Đầu vào có thể chưa sắp xếp, yêu cầu `O(n log n)`.
