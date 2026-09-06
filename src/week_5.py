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
# # Tuần 5 — Thuật toán cốt lõi & Bảng băm (Hash Table)
#
# **Mục tiêu sau tuần này, bạn phải làm được:**
#
# 1. Hiểu Big O ở mức đủ dùng: vì sao có thuật toán nhanh hơn thuật toán khác.
# 2. Viết được hàm đệ quy đúng (có điều kiện dừng + bước thu hẹp bài toán).
# 3. Cài đặt Tìm kiếm nhị phân, Merge Sort, và tự xây một Bảng băm từ đầu.

# %%
# Ô thiết lập - chạy đầu tiên, mỗi lần mở notebook.
import os
import sys
import urllib.request

REPO_RAW = "https://raw.githubusercontent.com/dongthethang2k15kkk/AI-for-Automotive-Course-v2/main"

if not os.path.isdir("tests"):
    os.makedirs("tests", exist_ok=True)
    open(os.path.join("tests", "__init__.py"), "w").close()
    for ten_file in ("runner.py", "test_week5.py"):
        urllib.request.urlretrieve(
            f"{REPO_RAW}/tests/{ten_file}", os.path.join("tests", ten_file)
        )

if os.getcwd() not in sys.path:
    sys.path.insert(0, os.getcwd())

from tests.test_week5 import kiem_tra_1_1, kiem_tra_2_1, kiem_tra_2_2, kiem_tra_du_an

print("Moi truong san sang. Phien ban Python:", sys.version.split()[0])

# %% [markdown]
# ---
# ## Bài 1 — Phân tích thuật toán & Đệ quy
#
# Big O đo tốc độ tăng của thời gian chạy khi dữ liệu đầu vào tăng lên, không phải
# thời gian chạy tuyệt đối. Từ nhanh đến chậm: `O(1)` (hằng số) < `O(log n)` (chia
# đôi) < `O(n)` (duyệt hết) < `O(n²)` (duyệt lồng nhau).
#
# Đệ quy là một hàm tự gọi lại chính nó. Bắt buộc phải có 2 phần:
#
# 1. **Điều kiện dừng (Base Case)** — không có nó, hàm gọi vô hạn, tràn bộ nhớ
#    (`RecursionError`).
# 2. **Bước đệ quy (Recursive Step)** — thu hẹp bài toán, tiến dần về điều kiện dừng.
#
# Mỗi lần hàm tự gọi, Python xếp thêm một khung vào **Call Stack**. Khung chỉ được
# gỡ ra khi lệnh gọi đó hoàn tất — nên đệ quy quá sâu (hàng chục nghìn lớp) sẽ
# tràn bộ nhớ.

# %%
def dem_nguoc_khoi_dong(so_buoc_con_lai):
    if so_buoc_con_lai <= 0:                       # Base Case
        print("He thong san sang. Kich hoat dong co!")
        return
    print(f"Kiem tra module so {so_buoc_con_lai}...")
    dem_nguoc_khoi_dong(so_buoc_con_lai - 1)        # Recursive Step


dem_nguoc_khoi_dong(3)

# %% [markdown]
# ### Lỗi thường gặp
#
# **1. Quên điều kiện dừng, hoặc điều kiện dừng không bao giờ đạt tới** — hàm gọi
# vô hạn, Python báo `RecursionError: maximum recursion depth exceeded`.
#
# **2. Bước đệ quy không thực sự thu hẹp bài toán** (ví dụ gọi lại với đúng tham
# số cũ) — cũng dẫn tới lặp vô hạn dù có điều kiện dừng.
#
# **3. Tưởng đệ quy luôn nhanh hơn vòng lặp.** Không đúng — đệ quy tốn thêm bộ
# nhớ cho Call Stack. Đệ quy chỉ đáng dùng khi bài toán tự nhiên có cấu trúc chia
# nhỏ giống hệt nhau (như Tháp Hà Nội, Merge Sort dưới đây).
#
# ### Bài tập 1.1 — Tháp Hà Nội (Dự án cấp chứng chỉ 5)
#
# Chuyển `so_dia` cái đĩa từ cột `cot_nguon` sang cột `cot_dich`, dùng
# `cot_trung_gian` làm trung chuyển. Quy tắc: chỉ chuyển 1 đĩa mỗi lần, không được
# đặt đĩa to lên đĩa nhỏ.
#
# Viết hàm `thap_ha_noi(so_dia, cot_nguon="A", cot_dich="C", cot_trung_gian="B")`
# trả về một **list các bước di chuyển**, mỗi bước là `tuple (cot_nguon, cot_dich)`
# của riêng bước đó.
#
# Đệ quy theo đúng thứ tự sau (đổi thứ tự thì kết quả không khớp mẫu bên dưới):
#
# 1. Chuyển `so_dia - 1` đĩa từ `cot_nguon` sang `cot_trung_gian` (dùng `cot_dich`
#    làm trung chuyển cho bước con này).
# 2. Ghi lại bước chuyển đĩa lớn nhất: từ `cot_nguon` sang `cot_dich`.
# 3. Chuyển `so_dia - 1` đĩa từ `cot_trung_gian` sang `cot_dich` (dùng `cot_nguon`
#    làm trung chuyển cho bước con này).
#
# Điều kiện dừng: `so_dia == 0` thì không có bước nào cả.
#
# Ví dụ: `thap_ha_noi(2)` → `[("A", "B"), ("A", "C"), ("B", "C")]`.

