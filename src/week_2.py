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
# # Tuần 2 — Hàm, vòng lặp & cấu trúc dữ liệu cơ bản
#
# **Mục tiêu sau tuần này, bạn phải làm được:**
#
# 1. Đóng gói code thành hàm, hiểu phạm vi biến (scope) và tham số mặc định.
# 2. Duyệt và lọc dữ liệu bằng `for` / `while`, dùng đúng `break` / `continue`.
# 3. Thao tác thành thạo `list`, `dict`, `set` — ba cấu trúc dữ liệu dùng nhiều nhất.

# %%
# Ô thiết lập - chạy đầu tiên, mỗi lần mở notebook.
import os
import sys
import urllib.request

REPO_RAW = "https://raw.githubusercontent.com/dongthethang2k15kkk/AI-for-Automotive-Course-v2/main"

if not os.path.isdir("tests"):
    os.makedirs("tests", exist_ok=True)
    open(os.path.join("tests", "__init__.py"), "w").close()
    for ten_file in ("runner.py", "test_week2.py"):
        urllib.request.urlretrieve(
            f"{REPO_RAW}/tests/{ten_file}", os.path.join("tests", ten_file)
        )

if os.getcwd() not in sys.path:
    sys.path.insert(0, os.getcwd())

from tests.test_week2 import (
    kiem_tra_1_1,
    kiem_tra_1_2,
    kiem_tra_2_1,
    kiem_tra_2_2,
    kiem_tra_3_1,
    kiem_tra_3_2,
    kiem_tra_3_3,
    kiem_tra_du_an,
)

print("Moi truong san sang. Phien ban Python:", sys.version.split()[0])

# %% [markdown]
# ---
# ## Bài 1 — Hàm (Functions) và phạm vi biến (Scope)
#
# `def` và `return` đã dùng ở tuần 1. Bài này thêm hai thứ: tham số mặc định, và
# quy tắc biến nào sống ở đâu.
#
# ```python
# def ten_ham(tham_so_1, tham_so_2=gia_tri_mac_dinh):
#     ... xử lý ...
#     return ket_qua
# ```
#
# **Phạm vi biến (scope):** biến khai báo *bên trong* hàm là biến cục bộ (local) —
# chỉ tồn tại trong lúc hàm chạy, không ảnh hưởng ra ngoài. Biến khai báo bên ngoài
# hàm là biến toàn cục (global). Một hàm đọc được biến toàn cục, nhưng muốn *gán lại*
# nó thì phải khai báo `global ten_bien`, cách này nên tránh, vì code phụ thuộc
# biến toàn cục rất khó debug.
#
# **Tham số mặc định** cho phép gọi hàm mà không cần truyền đủ mọi tham số.

# %%
def tinh_goc_danh_lai(do_lech_lan, goc_co_ban=0):
    he_so_hieu_chinh = 1.5
    return goc_co_ban + do_lech_lan * he_so_hieu_chinh


print(tinh_goc_danh_lai(10))        # dùng goc_co_ban mặc định = 0
print(tinh_goc_danh_lai(10, 5))     # truyền đủ 2 tham số
print(tinh_goc_danh_lai(do_lech_lan=-5))  # gọi bằng keyword argument

# %% [markdown]
# Đọc kết quả: lệnh đầu không truyền `goc_co_ban` nên dùng mặc định `0`, ra
# `0 + 10*1.5 = 15.0`. Lệnh hai truyền `goc_co_ban=5`, ra `5 + 10*1.5 = 20.0`. Lệnh
# ba gọi bằng `do_lech_lan=-5` (keyword argument — gọi kèm tên tham số, không cần
# đúng thứ tự khai báo), `goc_co_ban` vẫn dùng mặc định `0`, ra `0 + (-5)*1.5 = -7.5`.
#
# Tính chất của tham số mặc định:
#
# 1. Không truyền tham số có mặc định thì hàm tự lấy giá trị mặc định. Truyền vào
#    thì giá trị truyền đè lên mặc định, không cộng dồn.
# 2. Tham số có mặc định phải đứng sau tham số không có mặc định trong `def`. Viết
#    ngược thứ tự báo `SyntaxError` ngay khi định nghĩa hàm, chưa cần gọi.
# 3. Giá trị mặc định được tạo **đúng một lần**, ngay lúc Python đọc dòng `def`,
#    không tạo lại mỗi lần gọi hàm.
# 4. Hệ quả của tính chất 3: nếu mặc định là `list`/`dict` (`ds=[]`), mọi lần gọi
#    không truyền `ds` đều dùng chung **một** list đó. Sửa bằng cách đặt mặc định
#    là `None`, rồi tạo list mới bên trong hàm.

