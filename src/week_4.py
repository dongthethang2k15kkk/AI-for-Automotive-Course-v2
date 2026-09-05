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
# # Tuần 4 — OOP nâng cao & Cấu trúc dữ liệu tuyến tính
#
# **Mục tiêu sau tuần này, bạn phải làm được:**
#
# 1. Dùng Kế thừa (Inheritance) để tránh viết lại code, và Đa hình (Polymorphism)
#    để mỗi lớp con tự định nghĩa hành vi riêng.
# 2. Hiểu và cài đặt Stack (LIFO) và Queue (FIFO).
# 3. Hiểu Linked List hoạt động khác List (mảng) như thế nào.
#
# Thời lượng ước tính: 3–4 giờ tự học.

# %%
# Ô thiết lập - chạy đầu tiên, mỗi lần mở notebook.
import os
import sys
import urllib.request
from collections import deque

REPO_RAW = "https://raw.githubusercontent.com/dongthethang2k15kkk/AI-Course-v2/main"

if not os.path.isdir("tests"):
    os.makedirs("tests", exist_ok=True)
    open(os.path.join("tests", "__init__.py"), "w").close()
    for ten_file in ("runner.py", "test_week4.py"):
        urllib.request.urlretrieve(
            f"{REPO_RAW}/tests/{ten_file}", os.path.join("tests", ten_file)
        )

if os.getcwd() not in sys.path:
    sys.path.insert(0, os.getcwd())

from tests.test_week4 import kiem_tra_1_1, kiem_tra_2_1, kiem_tra_2_2, kiem_tra_3_1, kiem_tra_du_an

print("Moi truong san sang. Phien ban Python:", sys.version.split()[0])

# %% [markdown]
# ---
# ## Bài 1 — Kế thừa (Inheritance) và Đa hình (Polymorphism)
#
# ### Lý thuyết
#
# **Kế thừa:** lớp con (`class Con(Cha):`) tự động có toàn bộ thuộc tính và phương
# thức của lớp cha, không cần viết lại — đúng nguyên tắc DRY (Don't Repeat
# Yourself).
#
# **`super().__init__(...)`** gọi hàm khởi tạo của lớp cha từ bên trong lớp con,
# để không phải chép lại logic khởi tạo.
#
# **Ghi đè phương thức (Method Overriding)** — lớp con định nghĩa lại một phương
# thức đã có ở lớp cha, cho phù hợp đặc thù của nó. Đây chính là **Đa hình**: cùng
# một lời gọi `.doc_du_lieu()`, mỗi loại cảm biến trả lời khác nhau.
#
# **Đóng gói:** tiền tố `_` (protected, quy ước "đừng đụng vào từ bên ngoài") và
# `__` (private, Python thật sự đổi tên biến để khó truy cập từ bên ngoài hơn).

# %%
class CamBien:
    def __init__(self, ten, chan):
        self.ten = ten
        self.chan = chan
        self._trang_thai = "Online"  # protected

    def doc_du_lieu(self):
        return "Dang doc du lieu co ban..."


class Lidar(CamBien):
    def __init__(self, ten, chan, tam_quet_max):
        super().__init__(ten, chan)  # kế thừa __init__ của lớp cha
        self.tam_quet_max = tam_quet_max

    def doc_du_lieu(self):  # ghi đè - Đa hình
        return f"{self.ten} (chan {self.chan}): quet 3D trong pham vi {self.tam_quet_max}m"


class Camera(CamBien):
    def __init__(self, ten, chan, do_phan_giai):
        super().__init__(ten, chan)
        self.do_phan_giai = do_phan_giai

    def doc_du_lieu(self):
        return f"{self.ten} (chan {self.chan}): chup khung hinh {self.do_phan_giai}"


lidar_truoc = Lidar("Lidar_Truoc", chan=15, tam_quet_max=120)
cam_giua = Camera("Cam_Giua", chan=2, do_phan_giai="1080p")