# %%
def thap_ha_noi(so_dia, cot_nguon="A", cot_dich="C", cot_trung_gian="B"):
    # TODO: đệ quy theo đúng 3 bước ở trên, gom các tuple (nguon, dich) vào 1 list
    pass


# %%
kiem_tra_1_1(thap_ha_noi)

# %% [markdown]
# ---
# ## Bài 2 — Thuật toán Sắp xếp và Tìm kiếm
#
# Tìm kiếm tuyến tính: duyệt từng phần tử, `O(n)`.
#
# Tìm kiếm nhị phân: chỉ áp dụng được trên mảng đã sắp xếp. Mỗi bước loại bỏ một
# nửa mảng còn lại, `O(log n)`, nhanh hơn hẳn tìm kiếm tuyến tính khi dữ liệu lớn.
#
# Merge Sort: chia mảng làm đôi, đệ quy sắp xếp từng nửa, rồi trộn (merge) hai
# nửa đã sắp xếp lại thành một mảng sắp xếp hoàn chỉnh, `O(n log n)`. Nhanh hơn
# Bubble Sort (`O(n²)`) khi dữ liệu lớn.

# %%
def binary_search_log_vi_du(log_timestamps, target_time):
    left, right = 0, len(log_timestamps) - 1
    while left <= right:
        mid = (left + right) // 2
        if log_timestamps[mid] == target_time:
            return mid
        elif log_timestamps[mid] < target_time:
            left = mid + 1
        else:
            right = mid - 1
    return -1


telemetry_logs = [100, 150, 200, 250, 300, 350, 400]
print(binary_search_log_vi_du(telemetry_logs, 250))

# %% [markdown]
# ### Lỗi thường gặp
#
# **1. Dùng Tìm kiếm nhị phân trên mảng CHƯA sắp xếp** — thuật toán sẽ cho kết quả
# sai mà không báo lỗi gì, rất khó phát hiện.
#
# **2. Sai công thức tính `mid`, hoặc quên cập nhật `left`/`right`** → lặp vô hạn
# hoặc bỏ sót phần tử cần tìm.
#
# **3. Merge Sort quên điều kiện dừng** (`len(danh_sach) <= 1`) — mảng 0 hoặc 1
# phần tử đã tự nó là "đã sắp xếp", không cần chia tiếp.
#
# **4. Merge hai nửa sai thứ tự** — quên so sánh phần tử đầu của 2 nửa trước khi
# lấy ra, dẫn đến kết quả không thực sự sắp xếp.

# %%
def cong_thuc_mid_dung(left, right):
    return (left + right) // 2  # không dùng (left + right) / 2 -> ra float, sai chỉ số


print(cong_thuc_mid_dung(0, 7))

# %% [markdown]
# ### Bài tập 2.1 — Sắp xếp mảng vật cản (Merge Sort)
#
# Viết hàm `sap_xep_vat_can(danh_sach)` bằng **Merge Sort**. `danh_sach` là một
# list các `dict`, mỗi phần tử có khoá `"ten"` và `"khoang_cach"`. Trả về list mới
# đã sắp xếp theo `"khoang_cach"` **tăng dần** (vật cản gần nhất lên đầu).
#
# Gợi ý cấu trúc: chia đôi `danh_sach`, gọi đệ quy `sap_xep_vat_can` cho từng nửa,
# rồi viết một vòng lặp trộn (merge) hai nửa đã sắp xếp lại với nhau.

# %%
def sap_xep_vat_can(danh_sach):
    # TODO: Merge Sort - chia đôi, đệ quy sắp từng nửa, rồi trộn lại theo khoang_cach
    pass


# %%
kiem_tra_2_1(sap_xep_vat_can)

# %% [markdown]
# Bây giờ đã tự tay viết Merge Sort, bạn hiểu vì sao `O(n log n)` nhanh hơn
# `O(n²)`. Trong công việc thực tế không cần viết lại thuật toán sắp xếp — Python
# có sẵn `sorted(ds)` (trả về list mới) và `ds.sort()` (sắp xếp ngay trên `ds`),
# cả hai đều chạy `O(n log n)`. Truyền thêm `key=...` để sắp theo một tiêu chí
# khác thay vì so sánh trực tiếp giá trị phần tử.

# %%
vat_can_tho = [{"ten": "coc", "khoang_cach": 5.2}, {"ten": "xe", "khoang_cach": 1.1}]
print(sorted(vat_can_tho, key=lambda vt: vt["khoang_cach"]))

# %% [markdown]
# ### Bài tập 2.2 — Tìm kiếm nhị phân trong log
#
# Viết hàm `binary_search_log(log_timestamps, target_time)` — giống hệt ví dụ ở
# trên nhưng bạn tự viết lại (đừng copy) để chắc chắn hiểu rõ từng bước. Trả về
# chỉ số (index) nếu tìm thấy, `-1` nếu không.