# %%
def them_loi(item, ds=[]):        # BAY: list rong nay chi tao 1 lan duy nhat
    ds.append(item)
    return ds


print(them_loi("a"))  # ['a']
print(them_loi("b"))  # ['a', 'b']  <- bug: hai lan goi doc lap nhung dung chung 1 list


def them_dung(item, ds=None):     # sua: mac dinh la None, tao list moi ben trong
    if ds is None:
        ds = []
    ds.append(item)
    return ds


print(them_dung("a"))  # ['a']
print(them_dung("b"))  # ['b']  <- dung, doc lap moi lan goi

# %% [markdown]
# Phạm vi biến (scope) qua ba mốc — theo dõi `so_du` khi hàm `rut_tien` chạy:
#
# | Mốc | `so_du` (ngoài hàm) | Đang diễn ra |
# |---|---|---|
# | 1 | `1000` | trước khi gọi `rut_tien(1000, 200)` |
# | 2 | `1000` (không đổi) | bên trong hàm, tham số `so_du` cục bộ = `1000`, tính `so_du - so_tien = 800`, `return 800` |
# | 3 | `1000` (vẫn không đổi) | sau khi gọi xong; kết quả `800` chỉ tồn tại nếu được gán lại: `so_du = rut_tien(so_du, 200)` |
#
# Biến `so_du` bên trong hàm và `so_du` bên ngoài hàm là hai biến khác nhau, dù
# trùng tên. Gán lại bên trong hàm không đụng tới biến bên ngoài.

# %%
def rut_tien(so_du, so_tien):
    so_du = so_du - so_tien   # day la so_du CUC BO, rieng voi so_du ben ngoai
    return so_du


so_du = 1000
ket_qua = rut_tien(so_du, 200)
print("so_du ben ngoai sau khi goi ham:", so_du)   # 1000 - khong doi
print("gia tri ham tra ve:", ket_qua)              # 800

# %% [markdown]
# ### Bài tập 1.1 — Áp dụng giảm giá
#
# Viết hàm `ap_dung_giam_gia(gia_goc, phan_tram=0)` trả về giá sau khi giảm,
# **làm tròn 2 chữ số**. Nếu không truyền `phan_tram`, mặc định không giảm giá.

# %%
def ap_dung_giam_gia(gia_goc, phan_tram=0):
    # TODO: trả về gia_goc sau khi trừ phan_tram %, làm tròn 2 chữ số
    pass


# %%
kiem_tra_1_1(ap_dung_giam_gia)

# %% [markdown]
# ### Bài tập 1.2 — Nhân vật nhận sát thương
#
# Viết hàm `nhan_sat_thuong(mau_hien_tai, sat_thuong)` trả về lượng máu còn lại sau
# khi bị trừ sát thương. Máu **không được xuống dưới 0**.

# %%
def nhan_sat_thuong(mau_hien_tai, sat_thuong):
    # TODO: trừ sát thương, không cho kết quả âm
    pass


# %%
kiem_tra_1_2(nhan_sat_thuong)

# %% [markdown]
# ---
# ## Bài 2 — Chuỗi tuần tự (Sequences) và vòng lặp
#
# `ds[i]` truy cập theo chỉ số, bắt đầu từ `0`. Chỉ số âm đếm từ cuối lên: `ds[-1]`
# là phần tử cuối, `ds[-2]` là phần tử áp chót.
#
# `ds[start:stop:step]` cắt lát, trả về list mới, không đổi `ds` gốc:
#
# 1. Lấy từ chỉ số `start` đến `stop - 1`, không lấy tới `stop`.
# 2. `len(ds[a:b])` bằng đúng `b - a`.
# 3. Bỏ trống `start` là lấy từ đầu, bỏ trống `stop` là lấy tới cuối: `ds[:3]`,
#    `ds[-3:]`.
# 4. `step` âm đảo chiều duyệt: `ds[::-1]` đảo ngược toàn bộ list.

