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
# 1. Hiểu Big O bằng cách đếm số phép toán, không chỉ nhớ tên: vì sao có thuật
#    toán nhanh hơn thuật toán khác khi dữ liệu lớn lên.
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
# Đếm số phép so sánh cần làm để duyệt qua một danh sách:

# %%
danh_sach_vi_du = [3, 1, 4, 1, 5]
so_lan_so_sanh = 0

for x in danh_sach_vi_du:
    so_lan_so_sanh += 1   # moi phan tu can dung 1 lan xet

print("So lan so sanh:", so_lan_so_sanh)   # 5 - dung bang so phan tu

# %% [markdown]
# Một vòng `for` đơn xét mỗi phần tử đúng 1 lần: `n` phần tử thì `n` phép. Hai
# vòng lồng nhau, mỗi vòng chạy hết `n` lần:

# %%
so_lan_so_sanh_long = 0
for x in danh_sach_vi_du:
    for y in danh_sach_vi_du:
        so_lan_so_sanh_long += 1

print("So lan so sanh (long):", so_lan_so_sanh_long)   # 25 = 5 * 5

# %% [markdown]
# Big O đo tốc độ **tăng** của số phép toán khi `n` tăng, không phải thời gian
# chạy tuyệt đối (thời gian còn phụ thuộc máy chạy nhanh chậm). Đúng công thức
# đếm ở trên, chỉ đổi `n`:
#
# | `n` | 1 vòng: `n` phép | 2 vòng lồng: `n²` phép |
# |---|---|---|
# | 10 | 10 | 100 |
# | 100 | 100 | 10.000 |
# | 1.000 | 1.000 | 1.000.000 |
#
# `n` tăng 100 lần (từ 10 lên 1.000): `n` phép cũng tăng đúng 100 lần, còn `n²`
# phép tăng 10.000 lần. Đây là ý nghĩa "tốc độ tăng" mà Big O đo.
#
# Xếp từ nhanh đến chậm: `O(1)` (hằng số, không phụ thuộc `n`) < `O(log n)`
# (chia đôi mỗi bước, xem Tìm kiếm nhị phân ở Bài 2) < `O(n)` (một vòng) <
# `O(n²)` (hai vòng lồng).
#
# Đệ quy là một hàm tự gọi lại chính nó. Bắt buộc phải có điều kiện dừng (base
# case) — không có nó, hàm gọi vô hạn, tràn bộ nhớ (`RecursionError`) — và bước
# đệ quy (recursive step), thu hẹp bài toán, tiến dần về điều kiện dừng.

# %%
def dem_nguoc_khoi_dong(so_buoc_con_lai):
    if so_buoc_con_lai <= 0:                       # Base Case
        print("He thong san sang. Kich hoat dong co!")
        return
    print(f"Kiem tra module so {so_buoc_con_lai}...")
    dem_nguoc_khoi_dong(so_buoc_con_lai - 1)        # Recursive Step


dem_nguoc_khoi_dong(3)

# %% [markdown]
# Ví dụ trên không `return` giá trị nào, chỉ in ra rồi dừng. Phần lớn đệ quy
# cần trả kết quả ra ngoài. Tính tổng từ `1` đến `n`: `tong(n) = n + tong(n-1)`,
# và `tong(0) = 0` là điều kiện dừng.

# %%
def tong_den_n(n):
    if n == 0:                       # Base Case
        return 0
    return n + tong_den_n(n - 1)     # Recursive Step: cong n voi tong phan con lai


print(tong_den_n(4))   # 4 + 3 + 2 + 1 + 0 = 10

# %% [markdown]
# Vết chạy `tong_den_n(4)` — Call Stack chồng dần lúc gọi xuống, rồi trả ngược
# giá trị lúc quay lên:
#
# | Lớp | Lệnh gọi | Đang chờ |
# |---|---|---|
# | 0 | `tong_den_n(4)` | `4 + tong_den_n(3)` |
# | 1 | `tong_den_n(3)` | `3 + tong_den_n(2)` |
# | 2 | `tong_den_n(2)` | `2 + tong_den_n(1)` |
# | 3 | `tong_den_n(1)` | `1 + tong_den_n(0)` |
# | 4 | `tong_den_n(0)` | chạm điều kiện dừng, trả về `0` |
# | 3 | (tiếp) | `1 + 0 = 1` |
# | 2 | (tiếp) | `2 + 1 = 3` |
# | 1 | (tiếp) | `3 + 3 = 6` |
# | 0 | (tiếp) | `4 + 6 = 10` |
#
# Mỗi lớp phải chờ lớp bên dưới trả về xong mới tính tiếp được — mỗi lệnh gọi
# chiếm một khung riêng trên Call Stack cho tới khi nó xong việc.
#
# Bài tập Tháp Hà Nội cần đệ quy trả về một **list**, không phải một số. Mỗi
# lớp tự tạo list riêng của phần con, rồi ghép lại bằng `+`:

