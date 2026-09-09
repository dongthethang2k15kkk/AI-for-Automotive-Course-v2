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

# %%
# Ô thiết lập - chạy đầu tiên, mỗi lần mở notebook.
import os
import sys
import urllib.request
from collections import deque

REPO_RAW = "https://raw.githubusercontent.com/dongthethang2k15kkk/AI-for-Automotive-Course-v2/main"

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
# Kế thừa: lớp con (`class Con(Cha):`) tự động có toàn bộ thuộc tính và phương
# thức của lớp cha, không cần viết lại.
#
# `super().__init__(...)` gọi hàm khởi tạo của lớp cha từ bên trong lớp con, để
# không phải chép lại logic khởi tạo.
#
# Ghi đè phương thức (Method Overriding): lớp con định nghĩa lại một phương thức
# đã có ở lớp cha, cho phù hợp đặc thù của nó. Đây chính là Đa hình: cùng một lời
# gọi `.doc_du_lieu()`, mỗi loại cảm biến trả lời khác nhau.
#
# Đóng gói: tiền tố `_` là quy ước "đừng đụng vào từ bên ngoài"; `__` là private,
# Python thật sự đổi tên biến để khó truy cập từ bên ngoài hơn.

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
# Đọc kết quả: cùng một lời gọi `.doc_du_lieu()`, `lidar_truoc` và `cam_giua` trả
# lời khác nhau — đây chính là Đa hình. Cả hai đều có thuộc tính `ten`, `chan` mà
# không class nào tự viết lại, vì `Lidar` và `Camera` đều kế thừa từ `CamBien`.
#
# Vết chạy khi tạo `Lidar("Lidar_Truoc", chan=15, tam_quet_max=120)`:
#
# | Bước | Việc | Kết quả |
# |---|---|---|
# | 1 | Gọi `Lidar.__init__`, `self` trỏ vào object mới | object chưa có thuộc tính |
# | 2 | Dòng đầu tiên: `super().__init__(ten, chan)` — nhảy sang `CamBien.__init__` | |
# | 3 | Bên trong `CamBien.__init__`: `self.ten`, `self.chan`, `self._trang_thai` | object có 3 thuộc tính |
# | 4 | `CamBien.__init__` kết thúc, quay lại `Lidar.__init__` | |
# | 5 | Dòng cuối: `self.tam_quet_max = tam_quet_max` | object có thêm thuộc tính thứ 4 |
#
# Tính chất của kế thừa và đa hình:
#
# 1. Lớp con không gọi `super().__init__()` thì các thuộc tính lớp cha thiết lập
#    trong `__init__` của nó không tồn tại — truy cập ném `AttributeError`.
# 2. Lớp con định nghĩa lại một phương thức đã có ở lớp cha (cùng tên) thì bản
#    của lớp con **luôn thắng**: gọi qua object của lớp con chạy bản mới, không
#    chạy bản của lớp cha.
# 3. `super()` gọi được mọi phương thức của lớp cha, không riêng `__init__` — ví
#    dụ `super().doc_du_lieu()` gọi đúng bản của `CamBien`, dù lớp con đã ghi đè.
# 4. `isinstance(lidar_truoc, CamBien)` trả về `True`: một object của lớp con
#    vẫn là một object của lớp cha.
#
# Lỗi thường gặp: định nghĩa lại `__init__` ở lớp con mà không nhận đủ tham số
# của lớp cha thì không có cách nào truyền dữ liệu xuống `super().__init__()`.
# Nhầm ghi đè (override — định nghĩa lại đúng tên phương thức đã có) với việc vô
# tình đặt trùng tên một phương thức không liên quan gì tới lớp cha.
#
# ### Thứ tự gọi super().__init__()
#
# Luôn gọi `super().__init__(...)` là dòng đầu tiên trong `__init__` của lớp con,
# đúng thứ tự vết chạy ở trên: phần lớp cha thiết lập trước, phần riêng của lớp
# con gán sau, tránh lớp con ghi đè lên giá trị lớp cha vừa thiết lập.

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
# Stack (Ngăn xếp) hoạt động theo nguyên tắc LIFO (Last In, First Out — vào sau ra
# trước). Dùng `list` với `.append()` (đẩy vào) và `.pop()` (lấy phần tử cuối ra).
# Ứng dụng: Undo/Redo, nút Back của trình duyệt.
#
# Queue (Hàng đợi) hoạt động theo nguyên tắc FIFO (First In, First Out — vào
# trước ra trước). Dùng `collections.deque` với `.append()` (đẩy vào cuối) và
# `.popleft()` (lấy phần tử đầu ra). `list.pop(0)` cũng lấy được phần tử đầu,
# nhưng phải dịch chuyển toàn bộ phần tử còn lại nên chậm hẳn với dữ liệu lớn;
# `deque` không có nhược điểm đó.

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
# Vết chạy nội dung `hang_doi_lenh`:
#
# | Bước | Lệnh | Nội dung sau lệnh |
# |---|---|---|
# | 1 | `append("LENH_RE_TRAI")` | `["LENH_RE_TRAI"]` |
# | 2 | `append("LENH_TANG_TOC")` | `["LENH_RE_TRAI", "LENH_TANG_TOC"]` |
# | 3 | `append("LENH_BAT_DEN")` | `["LENH_RE_TRAI", "LENH_TANG_TOC", "LENH_BAT_DEN"]` |
# | 4 | `popleft()` → `"LENH_RE_TRAI"` | `["LENH_TANG_TOC", "LENH_BAT_DEN"]` |
# | 5 | `popleft()` → `"LENH_TANG_TOC"` | `["LENH_BAT_DEN"]` |
# | 6 | `popleft()` → `"LENH_BAT_DEN"` | `[]` |
#
# `popleft()` luôn lấy đúng phần tử được `append()` sớm nhất còn lại trong hàng
# đợi — vào trước, ra trước.
#
# Stack làm ngược lại: `.append()` vẫn đẩy vào cuối, nhưng `.pop()` lấy ra từ
# cuối — vào sau, ra trước.

