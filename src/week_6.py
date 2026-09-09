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

# %%
# Ô thiết lập - chạy đầu tiên, mỗi lần mở notebook.
import os
import sys
import urllib.request

REPO_RAW = "https://raw.githubusercontent.com/dongthethang2k15kkk/AI-for-Automotive-Course-v2/main"

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
# Cây là cấu trúc dữ liệu phân cấp: một Gốc (Root) ở trên cùng, mỗi Nút (Node) có
# thể có các Nút con, nút không có con gọi là Lá (Leaf).

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
# `goc_lech_lan` là Gốc, `nut_vat_can` là một Nút con của nó. Cây này không có
# quy tắc sắp xếp nào — hai nhánh chỉ là "đúng" và "sai", không phải "nhỏ hơn"
# và "lớn hơn hoặc bằng".
#
# Cây tìm kiếm nhị phân (BST) thêm đúng quy tắc đó: mỗi nút có tối đa 2 nút con
# (trái, phải); với mọi nút, toàn bộ nút bên trái nhỏ hơn nó, toàn bộ nút bên
# phải lớn hơn hoặc bằng nó. Dựng tay một BST từ ba giá trị `8`, `3`, `10`:

# %%
class NutMinhHoa:
    def __init__(self, gia_tri):
        self.gia_tri = gia_tri
        self.trai = None
        self.phai = None


goc_vd = NutMinhHoa(8)
goc_vd.trai = NutMinhHoa(3)     # 3 < 8 -> nhanh trai
goc_vd.phai = NutMinhHoa(10)    # 10 >= 8 -> nhanh phai

print(goc_vd.gia_tri, goc_vd.trai.gia_tri, goc_vd.phai.gia_tri)   # 8 3 10

# %% [markdown]
# Tính chất của BST:
#
# 1. Với mọi nút, toàn bộ nhánh trái nhỏ hơn nó, toàn bộ nhánh phải lớn hơn
#    hoặc bằng nó — đúng ở mọi tầng, không chỉ ở gốc.
# 2. Hệ quả của tính chất 1: giá trị nhỏ nhất trong cây luôn nằm ở nút cuối
#    cùng khi rẽ trái liên tục từ gốc — không cần duyệt hết cây để tìm nó.
# 3. Chèn giá trị đã có sẵn trong cây thì rẽ phải (theo quy tắc "lớn hơn hoặc
#    bằng"), không ghi đè, không báo lỗi — cây chấp nhận giá trị trùng.
# 4. Cây chỉ nhanh (`O(log n)`) khi cân đối. Chèn liên tiếp các giá trị đã sắp
#    tăng dần (`1, 2, 3, 4, ...`) thì mọi nút chỉ có nhánh phải — cây suy biến
#    thành một chuỗi thẳng, tra cứu tụt về `O(n)`, mất hết lợi ích của BST.
#
# Vết chạy chèn `5` vào cây `goc_vd` ở trên:
#
# | Bước | Đang ở nút | So `5` với `gia_tri` của nút | Việc |
# |---|---|---|---|
# | 1 | gốc (`8`) | `5 < 8` | rẽ trái, sang nút `3` |
# | 2 | nút `3` | `5 >= 3` | rẽ phải; nút `3` chưa có `.phai` (đang là `None`) → tạo nút mới `5`, gán vào `.phai` |
#
# Lỗi thường gặp: chèn vào BST mà không giữ đúng quy tắc trái-nhỏ/phải-lớn thì
# cây vẫn "chạy" nhưng không còn là BST, tính chất 2 không còn đúng — tìm giá
# trị nhỏ nhất bằng cách rẽ trái liên tục sẽ cho kết quả sai. Quên trả về nút
# gốc sau khi chèn đệ quy khiến các nhánh không được nối lại vào cây (lớp gọi
# bên ngoài cần giá trị trả về đó để gán lại đúng `.trai`/`.phai`). Không xử lý
# trường hợp cây rỗng (`goc is None`) trước khi chèn — đây chính là điều kiện
# dừng của đệ quy chèn.
#
# Bài mẫu: tìm một giá trị có trong cây hay không, cùng khuôn đệ quy mà
# `chen_bst` cần — kiểm tra `goc is None`, so giá trị, rẽ trái hoặc phải.