# %%
def dem_nguoc_thanh_list(n):
    if n == 0:                                  # Base Case
        return []
    return [n] + dem_nguoc_thanh_list(n - 1)     # Recursive Step


print(dem_nguoc_thanh_list(3))   # [3, 2, 1]

# %% [markdown]
# Vết chạy `dem_nguoc_thanh_list(3)`:
#
# | Lớp | Lệnh gọi | Trả về |
# |---|---|---|
# | 0 | `dem_nguoc_thanh_list(3)` | `[3] + dem_nguoc_thanh_list(2)` |
# | 1 | `dem_nguoc_thanh_list(2)` | `[2] + dem_nguoc_thanh_list(1)` |
# | 2 | `dem_nguoc_thanh_list(1)` | `[1] + dem_nguoc_thanh_list(0)` |
# | 3 | `dem_nguoc_thanh_list(0)` | `[]`, chạm điều kiện dừng |
# | 2 | (tiếp) | `[1] + [] = [1]` |
# | 1 | (tiếp) | `[2] + [1] = [2, 1]` |
# | 0 | (tiếp) | `[3] + [2, 1] = [3, 2, 1]` |
#
# Lỗi thường gặp: quên điều kiện dừng, hoặc điều kiện dừng không bao giờ đạt
# tới, làm hàm gọi vô hạn, Python báo `RecursionError: maximum recursion depth
# exceeded`. Bước đệ quy không thực sự thu hẹp bài toán (gọi lại với đúng tham
# số cũ) cũng dẫn tới lặp vô hạn dù có điều kiện dừng. Đệ quy không luôn nhanh
# hơn vòng lặp — nó tốn thêm bộ nhớ cho Call Stack, chỉ đáng dùng khi bài toán
# tự nhiên có cấu trúc chia nhỏ giống hệt nhau.
#
# Tháp Hà Nội cần một dạng nữa: **hai** lời gọi đệ quy trong cùng một thân hàm,
# nối kết quả lại bằng `+`. Bài mẫu cùng khuôn đó, đơn giản hơn — không có cột
# nào để theo dõi, chỉ đếm xuống rồi đếm lên:

# %%
def de_quy_hai_nhanh(n):
    if n == 0:                                            # Base Case
        return [0]
    return de_quy_hai_nhanh(n - 1) + [n] + de_quy_hai_nhanh(n - 1)  # 2 loi goi de quy


print(de_quy_hai_nhanh(2))   # [0, 1, 0, 2, 0, 1, 0]

# %% [markdown]
# `de_quy_hai_nhanh(2)` gọi `de_quy_hai_nhanh(1)` hai lần độc lập (mỗi lần tự
# tính lại từ đầu), chèn `[2]` vào giữa hai kết quả đó. Tháp Hà Nội có cùng
# khuôn: chuyển `(so_dia - 1)` đĩa, ghi 1 bước, chuyển `(so_dia - 1)` đĩa —
# chỉ khác hai lời gọi dùng tham số cột xoay khác nhau, không phải cùng
# `n - 1` như ví dụ trên.
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
# ## Bài 2 — Merge Sort
#
# Bài 1 vừa đếm: hai vòng lồng nhau (`O(n²)`) tốn `n²` phép. Một thuật toán sắp
# xếp kiểu "quét tìm nhỏ nhất, lặp lại" cũng tốn cỡ `n²` phép so sánh — 8 vật
# cản tốn khoảng 64 phép, 1.000 vật cản tốn khoảng một triệu phép.
#
# Merge Sort giảm việc đó xuống `O(n log n)`: chia mảng làm đôi, đệ quy sắp
# từng nửa, rồi trộn (merge) hai nửa đã sắp lại thành một mảng sắp xếp hoàn
# chỉnh.
#
# ```python
# def merge_sort(ds):
#     if len(ds) <= 1:                 # điều kiện dừng
#         return ds
#     giua = len(ds) // 2
#     trai = merge_sort(ds[:giua])     # đệ quy nửa trái
#     phai = merge_sort(ds[giua:])     # đệ quy nửa phải
#     return tron(trai, phai)          # trộn hai nửa đã sắp
# ```
#
# `tron` là phần việc chính: ghép hai list **đã sắp xếp** thành một list sắp
# xếp, bằng cách luôn lấy phần tử nhỏ hơn giữa hai đầu list.