print(lidar_truoc.doc_du_lieu())
print(cam_giua.doc_du_lieu())

# %% [markdown]
# ### Lỗi thường gặp
#
# **1. Quên gọi `super().__init__()`** trong lớp con — các thuộc tính của lớp cha
# sẽ không được thiết lập, gây lỗi `AttributeError` khi truy cập chúng sau này.
#
# **2. Định nghĩa lại `__init__` ở lớp con mà không nhận đủ tham số của lớp cha**
# — dẫn đến không có cách nào truyền dữ liệu xuống `super().__init__()`.
#
# **3. Nhầm ghi đè (override) với việc vô tình đặt trùng tên phương thức không
# liên quan.** Ghi đè đúng nghĩa là lớp con thay thế **hoàn toàn** hành vi đã có ở
# lớp cha cho cùng một tên phương thức.
#
# ### Cách viết chuẩn
#
# Luôn gọi `super().__init__(...)` đầu tiên trong `__init__` của lớp con — thiết
# lập nền tảng từ lớp cha trước, rồi mới thêm phần riêng của lớp con.

# %% [markdown]
# ### Bài tập 1.1 — Hệ thống nhân sự
#
# Viết 3 class:
#
# - `NhanVien` (lớp cha): `__init__(self, ten, luong_co_ban)`;
#   `tinh_tong_luong(self)` trả về `luong_co_ban`.
# - `QuanLy(NhanVien)`: `__init__(self, ten, luong_co_ban, phu_cap)`; ghi đè
#   `tinh_tong_luong` = `luong_co_ban + phu_cap`.
# - `LapTrinhVien(NhanVien)`: `__init__(self, ten, luong_co_ban, so_gio_ot,
#   don_gia_ot=100000)`; ghi đè `tinh_tong_luong` = `luong_co_ban + so_gio_ot *
#   don_gia_ot`.
#
# Cả `QuanLy` và `LapTrinhVien` phải gọi `super().__init__(ten, luong_co_ban)`.

# %%
class NhanVien:
    def __init__(self, ten, luong_co_ban):
        # TODO: lưu ten và luong_co_ban
        pass

    def tinh_tong_luong(self):
        # TODO: trả về luong_co_ban
        pass


class QuanLy(NhanVien):
    def __init__(self, ten, luong_co_ban, phu_cap):
        # TODO: gọi super().__init__(...), lưu thêm phu_cap
        pass

    def tinh_tong_luong(self):
        # TODO: ghi đè - cộng thêm phu_cap
        pass


class LapTrinhVien(NhanVien):
    def __init__(self, ten, luong_co_ban, so_gio_ot, don_gia_ot=100000):
        # TODO: gọi super().__init__(...), lưu thêm so_gio_ot và don_gia_ot
        pass

    def tinh_tong_luong(self):
        # TODO: ghi đè - cộng thêm so_gio_ot * don_gia_ot
        pass


# %%
kiem_tra_1_1(NhanVien, QuanLy, LapTrinhVien)

# %% [markdown]
# ---
# ## Bài 2 — Stack & Queue
#
# ### Lý thuyết
#
# **Stack (Ngăn xếp) — LIFO** (Last In, First Out — vào sau ra trước). Dùng
# `list` với `.append()` (đẩy vào) và `.pop()` (lấy phần tử **cuối** ra). Ứng
# dụng: Undo/Redo, nút Back của trình duyệt.
#
# **Queue (Hàng đợi) — FIFO** (First In, First Out — vào trước ra trước). Dùng
# `collections.deque` với `.append()` (đẩy vào cuối) và `.popleft()` (lấy phần tử
# **đầu** ra) — nhanh hơn `list.pop(0)` rất nhiều với dữ liệu lớn.

# %%
hang_doi_lenh = deque()
hang_doi_lenh.append("LENH_RE_TRAI")
hang_doi_lenh.append("LENH_TANG_TOC")
hang_doi_lenh.append("LENH_BAT_DEN")

