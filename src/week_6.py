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
# # Tuần 6 — Cấu trúc dữ liệu phi tuyến (Đồ thị, Cây) & Tổng kết
#
# **Mục tiêu sau tuần này, bạn phải làm được:**
#
# 1. Biểu diễn và duyệt Cây (Tree), đặc biệt là Cây tìm kiếm nhị phân (BST).
# 2. Biểu diễn Đồ thị (Graph) bằng Danh sách kề, tìm đường đi bằng DFS.
# 3. Hiểu Quy hoạch động (Dynamic Programming) qua kỹ thuật Memoization.
#
# Đây là tuần cuối phần kiến thức — sau tuần này là ôn tập và thi cuối khoá.
#
# Thời lượng ước tính: 3–4 giờ tự học.

# %%
# Ô thiết lập - chạy đầu tiên, mỗi lần mở notebook.
import os
import sys
import urllib.request

REPO_RAW = "https://raw.githubusercontent.com/dongthethang2k15kkk/AI-Course-v2/main"

if not os.path.isdir("tests"):
    os.makedirs("tests", exist_ok=True)
    open(os.path.join("tests", "__init__.py"), "w").close()
    for ten_file in ("runner.py", "test_week6.py"):
        urllib.request.urlretrieve(
            f"{REPO_RAW}/tests/{ten_file}", os.path.join("tests", ten_file)
        )

if os.getcwd() not in sys.path:
    sys.path.insert(0, os.getcwd())

from tests.test_week6 import kiem_tra_1_1, kiem_tra_2_1, kiem_tra_2_2

print("Moi truong san sang. Phien ban Python:", sys.version.split()[0])

# %% [markdown]
# ---
# ## Bài 1 — Cấu trúc Cây (Trees)
#
# ### Lý thuyết
#
# Cây là cấu trúc dữ liệu **phân cấp**: một **Gốc (Root)** ở trên cùng, mỗi
# **Nút (Node)** có thể có các **Nút con**, nút không có con gọi là **Lá (Leaf)**.
#
# **Cây nhị phân (Binary Tree):** mỗi nút có tối đa 2 nút con — trái và phải.
#
# **Cây tìm kiếm nhị phân (BST):** thêm một quy tắc sắp xếp — với mọi nút, **toàn
# bộ nút bên trái nhỏ hơn nó, toàn bộ nút bên phải lớn hơn hoặc bằng nó**. Nhờ quy
# tắc này, tìm kiếm trên BST cân đối chỉ mất `O(log n)`, giống Tìm kiếm nhị phân
# tuần trước.
#
# **Duyệt cây (Traversal):** In-order (trái → gốc → phải), Pre-order (gốc → trái →
# phải), Post-order (trái → phải → gốc). Bài tập tuần này chỉ cần rẽ trái liên tục
# để tìm giá trị nhỏ nhất — không cần duyệt hết cây.

# %%
class NutQuyetDinh:
    def __init__(self, cau_hoi, nhanh_dung=None, nhanh_sai=None):
        self.cau_hoi = cau_hoi
        self.nhanh_dung = nhanh_dung
        self.nhanh_sai = nhanh_sai


la_phanh = "Hanh dong: Phanh khan cap"
la_lai = "Hanh dong: Danh lai tranh vat can"
la_di = "Hanh dong: Duy tri toc do"

nut_vat_can = NutQuyetDinh("Co vat can phia truoc khong?", la_phanh, la_di)
goc_lech_lan = NutQuyetDinh("Xe co dang lech lan khong?", la_lai, nut_vat_can)

print(f"Goc: {goc_lech_lan.cau_hoi}")
print(f" -> Neu Dung: {goc_lech_lan.nhanh_dung}")
print(f" -> Neu Sai, kiem tra tiep: {goc_lech_lan.nhanh_sai.cau_hoi}")