# %%
def tron(trai, phai):
    ket_qua = []
    i = j = 0
    while i < len(trai) and j < len(phai):
        if trai[i] <= phai[j]:
            ket_qua.append(trai[i])
            i += 1
        else:
            ket_qua.append(phai[j])
            j += 1
    ket_qua.extend(trai[i:])   # con du lai ben nao thi noi thang vao cuoi
    ket_qua.extend(phai[j:])
    return ket_qua


print(tron([2, 5], [1, 8]))   # [1, 2, 5, 8]

# %% [markdown]
# Đọc kết quả: `tron` so sánh `2` với `1`, lấy `1` (nhỏ hơn); so `2` với `8`,
# lấy `2`; so `5` với `8`, lấy `5`; hết phần tử ở `trai`, nối thẳng phần còn
# lại của `phai` (`[8]`) vào cuối.
#
# Ghép `tron` vào `merge_sort`:

# %%
def merge_sort(ds):
    if len(ds) <= 1:                 # điều kiện dừng
        return ds
    giua = len(ds) // 2
    trai = merge_sort(ds[:giua])     # đệ quy nửa trái
    phai = merge_sort(ds[giua:])     # đệ quy nửa phải
    return tron(trai, phai)          # trộn hai nửa đã sắp


so_goc = [5, 2, 8, 1]
so_da_sap = merge_sort(so_goc)
print(so_da_sap)   # [1, 2, 5, 8]
print(so_goc)      # [5, 2, 8, 1] - khong doi

# %% [markdown]
# Tính chất của Merge Sort:
#
# 1. `tron(a, b)` chỉ cho kết quả đúng khi cả `a` và `b` đã sắp xếp — đây là lý
#    do phải đệ quy sắp từng nửa trước, không thể `tron` hai nửa còn lộn xộn.
# 2. `merge_sort` trả về list mới, list gốc không đổi (`so_goc` vẫn giữ thứ tự
#    ban đầu ở ví dụ trên).
# 3. List 0 hoặc 1 phần tử đã tự nó là "đã sắp xếp" — đó là điều kiện dừng,
#    thiếu nó thì `giua = len(ds) // 2` chia mãi không bao giờ dừng.
# 4. Chia đôi liên tiếp `n` phần tử thì sau `log2(n)` lần chia còn lại 1 phần
#    tử. `1.000` phần tử chỉ cần chia khoảng 10 lần.
# 5. Trong `tron`, điều kiện `trai[i] <= phai[j]` (không phải `<`) lấy phần tử
#    bên trái trước khi hai bên bằng nhau — giữ đúng thứ tự cũ giữa các phần
#    tử bằng nhau.
#
# Vết chạy `merge_sort([5, 2, 8, 1])`:
#
# | Lớp | Lệnh gọi | Trả về |
# |---|---|---|
# | 0 | `merge_sort([5,2,8,1])` | chia thành `[5,2]` và `[8,1]` |
# | 1 | `merge_sort([5,2])` | chia thành `[5]` và `[2]` |
# | 2 | `merge_sort([5])` | `[5]`, chạm điều kiện dừng |
# | 2 | `merge_sort([2])` | `[2]`, chạm điều kiện dừng |
# | 1 | `tron([5], [2])` | `[2, 5]` |
# | 1 | `merge_sort([8,1])` | chia thành `[8]` và `[1]`, `tron` lại thành `[1, 8]` |
# | 0 | `tron([2,5], [1,8])` | `[1, 2, 5, 8]` |
#
# Lỗi thường gặp: quên điều kiện dừng (`len(ds) <= 1`) làm mảng 0 hoặc 1 phần
# tử vẫn bị chia tiếp, không bao giờ dừng — vi phạm tính chất 3. Merge hai nửa
# sai thứ tự (quên so sánh `trai[i]` với `phai[j]` trước khi lấy ra) làm kết
# quả không thực sự sắp xếp — vi phạm tính chất 1.
#
# ### Bài tập 2.1 — Sắp xếp mảng vật cản (Merge Sort)
#
# Viết hàm `sap_xep_vat_can(danh_sach)` bằng Merge Sort. `danh_sach` là một
# `list` các `dict`, mỗi phần tử có khoá `"ten"` và `"khoang_cach"`. Trả về list
# mới đã sắp xếp theo `"khoang_cach"` tăng dần (vật cản gần nhất lên đầu).
#
# Bài mẫu vừa sắp một list **số** thuần. Bài tập thêm đúng một biến số: phần tử
# giờ là `dict`, nên chỗ so sánh trong `tron` đổi từ `trai[i] <= phai[j]` thành
# `trai[i]["khoang_cach"] <= phai[j]["khoang_cach"]`. Điều kiện dừng và cách
# chia đôi giữ nguyên như bài mẫu.

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
# ---
# ## Tìm kiếm tuyến tính & nhị phân
#
# Tìm kiếm tuyến tính: duyệt từng phần tử, `O(n)` — luôn chạy được, không cần
# mảng đã sắp xếp.
#
# Tìm kiếm nhị phân chỉ áp dụng được trên mảng **đã sắp xếp**. Mỗi bước so
# `target` với phần tử giữa (`mid`), rồi bỏ hẳn một nửa mảng còn lại — không
# quét tiếp nửa đó nữa:
#
# ```python
# left, right = 0, len(ds) - 1
# while left <= right:
#     mid = (left + right) // 2        # // bat buoc: / cho float, sai chi so
#     if ds[mid] == target:
#         ... tim thay tai mid ...
#     elif ds[mid] < target:
#         left = mid + 1               # bo nua trai, target o nua phai
#     else:
#         right = mid - 1              # bo nua phai, target o nua trai
# ```