# %%
lidar_readings = [5.2, 3.1, 0.8, 4.5, 1.2, 0.3]

print("Gia tri cuoi:", lidar_readings[-1])                        # 0.3
print("Ba gia tri cuoi:", lidar_readings[-3:])                    # [4.5, 1.2, 0.3]
print("Dao nguoc thu tu:", lidar_readings[::-1])
print("So phan tu cua lat cat [1:4]:", len(lidar_readings[1:4]))  # 3 = 4 - 1

# %% [markdown]
# `for` duyệt qua từng phần tử của list, không cần biết chỉ số. `.append()` thêm
# một phần tử vào cuối list.

# %%
canh_bao = []

for khoang_cach in lidar_readings:
    if khoang_cach < 1.0:
        print(f"Nguy hiem! Vat can o {khoang_cach} m")
        canh_bao.append(khoang_cach)

print("Cac khoang cach can chu y:", canh_bao)

# %% [markdown]
# `while` lặp theo điều kiện, không theo số phần tử — phải tự cập nhật biến điều
# kiện bên trong vòng lặp, thiếu bước này thì lặp vô hạn.
#
# `break` thoát hẳn vòng lặp ngay lập tức, không chạy nốt các lượt còn lại dù điều
# kiện `while` vẫn đúng. `continue` chỉ bỏ qua phần còn lại của lượt hiện tại,
# vòng lặp vẫn tiếp tục ở lượt sau.

# %%
pin = 100
buoc = 0

while pin > 0:
    buoc += 1
    pin -= 15
    if pin == 40:
        print(f"Buoc {buoc}: pin con {pin}%, bo qua canh bao rieng")
        continue
    if pin <= 10:
        print(f"Buoc {buoc}: pin con {pin}%, DUNG KHAN CAP")
        break
    print(f"Buoc {buoc}: pin con {pin}%")

# %% [markdown]
# Vết chạy, bắt đầu `pin = 100`:
#
# | Bước | `pin` sau `-= 15` | So điều kiện | Việc |
# |---|---|---|---|
# | 1 | 85 | khác 40, > 10 | in dòng cuối |
# | 2 | 70 | khác 40, > 10 | in dòng cuối |
# | 3 | 55 | khác 40, > 10 | in dòng cuối |
# | 4 | 40 | bằng 40 | in rồi `continue` — bỏ qua dòng in cuối, sang bước 5 |
# | 5 | 25 | khác 40, > 10 | in dòng cuối |
# | 6 | 10 | <= 10 | in rồi `break` — dừng hẳn |
#
# Vòng lặp dừng ở bước 6 dù `pin > 0` vẫn đúng (`10 > 0`): `break` cắt ngang, không
# chờ điều kiện `while` sai.
#
# Lỗi thường gặp: dùng `range(len(ds))` để lấy chỉ số thì vòng chạy từ `0` đến
# `len(ds) - 1`, không tới `len(ds)` (đúng tính chất 1 ở trên). Xoá hoặc thêm phần
# tử của chính list đang duyệt bằng `for` làm chỉ số bị lệch, bỏ sót hoặc lặp lại
# phần tử — muốn lọc thì tạo list mới như `canh_bao` ở trên, không sửa list gốc.
# Quên cập nhật biến điều kiện trong `while` (quên dòng `pin -= 15`) gây lặp vô
# hạn, Colab treo, bấm nút dừng cạnh nút Run để ngắt.
#
# ### List comprehension
#
# Khi thân vòng `for` chỉ là "lọc và giữ lại", list comprehension viết gọn cả
# vòng lặp lẫn `.append()` vào một dòng. Chỉ thay được `for` theo nghĩa này —
# thân vòng có nhánh rẽ phức tạp hoặc có tác dụng phụ như `print` thì viết `for`
# bình thường, không gượng ép vào comprehension.

# %%
# Cách viết dài
ket_qua_dai = []
for x in lidar_readings:
    if x < 1.0:
        ket_qua_dai.append(x)

# Cách viết Pythonic - list comprehension
ket_qua_gon = [x for x in lidar_readings if x < 1.0]

print(ket_qua_dai == ket_qua_gon, ket_qua_gon)