# %% [markdown]
# ### Lỗi thường gặp
#
# **1. Chèn vào BST mà không giữ đúng quy tắc trái-nhỏ/phải-lớn** — cây vẫn "chạy"
# nhưng không còn là BST nữa, mọi lợi ích tốc độ tìm kiếm mất hết.
#
# **2. Quên trả về nút gốc sau khi chèn đệ quy.** Hàm `chen_bst` phải trả về nút
# gốc ở mỗi lớp đệ quy, để lớp gọi bên ngoài gán lại đúng `.trai`/`.phai` — quên
# bước này khiến các nhánh không được nối lại vào cây.
#
# **3. Không xử lý trường hợp cây rỗng (`goc is None`)** trước khi chèn — đây
# chính là điều kiện dừng của đệ quy chèn.
#
# ### Bài tập 1.1 — Tổ chức dữ liệu cảm biến bằng BST
#
# Viết:
#
# - `class NutBST`: `__init__(self, gia_tri)` — lưu `gia_tri`, khởi tạo
#   `self.trai = None` và `self.phai = None`.
# - `chen_bst(goc, gia_tri)` — chèn `gia_tri` vào cây có gốc `goc` (đệ quy). Nếu
#   `goc` là `None`, tạo `NutBST` mới và trả về nó. `gia_tri` nhỏ hơn `goc.gia_tri`
#   thì rẽ trái, ngược lại rẽ phải. **Luôn trả về `goc`** sau khi xử lý.
# - `tim_nho_nhat(goc)` — trả về giá trị nhỏ nhất trong cây, bằng cách rẽ trái
#   liên tục cho tới khi không còn nút trái nào nữa.

# %%
class NutBST:
    def __init__(self, gia_tri):
        # TODO: lưu gia_tri, self.trai = None, self.phai = None
        pass


def chen_bst(goc, gia_tri):
    # TODO: nếu goc None -> tạo NutBST mới; không thì rẽ trái/phải theo gia_tri;
    # luôn trả về goc
    pass


def tim_nho_nhat(goc):
    # TODO: rẽ trái liên tục cho tới khi hết nút trái, trả về gia_tri ở đó
    pass


# %%
kiem_tra_1_1(NutBST, chen_bst, tim_nho_nhat)

# %% [markdown]
# ---
# ## Bài 2 — Đồ thị (Graphs) và Quy hoạch động
#
# ### Lý thuyết
#
# **Đồ thị** là mạng lưới các **Đỉnh (Vertices)** nối nhau qua **Cạnh (Edges)**.
# Có hướng (chỉ đi được 1 chiều) hoặc vô hướng, có trọng số hoặc không.
#
# **Danh sách kề (Adjacency List)** — cách biểu diễn phổ biến nhất bằng `dict`:
# khoá là tên đỉnh, giá trị là list các đỉnh liền kề.
#
# **Quy hoạch động (DP)** tối ưu các bài toán có **bài toán con lặp lại**, bằng
# cách lưu lại (Memoization) kết quả đã tính, tránh tính lại nhiều lần.

# %%
mang_luoi_duong = {
    "Nut A": ["Nut B", "Nut C"],
    "Nut B": ["Nut A", "Nut D"],
    "Nut C": ["Nut A", "Nut D"],
    "Nut D": ["Nut B", "Nut C", "Dich"],
}


def tim_duong_di_vi_du(do_thi, dau, cuoi, duong_di=None):
    if duong_di is None:
        duong_di = []
    duong_di = duong_di + [dau]
    if dau == cuoi:
        return [duong_di]
    if dau not in do_thi:
        return []
    tat_ca = []
    for lang_gieng in do_thi[dau]:
        if lang_gieng not in duong_di:
            tat_ca.extend(tim_duong_di_vi_du(do_thi, lang_gieng, cuoi, duong_di))
    return tat_ca


print("Cac lo trinh kha thi:", tim_duong_di_vi_du(mang_luoi_duong, "Nut A", "Dich"))

# %% [markdown]
# ### Lỗi thường gặp
#
# **1. Không kiểm tra đỉnh đã đi qua chưa** — với đồ thị có chu trình (đi vòng
# lại được), thiếu kiểm tra này gây lặp vô hạn.
#
# **2. Sửa trực tiếp list `duong_di` bằng `.append()` thay vì tạo list mới
# (`duong_di + [dau]`)** — vì `duong_di` được truyền qua các lớp đệ quy, sửa trực
# tiếp làm các nhánh đệ quy khác nhau **dùng chung một list**, gây kết quả sai (bẫy
# giống tham số mặc định mutable ở tuần 2).
#
# **3. Quên trường hợp đệ quy đơn giản nhất trong Fibonacci** (`fibonacci_memo(0)`,
# `fibonacci_memo(1)`) — thiếu điều kiện dừng đúng làm sai toàn bộ dãy số.
#
# **4. Tạo `cache` mới ở mỗi lần gọi đệ quy** thay vì dùng chung một `cache`
# xuyên suốt — làm mất hoàn toàn tác dụng của memoization (chương trình vẫn đúng
# nhưng chạy chậm y hệt bản không tối ưu).