# %%
def tim_bst(goc, gia_tri):
    if goc is None:                        # Base Case - di het cay ma khong thay
        return False
    if goc.gia_tri == gia_tri:
        return True
    if gia_tri < goc.gia_tri:
        return tim_bst(goc.trai, gia_tri)   # de quy sang nhanh trai
    return tim_bst(goc.phai, gia_tri)       # de quy sang nhanh phai


print(tim_bst(goc_vd, 3))    # True
print(tim_bst(goc_vd, 5))    # False - 5 chua duoc chen vao goc_vd

# %% [markdown]
# `chen_bst` cần thêm hai việc so với `tim_bst`: khi gặp `goc is None` thì tạo
# nút mới thay vì trả `False`, và sau khi rẽ trái/phải xong phải trả về `goc`
# (không trả `True`/`False`) để lớp gọi bên ngoài nối lại đúng nhánh.
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
# Đồ thị là mạng lưới các Đỉnh (Vertices) nối nhau qua Cạnh (Edges). Danh sách
# kề (Adjacency List) là cách biểu diễn phổ biến nhất, bằng `dict`: khoá là
# tên đỉnh, giá trị là list các đỉnh liền kề.

# %%
mang_luoi_duong = {
    "Nut A": ["Nut B", "Nut C"],
    "Nut B": ["Nut A", "Nut D"],
    "Nut C": ["Nut A", "Nut D"],
    "Nut D": ["Nut B", "Nut C", "Dich"],
}

print("Cac dinh ke voi Nut A:", mang_luoi_duong["Nut A"])

# %% [markdown]
# Tính chất của đồ thị vô hướng: nếu `B` xuất hiện trong `do_thi[A]` thì `A`
# cũng phải xuất hiện trong `do_thi[B]` — cạnh đi được cả hai chiều.

# %%
print("Nut B" in mang_luoi_duong["Nut A"] and "Nut A" in mang_luoi_duong["Nut B"])   # True

# %% [markdown]
# Đồ thị có trọng số gắn thêm một con số cho mỗi cạnh (khoảng cách, thời gian,
# chi phí — câu hỏi "nối được không" không đủ, cần biết "nối thì tốn bao
# nhiêu"). Cách biểu diễn: giá trị của mỗi đỉnh không còn là `list`, mà là
# `dict` ánh xạ đỉnh liền kề sang trọng số.

# %%
duong_co_khoang_cach = {
    "Nut A": {"Nut B": 5, "Nut C": 2},
    "Nut B": {"Nut A": 5, "Nut D": 3},
    "Nut C": {"Nut A": 2, "Nut D": 6},
    "Nut D": {"Nut B": 3, "Nut C": 6},
}

print(duong_co_khoang_cach["Nut A"]["Nut C"])   # 2 - khoang cach tu Nut A den Nut C