# %%
ngan_xep = []
ngan_xep.append("A")
ngan_xep.append("B")
ngan_xep.append("C")
print("Ngan xep:", ngan_xep)

print("Lay ra:", ngan_xep.pop())   # 'C' - phan tu vua day vao sau cung
print("Ngan xep con lai:", ngan_xep)

# %% [markdown]
# Vết chạy `ngan_xep`:
#
# | Bước | Lệnh | Nội dung sau lệnh |
# |---|---|---|
# | 1 | `append("A")` | `["A"]` |
# | 2 | `append("B")` | `["A", "B"]` |
# | 3 | `append("C")` | `["A", "B", "C"]` |
# | 4 | `pop()` → `"C"` | `["A", "B"]` |
#
# Lỗi thường gặp: dùng `list.pop(0)` để giả lập Queue chạy được nhưng chậm với
# dữ liệu lớn, vì mọi phần tử còn lại phải dịch chuyển vị trí — luôn dùng `deque`
# cho Queue. Nhầm `.pop()` (lấy cuối, dùng cho Stack) với `.popleft()` (lấy đầu,
# dùng cho Queue) cho ra thứ tự ngược với yêu cầu bài toán. Gọi `.pop()` hay
# `.popleft()` trên cấu trúc rỗng ném `IndexError` — luôn kiểm tra rỗng trước
# bằng `if ngan_xep:` hoặc `while ngan_xep:`.
#
# Bài mẫu ứng dụng Stack: kiểm tra một chuỗi dấu ngoặc tròn có cân bằng không.
# Mỗi dấu `(` đẩy vào ngăn xếp; mỗi dấu `)` phải lấy ra đúng một `(` đang chờ.

# %%
def ngoac_can_bang(chuoi):
    ngan_xep = []
    for ky_tu in chuoi:
        if ky_tu == "(":
            ngan_xep.append(ky_tu)
        elif ky_tu == ")":
            if not ngan_xep:   # gap ')' nhung khong con '(' nao de ghep
                return False
            ngan_xep.pop()
    return len(ngan_xep) == 0   # con du '(' chua duoc ghep thi khong can bang