# %%
import time


def fib_khong_memo(n):
    if n <= 1:
        return n
    return fib_khong_memo(n - 1) + fib_khong_memo(n - 2)


bat_dau = time.perf_counter()
print(fib_khong_memo(28))
print(f"Khong memoization: {time.perf_counter() - bat_dau:.3f} giay")

# %% [markdown]
# ### Bài tập 2.1 — Tìm tất cả đường đi bằng DFS
#
# Viết hàm `tim_tat_ca_duong_di(do_thi, diem_dau, diem_cuoi, duong_di=None)` —
# giống hệt ví dụ ở trên nhưng tự viết lại. Trả về **list các đường đi**, mỗi
# đường đi là một list các đỉnh theo đúng thứ tự đi qua.

# %%
def tim_tat_ca_duong_di(do_thi, diem_dau, diem_cuoi, duong_di=None):
    # TODO: đệ quy DFS, tự viết lại theo đúng logic ví dụ trên
    pass


# %%
kiem_tra_2_1(tim_tat_ca_duong_di)

# %% [markdown]
# ### Bài tập 2.2 — Fibonacci với Memoization
#
# Viết hàm `fibonacci_memo(n, cache=None)` trả về số Fibonacci thứ `n`
# (`fib(0) = 0`, `fib(1) = 1`, `fib(2) = 1`, `fib(3) = 2`, ...), có dùng
# memoization để không tính lại các bài toán con đã giải.
#
# Gợi ý: nếu `cache is None`, tạo `cache = {}` mới. Trước khi tính, kiểm tra `n`
# đã có trong `cache` chưa — nếu có thì trả về ngay. Sau khi tính xong, lưu kết
# quả vào `cache[n]` trước khi trả về.

# %%
def fibonacci_memo(n, cache=None):
    # TODO: kiểm tra cache trước, đệ quy có lưu cache, xử lý n <= 1
    pass


# %%
kiem_tra_2_2(fibonacci_memo)

# %%
# So sánh tốc độ với bản không memoization ở trên (không chấm điểm, chỉ để thấy rõ)
bat_dau = time.perf_counter()
print(fibonacci_memo(28))
print(f"Co memoization: {time.perf_counter() - bat_dau:.5f} giay")

# %% [markdown]
# ---
# ## Bài 3 — Tổng kết khoá học & Chinh phục chứng chỉ
#
# Chúc mừng bạn đã đi hết 6 tuần: từ biến cơ bản → cấu trúc điều khiển → lập
# trình hướng đối tượng → cấu trúc dữ liệu & thuật toán.
#
# Trước khi thi, nên ôn lại 5 Dự án cấp chứng chỉ đã làm ở các tuần trước — đây
# chính là những bài thể hiện rõ nhất năng lực thực chiến của bạn:
#
# | Tuần | Dự án |
# |---|---|
# | 2 | Bộ quản lý cấu hình người dùng |
# | 3 | Budget App (Category) |
# | 4 | Máy tính diện tích đa giác |
# | 5 | Tháp Hà Nội + Bảng băm tự cài đặt |
# | 6 | BST + DFS tìm đường + Fibonacci memo |
#
# Đề thi cuối khoá (20 câu trắc nghiệm + 1 bài code) nằm ở notebook riêng
# `final/final_test.ipynb` — mở bằng badge ở README của repo.

# %% [markdown]
# ---
# ## Tổng kết tuần 6

# %%
ket_qua = [
    kiem_tra_1_1(NutBST, chen_bst, tim_nho_nhat),
    kiem_tra_2_1(tim_tat_ca_duong_di),
    kiem_tra_2_2(fibonacci_memo),
]

print(f"\nTONG KET TUAN 6: {sum(ket_qua)}/{len(ket_qua)} bai dat.")
print("Hoan thanh tuan 6! Tiep theo: mo notebook final/final_test.ipynb de thi cuoi khoa.")

# %% [markdown]
# ### Nộp bài
#
# `File > Save a copy in GitHub`, chọn repo của bạn, đường dẫn `week6/week_6.ipynb`.