# %% [markdown]
# Mỗi ký tự có một mã số theo bảng ASCII. `ord(c)` trả về mã số của ký tự `c`,
# `chr(n)` làm ngược lại — trả về ký tự ứng với mã số `n`. `c.isalpha()` kiểm tra
# `c` có phải chữ cái, `c.isupper()` kiểm tra `c` có phải chữ hoa.

# %%
print(ord("a"), ord("A"))       # 97 65
print(chr(98), chr(66))         # 'b' 'B'
print("A".isalpha(), "5".isalpha())   # True False
print("A".isupper(), "a".isupper())   # True False

# %% [markdown]
# ### Bài tập 2.1 — Mã hoá Caesar
#
# Mã hoá Caesar dịch mỗi chữ cái đi một số vị trí cố định trong bảng chữ cái, vòng
# lại từ đầu nếu vượt quá `z`. Trước khi viết hàm đầy đủ, dịch thử một ký tự
# thường bằng công thức số học, không cần `if`:

# %%
def dich_ky_tu_thuong(c, dich_chuyen):
    return chr((ord(c) - ord("a") + dich_chuyen) % 26 + ord("a"))


print(dich_ky_tu_thuong("a", 3))   # 'd'
print(dich_ky_tu_thuong("y", 3))   # 'b' - vong qua tu z ve a

# %% [markdown]
# Đọc công thức: `ord(c) - ord("a")` đưa `c` về vị trí `0`-`25` trong bảng chữ cái
# (`a` là `0`, `z` là `25`), không phụ thuộc mã ASCII gốc. Cộng `dich_chuyen` rồi
# `% 26` để vòng lại nếu vượt quá `25`. Cộng lại `ord("a")` để quay về đúng mã ký
# tự thường.
#
# Vết chạy với `c = "y"`, `dich_chuyen = 3`:
#
# | Biểu thức | Kết quả |
# |---|---|
# | `ord("y")` | `121` |
# | `121 - ord("a")` | `121 - 97 = 24` |
# | `24 + 3` | `27` |
# | `27 % 26` | `1` |
# | `1 + ord("a")` | `1 + 97 = 98` |
# | `chr(98)` | `"b"` |
#
# `27 % 26` cho `1` thay vì `27` — đây chính là bước vòng lại từ `z` (vị trí `25`)
# về `a` (vị trí `0`).
#
# Ghép công thức trên vào một vòng `for` để dịch cả chuỗi, với điều kiện đơn giản
# nhất: chuỗi chỉ toàn chữ thường, không số, không dấu câu.

# %%
def dich_chuoi_thuong(van_ban, dich_chuyen):
    ket_qua = ""
    for c in van_ban:
        ket_qua += dich_ky_tu_thuong(c, dich_chuyen)
    return ket_qua


print(dich_chuoi_thuong("hello", 3))   # 'khoor'
print(dich_chuoi_thuong("xyz", 3))     # 'abc'

# %% [markdown]
# Viết hàm `ma_hoa_caesar(van_ban, dich_chuyen)` làm đúng việc `dich_chuoi_thuong`
# vừa làm, cộng thêm hai việc:
#
# 1. Ký tự không phải chữ cái (số, dấu câu, khoảng trắng) giữ nguyên, không dịch.
#    Dùng `c.isalpha()` để kiểm tra trước khi dịch.
# 2. Chữ hoa dịch bằng đúng công thức trên nhưng thay `ord("a")` bằng `ord("A")`,
#    dùng `c.isupper()` để biết ký tự đang xét là hoa hay thường.
#
# Ví dụ: `ma_hoa_caesar("Hello, World!", 3)` → `"Khoor, Zruog!"`.

# %%
def ma_hoa_caesar(van_ban, dich_chuyen):
    # TODO: dịch từng chữ cái, giữ nguyên ký tự không phải chữ cái
    pass


# %%
kiem_tra_2_1(ma_hoa_caesar)

# %% [markdown]
# ### Bài tập 2.2 — Lọc vật cản gần
#
# Viết hàm `loc_vat_can_gan(khoang_cach, nguong=1.0)` trả về **list** các giá trị
# trong `khoang_cach` **nhỏ hơn** `nguong` (giữ nguyên thứ tự xuất hiện).