# %%
def co_ton_tai(ds, target):
    left, right = 0, len(ds) - 1
    while left <= right:
        mid = (left + right) // 2
        if ds[mid] == target:
            return True
        elif ds[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return False


telemetry_logs = [100, 150, 200, 250, 300, 350, 400]
print(co_ton_tai(telemetry_logs, 400))   # True
print(co_ton_tai(telemetry_logs, 999))   # False

# %% [markdown]
# Vết chạy `co_ton_tai(telemetry_logs, 400)`:
#
# | Bước | `left` | `right` | `mid` | `ds[mid]` | So với `400` | Việc |
# |---|---|---|---|---|---|---|
# | 1 | 0 | 6 | 3 | 250 | nhỏ hơn | bỏ nửa trái: `left = 4` |
# | 2 | 4 | 6 | 5 | 350 | nhỏ hơn | bỏ nửa trái: `left = 6` |
# | 3 | 6 | 6 | 6 | 400 | bằng | trả về `True` |
#
# Với `target = 999`, ba bước đầu giống hệt bảng trên (mọi phần tử đều nhỏ
# hơn `999`), rồi `left = 7 > right = 6` — vòng `while` dừng, trả về `False`.
# Không tìm thấy không phải vì hết cách so sánh, mà vì `left` vượt qua `right`.
#
# Tính chất của Tìm kiếm nhị phân: dùng trên mảng chưa sắp xếp cho kết quả sai
# mà không báo lỗi gì — thuật toán vẫn chạy hết, chỉ là chạy sai. Công thức
# `mid` bắt buộc dùng `//`, dùng `/` cho ra `float`, không dùng được làm chỉ
# số. Mỗi bước loại đúng một nửa mảng còn lại, nên đây là `O(log n)`.
#
# ### Bài tập 2.2 — Tìm kiếm nhị phân trong log
#
# Viết hàm `binary_search_log(log_timestamps, target_time)`. Khác bài mẫu
# `co_ton_tai` ở một điểm: trả về **chỉ số** (`mid`) nếu tìm thấy, không phải
# `True`; và trả về `-1` nếu không tìm thấy, không phải `False`. Toàn bộ phần
# `while`, cách cập nhật `left`/`right` giữ nguyên như bài mẫu.

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
# Hàm băm (Hash Function) biến một khoá thành một số nguyên, rồi chia dư cho
# kích thước bảng để xác định "ngăn" lưu trữ.

# %%
def ham_bam_don_gian(khoa, kich_thuoc_bang):
    tong_ma_ascii = sum(ord(ky_tu) for ky_tu in str(khoa))
    return tong_ma_ascii % kich_thuoc_bang


kich_thuoc = 10
print(f"Module A luu o ngan so: {ham_bam_don_gian('AA:BB:CC:DD:EE:01', kich_thuoc)}")
print(f"Module B luu o ngan so: {ham_bam_don_gian('AA:BB:CC:DD:EE:02', kich_thuoc)}")

# %% [markdown]
# Xung đột (Collision) xảy ra khi hai khoá khác nhau bị hàm băm trả về cùng
# một ngăn. Bảng càng nhỏ, xung đột càng dễ xảy ra. Chaining giải quyết xung
# đột: mỗi ngăn không lưu 1 giá trị, mà lưu một `list` các cặp `(khoá, giá
# trị)`; tra cứu thì duyệt list đó để tìm đúng khoá.

# %%
bang_4_ngan = [[] for _ in range(4)]   # 4 ngan, moi ngan la 1 list rong

for khoa, gia_tri in [("camera", 2), ("dong_co", 5), ("gps", 3)]:
    ngan = ham_bam_don_gian(khoa, 4)
    bang_4_ngan[ngan].append((khoa, gia_tri))

print(bang_4_ngan)

# %% [markdown]
# Vết chạy (kích thước bảng = 4):
#
# | Khoá | `ham_bam_don_gian(khoa, 4)` | Ngăn sau khi thêm |
# |---|---|---|
# | `"camera"` | 1 | ngăn 1: `[("camera", 2)]` |
# | `"dong_co"` | 1 | ngăn 1: `[("camera", 2), ("dong_co", 5)]` — xung đột, chaining nối thêm |
# | `"gps"` | 2 | ngăn 2: `[("gps", 3)]` |
#
# `"camera"` và `"dong_co"` cùng rơi vào ngăn 1. Nhờ ngăn lưu một `list`, cả
# hai vẫn giữ được — tra `"camera"` phải duyệt từng cặp trong ngăn 1 tìm đúng
# khoá, không thể chỉ lấy phần tử đầu tiên.
#
# Bài mẫu: `insert`/`get` cho bảng băm chỉ nhận khoá chuỗi, chưa có xoá.

# %%
class BangBamNho:
    def __init__(self, kich_thuoc=4):
        self.kich_thuoc = kich_thuoc
        self.bang = [[] for _ in range(kich_thuoc)]

    def _bam(self, khoa):
        return sum(ord(ky_tu) for ky_tu in khoa) % self.kich_thuoc

    def insert(self, khoa, gia_tri):
        ngan = self.bang[self._bam(khoa)]
        for i, (k, v) in enumerate(ngan):
            if k == khoa:
                ngan[i] = (khoa, gia_tri)   # khoa da co - ghi de
                return
        ngan.append((khoa, gia_tri))        # khoa moi - them vao ngan

    def get(self, khoa):
        ngan = self.bang[self._bam(khoa)]
        for k, v in ngan:
            if k == khoa:
                return v
        return None


bb_nho = BangBamNho()
bb_nho.insert("camera", 2)
bb_nho.insert("dong_co", 5)
bb_nho.insert("camera", 99)   # ghi de, khong tao ban ghi thu 2
print(bb_nho.get("camera"))   # 99
print(bb_nho.get("dong_co"))  # 5
print(bb_nho.get("gps"))      # None - chua tung insert

# %% [markdown]
# Lỗi thường gặp: bỏ qua xử lý xung đột, coi như mỗi ngăn chỉ chứa được 1 giá
# trị — khoá đến sau ghi đè mất khoá đến trước dù chúng là hai khoá khác nhau.
# `insert` cùng một khoá 2 lần mà không kiểm tra khoá đã tồn tại trong ngăn thì
# tạo ra 2 bản ghi trùng, thay vì cập nhật bản ghi cũ (đúng việc `BangBamNho`
# vừa làm ở dòng `if k == khoa`). Hàm băm quên chia dư (`% kich_thuoc_bang`)
# cho ra chỉ số vượt quá kích thước bảng, `self.bang[...]` báo `IndexError`.
#
# ### Dự án 4 — Bảng băm tự cài đặt
#
# Không dùng `dict` có sẵn của Python. Viết class `BangBam`, cùng khuôn với
# `BangBamNho` ở trên, thêm đúng một phương thức mới — `delete`:
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