print("Hang doi hien tai:", list(hang_doi_lenh))

while hang_doi_lenh:
    lenh = hang_doi_lenh.popleft()
    print(f"Dang thuc thi: {lenh}...")

# %% [markdown]
# ### Lỗi thường gặp
#
# **1. Dùng `list.pop(0)` để giả lập Queue.** Chạy được nhưng **chậm** với dữ liệu
# lớn, vì mọi phần tử còn lại phải dịch chuyển vị trí. Luôn dùng `deque` cho Queue.
#
# **2. Nhầm `.pop()` (lấy cuối, dùng cho Stack) với `.popleft()` (lấy đầu, dùng
# cho Queue).** Dùng sai hàm sẽ cho ra thứ tự ngược với yêu cầu bài toán.
#
# **3. Quên kiểm tra rỗng trước khi `.pop()`/`.popleft()`** — gọi trên cấu trúc
# rỗng sẽ báo lỗi `IndexError`.

# %%
def dao_nguoc_bang_stack_vi_du(danh_sach):
    stack = list(danh_sach)
    ket_qua = []
    while stack:
        ket_qua.append(stack.pop())  # lấy từ cuối - đúng bản chất Stack
    return ket_qua


print(dao_nguoc_bang_stack_vi_du([1, 2, 3]))

# %% [markdown]
# ### Bài tập 2.1 — Đảo ngược bằng Stack
#
# Viết hàm `dao_nguoc_bang_stack(danh_sach)` trả về list đảo ngược thứ tự,
# **bằng cách mô phỏng Stack** (dùng `.append()`/`.pop()`), không dùng
# `list(reversed(...))` hay `danh_sach[::-1]` — mục đích là luyện đúng thao tác
# Stack, dù kết quả cuối tương đương.

# %%
def dao_nguoc_bang_stack(danh_sach):
    # TODO: đẩy hết vào 1 stack (list), rồi pop() lần lượt ra list kết quả
    pass


# %%
kiem_tra_2_1(dao_nguoc_bang_stack)

# %% [markdown]
# ### Bài tập 2.2 — Điều hướng Waypoint bằng Queue
#
# Viết hàm `dieu_huong_waypoint(danh_sach_toa_do)` nhận vào một list các toạ độ
# (mỗi toạ độ là 1 tuple `(x, y)`), trả về list các thông báo theo đúng thứ tự
# **vào trước, xử lý trước**, mỗi thông báo đúng định dạng:
#
# ```
# f"Dang di chuyen toi toa do {toa_do}"
# ```
#
# Gợi ý: dùng `deque`.

# %%
def dieu_huong_waypoint(danh_sach_toa_do):
    # TODO: đưa vào deque, popleft() lần lượt, tạo chuỗi thông báo theo mẫu
    pass


# %%
kiem_tra_2_2(dieu_huong_waypoint)

# %% [markdown]
# ---
# ## Bài 3 — Danh sách liên kết (Linked List)
#
# ### Lý thuyết
#
# **Node** là đơn vị cơ bản: chứa `data` (dữ liệu) và `next` (con trỏ tới Node kế
# tiếp, hoặc `None` nếu là Node cuối).
#
# Khác với `list` (mảng) của Python — không có chỉ số (index) để nhảy thẳng tới
# một phần tử, phải **duyệt tuần tự từ đầu**. Đổi lại, chèn/xoá ở đầu danh sách
# nhanh hơn vì không cần dịch chuyển các phần tử khác.

# %%
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


dau = Node("Khoi dong he thong")
node_2 = Node("Kiem tra ngoai vi")
node_3 = Node("San sang hoat dong")

dau.next = node_2
node_2.next = node_3

hien_tai = dau
while hien_tai:
    print("Trang thai:", hien_tai.data)
    hien_tai = hien_tai.next