# %%
def loc_vat_can_gan(khoang_cach, nguong=1.0):
    # TODO: trả về list các phần tử nhỏ hơn nguong
    pass


# %%
kiem_tra_2_2(loc_vat_can_gan)

# %% [markdown]
# ---
# ## Bài 3 — Dictionary, Set & Dự án 1
#
# Dictionary lưu theo cặp khóa-giá trị: `config["khoa"]`. Duyệt bằng `.keys()`,
# `.values()`, `.items()`. `.get(khoa, mac_dinh)` tránh lỗi `KeyError` khi khóa có
# thể không tồn tại. `.update(dict_khac)` gộp thêm/ghi đè.
#
# Set là tập hợp không trùng lặp, không có thứ tự. Phép toán: `|` (hợp), `&`
# (giao), `-` (hiệu), và `.issubset()` kiểm tra tập con.
#
# `{}` là dict rỗng, không phải set rỗng — set rỗng phải viết `set()`.

# %%
cau_hinh_xe = {
    "toc_do_toi_da": 40,
    "do_phan_giai_camera": "1080p",
    "pid_lai": [0.1, 0.01, 0.5],
}
cam_bien_dang_bat = {"lidar", "sieu_am", "camera"}

cau_hinh_xe["toc_do_toi_da"] = 30
print(f"Do phan giai camera: {cau_hinh_xe['do_phan_giai_camera']}")
print(f"Cam bien dang bat: {cam_bien_dang_bat}")

cam_bien_yeu_cau = {"lidar", "gps"}
print("Cam bien con thieu:", cam_bien_yeu_cau - cam_bien_dang_bat)

# %% [markdown]
# Tính chất của `dict` và `set`:
#
# 1. `config["khoa"]` với khoá không tồn tại ném `KeyError`. `config.get("khoa",
#    mac_dinh)` trả về `mac_dinh` thay vì báo lỗi.
# 2. `{}` luôn là dict rỗng, kể cả khi định gán cho một set. Set rỗng phải viết
#    `set()`.
# 3. Set không giữ thứ tự chèn vào, và không chứa phần tử trùng lặp — thêm cùng
#    một giá trị hai lần thì set chỉ còn lại một.
# 4. Phần tử của set phải bất biến: số, chuỗi, tuple được, nhưng `list` thì không —
#    `{[1, 2]}` ném `TypeError: unhashable type: 'list'`.

# %%
print(cau_hinh_xe.get("mau_son", "chua dat"))   # 'chua dat' - khong KeyError
vi_du_set = {1, 1, 2, 2, 3}
print(vi_du_set)                                # {1, 2, 3} - trung lap tu dong bi loai

# %% [markdown]
# `zip(a, b)` ghép hai list lại theo từng cặp cùng chỉ số, dừng khi list ngắn
# nhất hết phần tử.

# %%
ten_mon = ["Toan", "Ly", "Hoa"]
diem_mon = [8, 9, 10]

for mon, d in zip(ten_mon, diem_mon):
    print(mon, d)

# %% [markdown]
# ### Dict và set comprehension
#
# Cùng cú pháp với list comprehension ở Bài 2, chỉ đổi ngoặc vuông thành ngoặc
# nhọn, dùng khi cần tạo dict/set mới từ một list có sẵn.

# %%
diem_so = [8, 9, 10, 7]
mon_hoc = ["Toan", "Ly", "Hoa", "Van"]

bang_diem = {mon: diem for mon, diem in zip(mon_hoc, diem_so)}
print(bang_diem)

diem_gioi = {mon for mon, diem in bang_diem.items() if diem >= 8}
print("Cac mon dat gioi:", diem_gioi)

# %% [markdown]
# ### Bài tập 3.1 — Lọc phần tử trùng lặp
#
# Trước bài tập, một bài cùng cách nghĩ — "nhớ những giá trị đã gặp" — nhưng khác
# đầu ra: đếm số lần xuất hiện của mỗi phần tử bằng dict.

# %%
def dem_so_lan(ds):
    dem = {}
    for x in ds:
        if x in dem:
            dem[x] += 1
        else:
            dem[x] = 1
    return dem


print(dem_so_lan([1, 2, 2, 3, 1, 4]))   # {1: 2, 2: 2, 3: 1, 4: 1}