# %%
def binary_search_log(log_timestamps, target_time):
    # TODO: tự viết lại thuật toán tìm kiếm nhị phân
    pass


# %%
kiem_tra_2_2(binary_search_log)

# %% [markdown]
# ---
# ## Bài 3 — Bảng băm (Hash Table)
#
# `dict` và `set` của Python được cài đặt bên trong bằng Bảng băm, cho phép
# thêm/tìm/xoá gần như tức thời, `O(1)` trung bình.
#
# Hàm băm (Hash Function) biến một khoá (thường là chuỗi) thành một số nguyên,
# rồi chia dư cho kích thước bảng để xác định "ngăn" lưu trữ.
#
# Xung đột (Collision) xảy ra khi hai khoá khác nhau bị hàm băm trả về cùng một
# ngăn. Cách xử lý phổ biến nhất là Chaining: mỗi ngăn không lưu 1 giá trị, mà lưu
# một list các cặp `(khoá, giá trị)`; khi tra cứu, duyệt list đó để tìm đúng khoá.

# %%
def ham_bam_don_gian(dia_chi_mac, kich_thuoc_bang):
    tong_ma_ascii = sum(ord(ky_tu) for ky_tu in dia_chi_mac)
    return tong_ma_ascii % kich_thuoc_bang


kich_thuoc = 10
print(f"Module A luu o ngan so: {ham_bam_don_gian('AA:BB:CC:DD:EE:01', kich_thuoc)}")
print(f"Module B luu o ngan so: {ham_bam_don_gian('AA:BB:CC:DD:EE:02', kich_thuoc)}")

# %% [markdown]
# ### Lỗi thường gặp
#
# **1. Bỏ qua xử lý xung đột** — coi như mỗi ngăn chỉ chứa được 1 giá trị, khoá
# đến sau ghi đè mất khoá đến trước dù chúng là 2 khoá khác nhau. Đây là lỗi phổ
# biến nhất khi tự cài Hash Table.
#
# **2. `insert` cùng một khoá 2 lần lại tạo thành 2 bản ghi trùng** thay vì cập
# nhật giá trị của bản ghi cũ — phải kiểm tra khoá đã tồn tại trong ngăn chưa
# trước khi thêm mới.
#
# **3. Hàm băm cho ra chỉ số vượt quá kích thước bảng** — luôn nhớ chia dư
# (`% kich_thuoc_bang`) để chỉ số nằm trong giới hạn.
#
# ### Dự án 4 — Bảng băm tự cài đặt
#
# Không dùng `dict` có sẵn của Python. Viết class `BangBam`:
#
# - `__init__(self, kich_thuoc=16)` — tạo `self.bang`: một `list` gồm `kich_thuoc`
#   ngăn, mỗi ngăn ban đầu là một `list` rỗng (dùng cho Chaining).
# - Viết một phương thức băm nội bộ (ví dụ `_bam`), dựa trên tổng mã ASCII của
#   khoá, chia dư cho `kich_thuoc`.
# - `insert(self, khoa, gia_tri)` — nếu `khoa` đã có trong ngăn tương ứng, **ghi
#   đè** giá trị cũ; nếu chưa có, thêm cặp `(khoa, gia_tri)` mới vào ngăn.
# - `get(self, khoa)` — trả về giá trị nếu tìm thấy `khoa`, `None` nếu không.
# - `delete(self, khoa)` — xoá cặp có `khoa` này khỏi ngăn, trả về `True` nếu xoá
#   được, `False` nếu `khoa` không tồn tại.

# %%
class BangBam:
    def __init__(self, kich_thuoc=16):
        # TODO: lưu kich_thuoc, tạo self.bang = list các list rỗng
        pass

    def _bam(self, khoa):
        # TODO: tổng mã ASCII của str(khoa), chia dư cho self.kich_thuoc
        pass

    def insert(self, khoa, gia_tri):
        # TODO: tìm ngăn qua _bam(); nếu khoa đã có thì ghi đè, không thì append mới
        pass

    def get(self, khoa):
        # TODO: tìm trong đúng ngăn, trả về gia_tri nếu thấy khoa, None nếu không
        pass

    def delete(self, khoa):
        # TODO: xoá cặp có khoa trong đúng ngăn, trả True/False
        pass


# %%
kiem_tra_du_an(BangBam)

# %% [markdown]
# ---
# ## Tổng kết tuần 5

# %%
ket_qua = [
    kiem_tra_1_1(thap_ha_noi),
    kiem_tra_2_1(sap_xep_vat_can),
    kiem_tra_2_2(binary_search_log),
    kiem_tra_du_an(BangBam),
]

print(f"\nTONG KET TUAN 5: {sum(ket_qua)}/{len(ket_qua)} bai dat.")

# %% [markdown]
# ### Nộp bài
#
# `File > Save a copy in GitHub`, chọn repo của bạn, đường dẫn `week5/week_5.ipynb`.