# %% [markdown]
# ### Lỗi thường gặp
#
# **1. Quên cập nhật `next` khi nối Node** — Node mới bị "rơi" ra khỏi danh sách,
# không ai trỏ tới nó.
#
# **2. Vòng lặp duyệt quên di chuyển `hien_tai = hien_tai.next`** → lặp vô hạn
# trên cùng một Node.
#
# **3. Không kiểm tra danh sách rỗng (`self.head is None`)** trước khi thao tác —
# gây lỗi khi cố truy cập `.next` của `None`.
#
# ### Bài tập 3.1 — Danh sách liên kết đơn
#
# Dùng class `Node` ở trên, viết class `DanhSachLienKet` với:
#
# - `__init__(self)` — `self.head = None`
# - `them_cuoi(self, data)` — tạo `Node` mới, nối vào **cuối** danh sách
# - `duyet(self)` — trả về một `list` Python chứa `data` của mọi Node, theo đúng
#   thứ tự từ đầu tới cuối

# %%
class DanhSachLienKet:
    def __init__(self):
        # TODO: self.head = None
        pass

    def them_cuoi(self, data):
        # TODO: tạo Node(data), nếu danh sách rỗng thì làm head,
        # không thì duyệt tới Node cuối rồi nối vào
        pass

    def duyet(self):
        # TODO: duyệt từ head, gom data vào 1 list rồi trả về
        pass


# %%
kiem_tra_3_1(DanhSachLienKet)

# %% [markdown]
# ---
# ## Dự án 3 — Máy tính diện tích đa giác
#
# Bài tập tổng kết phần OOP. Viết 2 class:
#
# - `HinhChuNhat`: `__init__(self, chieu_dai, chieu_rong)`; `dien_tich(self)`;
#   `chu_vi(self)` = `2 * (chieu_dai + chieu_rong)`.
# - `HinhVuong(HinhChuNhat)`: `__init__(self, canh)` — gọi
#   `super().__init__(canh, canh)`. Thêm `dat_canh(self, canh_moi)` — đổi **cả**
#   `chieu_dai` và `chieu_rong` sang `canh_moi`, để luôn đảm bảo 2 cạnh bằng nhau
#   (đặc trưng của hình vuông).
#
# `HinhVuong` **kế thừa nguyên vẹn** `dien_tich()` và `chu_vi()` từ `HinhChuNhat`
# — không cần viết lại, vì công thức vẫn đúng khi `chieu_dai == chieu_rong`.

# %%
class HinhChuNhat:
    def __init__(self, chieu_dai, chieu_rong):
        # TODO: lưu chieu_dai và chieu_rong
        pass

    def dien_tich(self):
        # TODO: trả về chieu_dai * chieu_rong
        pass

    def chu_vi(self):
        # TODO: trả về 2 * (chieu_dai + chieu_rong)
        pass


class HinhVuong(HinhChuNhat):
    def __init__(self, canh):
        # TODO: gọi super().__init__(canh, canh)
        pass

    def dat_canh(self, canh_moi):
        # TODO: đổi cả chieu_dai và chieu_rong sang canh_moi
        pass


# %%
kiem_tra_du_an(HinhChuNhat, HinhVuong)

# %% [markdown]
# ---
# ## Tổng kết tuần 4

# %%
ket_qua = [
    kiem_tra_1_1(NhanVien, QuanLy, LapTrinhVien),
    kiem_tra_2_1(dao_nguoc_bang_stack),
    kiem_tra_2_2(dieu_huong_waypoint),
    kiem_tra_3_1(DanhSachLienKet),
    kiem_tra_du_an(HinhChuNhat, HinhVuong),
]

print(f"\nTONG KET TUAN 4: {sum(ket_qua)}/{len(ket_qua)} bai dat.")

# %% [markdown]
# ### Nộp bài
#
# `File > Save a copy in GitHub`, chọn repo của bạn, đường dẫn `week4/week_4.ipynb`.