# %% [markdown]
# Viết hàm `loc_trung_lap(ds)` trả về một **list** chỉ giữ lần xuất hiện **đầu
# tiên** của mỗi phần tử, theo đúng thứ tự ban đầu. Khác `dem_so_lan` ở chỗ: không
# cần đếm, chỉ cần biết "đã gặp chưa" (`set` tra nhanh hơn `dict` cho việc chỉ hỏi
# có/không), và giữ phần tử vào một list kết quả ngay lần gặp đầu tiên.
#
# Ví dụ: `loc_trung_lap([1, 2, 2, 3, 1, 4])` → `[1, 2, 3, 4]`.

# %%
def loc_trung_lap(ds):
    # TODO: trả về list không trùng lặp, giữ thứ tự xuất hiện đầu tiên
    pass


# %%
kiem_tra_3_1(loc_trung_lap)

# %% [markdown]
# ### Bài tập 3.2 — Hợp nhất cấu hình
#
# Viết hàm `hop_nhat_cau_hinh(mac_dinh, tuy_chinh)` trả về một `dict` mới: bắt đầu
# từ `mac_dinh`, rồi các khóa trong `tuy_chinh` **ghi đè** lên.

# %%
def hop_nhat_cau_hinh(mac_dinh, tuy_chinh):
    # TODO: trả về dict = mac_dinh, ghi đè bởi tuy_chinh
    pass


# %%
kiem_tra_3_2(hop_nhat_cau_hinh)

# %% [markdown]
# ### Bài tập 3.3 — Kiểm tra quyền truy cập
#
# Viết hàm `kiem_tra_quyen_truy_cap(quyen_nguoi_dung, quyen_yeu_cau)` trả về `True`
# nếu `quyen_nguoi_dung` có **đủ tất cả** các quyền trong `quyen_yeu_cau`.
#
# Gợi ý: dùng `.issubset()` hoặc toán tử `<=` giữa hai set.

# %%
def kiem_tra_quyen_truy_cap(quyen_nguoi_dung, quyen_yeu_cau):
    # TODO: trả về True nếu quyen_yeu_cau là tập con của quyen_nguoi_dung
    pass


# %%
kiem_tra_3_3(kiem_tra_quyen_truy_cap)

# %% [markdown]
# ---
# ## Dự án 1 — Bộ quản lý cấu hình người dùng
#
# Ghép bài 3.2 và 3.3 lại: viết hàm
# `quan_ly_cau_hinh(mac_dinh, tuy_chinh, quyen_nguoi_dung, quyen_yeu_cau)`
# trả về một `dict`:
#
# ```python
# {
#     "cau_hinh": ...,   # kết quả hop_nhat_cau_hinh(mac_dinh, tuy_chinh)
#     "duoc_phep": ...,  # kết quả kiem_tra_quyen_truy_cap(quyen_nguoi_dung, quyen_yeu_cau)
# }
# ```
#
# Đây là bài đầu tiên bạn gọi lại chính các hàm mình đã viết ở trên, thay vì chép
# lại logic đã có.

# %%
def quan_ly_cau_hinh(mac_dinh, tuy_chinh, quyen_nguoi_dung, quyen_yeu_cau):
    # TODO: gọi lại hop_nhat_cau_hinh và kiem_tra_quyen_truy_cap, gộp kết quả vào dict
    pass


# %%
kiem_tra_du_an(quan_ly_cau_hinh)

# %% [markdown]
# ---
# ## Tổng kết tuần 2

# %%
ket_qua = [
    kiem_tra_1_1(ap_dung_giam_gia),
    kiem_tra_1_2(nhan_sat_thuong),
    kiem_tra_2_1(ma_hoa_caesar),
    kiem_tra_2_2(loc_vat_can_gan),
    kiem_tra_3_1(loc_trung_lap),
    kiem_tra_3_2(hop_nhat_cau_hinh),
    kiem_tra_3_3(kiem_tra_quyen_truy_cap),
    kiem_tra_du_an(quan_ly_cau_hinh),
]

print(f"\nTONG KET TUAN 2: {sum(ket_qua)}/{len(ket_qua)} bai dat.")

# %% [markdown]
# ### Nộp bài
#
# `File > Save a copy in GitHub`, chọn repo của bạn, đường dẫn `week2/week_2.ipynb`.