print(ngoac_can_bang("(())"))   # True
print(ngoac_can_bang("(()"))    # False - thieu 1 dau dong
print(ngoac_can_bang("())"))    # False - du 1 dau dong

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
# Chèn một phần tử vào đầu `list` Python (`ds.insert(0, x)`) phải dịch toàn bộ
# các phần tử còn lại sang phải một vị trí. List 1 triệu phần tử thì dịch 1
# triệu lần chỉ để thêm đúng 1 phần tử vào đầu.

# %%
ds_thuong = [2, 3, 4]
ds_thuong.insert(0, 1)   # chen vao dau: phai dich [2, 3, 4] sang phai truoc
print(ds_thuong)          # [1, 2, 3, 4]

# %% [markdown]
# Danh sách liên kết (Linked List) tránh việc dịch chuyển này. Node là đơn vị cơ
# bản: chứa `data` (dữ liệu) và `next` (con trỏ tới Node kế tiếp, hoặc `None`
# nếu là Node cuối). Thêm vào đầu chỉ cần đổi một con trỏ, không đụng tới các
# Node khác. Đổi lại, không có chỉ số (index) để nhảy thẳng tới một phần tử —
# phải duyệt tuần tự từ đầu.

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
# Vết chạy con trỏ `hien_tai` qua vòng `while`:
#
# | Lượt | `hien_tai` trước dòng `print` | `.data` in ra | `hien_tai.next` |
# |---|---|---|---|
# | 1 | `dau` | "Khoi dong he thong" | `node_2` |
# | 2 | `node_2` | "Kiem tra ngoai vi" | `node_3` |
# | 3 | `node_3` | "San sang hoat dong" | `None` |
# | 4 | `None` | — | vòng dừng, điều kiện `while hien_tai` sai |
#
# Lỗi thường gặp: quên cập nhật `next` khi nối Node mới thì Node đó bị "rơi" ra
# khỏi danh sách, không ai trỏ tới nó. Vòng lặp duyệt quên di chuyển
# `hien_tai = hien_tai.next` thì lặp vô hạn trên cùng một Node (không tiến được
# tới lượt 4 trong bảng trên). Không kiểm tra danh sách rỗng trước khi thao tác
# gây lỗi khi cố truy cập `.next` của `None`.
#
# Bài mẫu, cùng kỹ thuật duyệt ở trên nhưng đếm thay vì in:

# %%
def dem_so_node(head):
    dem = 0
    hien_tai = head
    while hien_tai:
        dem += 1
        hien_tai = hien_tai.next
    return dem


print(dem_so_node(dau))   # 3

# %% [markdown]
# `them_cuoi` (bài tập dưới đây) cần thêm một biến thể của cách duyệt này: không
# đếm, mà đi tới Node **cuối cùng** — Node có `.next is None` — rồi gắn Node mới
# vào `.next` của nó.
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
# Hình vuông là một hình chữ nhật có hai cạnh bằng nhau. Tính chất này quyết
# định cách viết `HinhVuong`: mọi phương thức chỉ dùng `chieu_dai`/`chieu_rong`
# mà không quan tâm chúng có bằng nhau không (`dien_tich`, `chu_vi`) thì kế thừa
# nguyên vẹn từ `HinhChuNhat`, không cần viết lại. Phương thức nào có thể làm
# gãy tính chất "hai cạnh bằng nhau" — cụ thể là đổi một cạnh — thì phải tự
# viết lại để đổi luôn cả hai cạnh cùng lúc.
#
# Bài tập tổng kết phần OOP. Viết 2 class:
#
# - `HinhChuNhat`: `__init__(self, chieu_dai, chieu_rong)`; `dien_tich(self)`;
#   `chu_vi(self)` = `2 * (chieu_dai + chieu_rong)`.
# - `HinhVuong(HinhChuNhat)`: `__init__(self, canh)` — gọi
#   `super().__init__(canh, canh)`. Thêm `dat_canh(self, canh_moi)` — đổi cả
#   `chieu_dai` và `chieu_rong` sang `canh_moi`.
#
# `HinhVuong` kế thừa nguyên vẹn `dien_tich()` và `chu_vi()` từ `HinhChuNhat` —
# không cần viết lại, vì công thức vẫn đúng khi `chieu_dai == chieu_rong`.

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