# %% [markdown]
# Đồ thị có chu trình (đi vòng lại được, như `mang_luoi_duong` ở trên) mà
# duyệt không kiểm tra đỉnh đã đi qua chưa sẽ lặp vô hạn: từ `Nut A` sang
# `Nut B` rồi quay lại `Nut A`, cứ thế không dừng. DFS (Depth-First Search)
# tránh việc này bằng cách nhớ lại đường đi hiện tại, không quay lại đỉnh đã
# có trong đường đi đó.
#
# Vết chạy DFS tìm đường từ `"Nut A"` tới `"Dich"`, theo đúng thứ tự các đỉnh
# xuất hiện trong `mang_luoi_duong`:
#
# | Bước | Đỉnh đang xét | Đường đi hiện tại | Láng giềng còn lại |
# |---|---|---|---|
# | 1 | `Nut A` | `[Nut A]` | `Nut B`, `Nut C` |
# | 2 | `Nut B` (từ `Nut A`) | `[Nut A, Nut B]` | `Nut D` (`Nut A` đã đi qua, bỏ qua) |
# | 3 | `Nut D` (từ `Nut B`) | `[Nut A, Nut B, Nut D]` | `Nut C`, `Dich` (`Nut B` đã đi qua, bỏ qua) |
# | 4 | `Dich` (từ `Nut D`) | `[Nut A, Nut B, Nut D, Dich]` | đây là đích — ghi nhận đường đi này |
#
# Đến bước 4 đã tìm được một đường đi. DFS không dừng lại — nó lùi về bước 3
# và thử tiếp nhánh còn lại (`Nut C`), tìm ra đường đi thứ hai
# `[Nut A, Nut C, Nut D, Dich]`, theo đúng cách nó đã lùi về bước 2 và bước 1
# để thử hết mọi láng giềng chưa đi qua.
#
# Bài mẫu: đếm số đỉnh có thể đi tới được từ một đỉnh, cùng khung đệ quy DFS ở
# trên nhưng trả về một số, không phải list các đường đi.

# %%
def dem_so_dinh_toi_duoc(do_thi, dinh_bat_dau, da_tham=None):
    if da_tham is None:
        da_tham = set()
    da_tham.add(dinh_bat_dau)
    for lang_gieng in do_thi.get(dinh_bat_dau, []):
        if lang_gieng not in da_tham:
            dem_so_dinh_toi_duoc(do_thi, lang_gieng, da_tham)
    return len(da_tham)


print(dem_so_dinh_toi_duoc(mang_luoi_duong, "Nut A"))   # 5 - ca Nut A, B, C, D, Dich

# %% [markdown]
# ### Bài tập 2.1 — Tìm tất cả đường đi bằng DFS
#
# Viết hàm `tim_tat_ca_duong_di(do_thi, diem_dau, diem_cuoi, duong_di=None)` —
# đệ quy DFS cùng khung với `dem_so_dinh_toi_duoc` ở trên, nhưng gom **list các
# đường đi** thay vì đếm số đỉnh. Trả về list các đường đi khả thi, mỗi đường
# đi là một list các đỉnh theo đúng thứ tự đi qua.
#
# Khác biệt chính: `dem_so_dinh_toi_duoc` dùng một `set` chung `da_tham` để
# không bao giờ quay lại một đỉnh trên toàn đồ thị. Bài này cần một đường đi
# *riêng* cho mỗi nhánh (giống vết chạy ở trên: nhánh qua `Nut B` và nhánh qua
# `Nut C` có hai đường đi khác nhau), nên phải tạo `duong_di` mới bằng
# `duong_di + [dinh]` ở mỗi lớp đệ quy, không dùng chung một `list`/`set` cho
# mọi nhánh.

# %%
def tim_tat_ca_duong_di(do_thi, diem_dau, diem_cuoi, duong_di=None):
    # TODO: đệ quy DFS, tự viết lại theo đúng logic ví dụ trên
    pass


# %%
kiem_tra_2_1(tim_tat_ca_duong_di)

# %% [markdown]
# Quy hoạch động (DP) tối ưu các bài toán có bài toán con lặp lại, bằng cách
# lưu lại (Memoization) kết quả đã tính để khỏi tính lại nhiều lần.

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
# Vết chạy `fib(5)` không memo — mỗi lời gọi tự tính lại từ đầu, dù đã tính
# đúng giá trị đó trước rồi:
#
# | Lời gọi `fib(2)` | Xuất phát từ | Đã tính trước chưa? |
# |---|---|---|
# | lần 1 | `fib(5)` → `fib(4)` → `fib(3)` → `fib(2)` | chưa, tính từ đầu |
# | lần 2 | `fib(5)` → `fib(4)` → `fib(2)` | có (lần 1), nhưng không nhớ lại, tính từ đầu lần nữa |
# | lần 3 | `fib(5)` → `fib(3)` → `fib(2)` | có (lần 1, 2), vẫn tính từ đầu lần thứ ba |
#
# Tính đúng `fib(5)` cần đúng 3 lần gọi `fib(2)`, đều ra `1`, đều tính lại từ
# đầu. Đây là "bài toán con lặp lại" mà memoization giải quyết: nhớ lại `1` từ
# lần đầu, bỏ qua hai lần tính lại sau.
#
# Bài mẫu memoization trên một bài toán khác Fibonacci: đếm số cách leo hết
# `n` bậc thang, mỗi lần bước 1 hoặc 2 bậc (`cach(n) = cach(n-1) + cach(n-2)`,
# `cach(0) = cach(1) = 1`).

# %%
def so_cach_leo_thang(n, cache=None):
    if cache is None:
        cache = {}
    if n in cache:                # da tinh roi - lay lai, khong tinh nua
        return cache[n]
    if n <= 1:                    # Base Case
        return 1
    ket_qua = so_cach_leo_thang(n - 1, cache) + so_cach_leo_thang(n - 2, cache)
    cache[n] = ket_qua             # luu lai truoc khi tra ve
    return ket_qua


print(so_cach_leo_thang(5))   # 8

# %% [markdown]
# Tính chất của memoization:
#
# 1. `cache` phải là **một** dict dùng chung xuyên suốt mọi lớp đệ quy — truyền
#    nó qua tham số ở mỗi lời gọi. Tạo `cache = {}` mới ở mỗi lớp thì mỗi lời
#    gọi lại có cache riêng, mất hết tác dụng.
# 2. Khoá của `cache` là chính đầu vào (`n`). Trước khi tính, kiểm tra `n` đã
#    có trong `cache` chưa — có thì trả ngay, không tính lại.
# 3. Chỉ dùng được khi hàm luôn cho cùng đầu vào ra cùng đầu ra. Hàm phụ thuộc
#    vào trạng thái bên ngoài thay đổi theo thời gian thì kết quả lưu trong
#    `cache` có thể sai ở lần gọi sau.
#
# Lỗi thường gặp: quên trường hợp đơn giản nhất (`fib(0)`, `fib(1)`) khiến
# điều kiện dừng sai, sai toàn bộ dãy số theo sau. Tạo `cache` mới ở mỗi lần
# gọi đệ quy — vi phạm tính chất 1 — làm chương trình vẫn đúng nhưng chạy chậm
# y hệt bản không tối ưu.
#
# ### Bài tập 2.2 — Fibonacci với Memoization
#
# Viết hàm `fibonacci_memo(n, cache=None)` trả về số Fibonacci thứ `n`
# (`fib(0) = 0`, `fib(1) = 1`, `fib(2) = 1`, `fib(3) = 2`, ...), có dùng
# memoization để không tính lại các bài toán con đã giải.
#
# Cùng khuôn với `so_cach_leo_thang` ở trên, chỉ đổi điều kiện dừng
# (`fib(0) = 0` thay vì `1`, `fib(1) = 1`) và công thức đệ quy dùng đúng dãy
# Fibonacci.

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
# ## Bài 3 — Tổng kết khoá học
#
# Sáu tuần đã đi qua: biến cơ bản, cấu trúc điều khiển, lập trình hướng đối
# tượng, cấu trúc dữ liệu và thuật toán.
#
# Trước khi thi, ôn lại 5 Dự án cấp chứng chỉ đã làm ở các tuần trước — mỗi dự án
# ghép nhiều bài tập nhỏ trong tuần lại thành một hệ thống hoàn chỉnh:
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
