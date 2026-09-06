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
# Hàm là một khối code có tên, nhận đầu vào (tham số), trả về đầu ra (`return`), và
# có thể gọi lại nhiều lần mà không phải chép lại cùng một đoạn code ở nhiều chỗ —
# đúng vấn đề mà tuần 1 gặp phải khi viết bốn khối `if/elif/else` gần giống hệt nhau.
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
# nó thì phải khai báo `global ten_bien` — cách này nên tránh, vì code phụ thuộc
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
# ### Lỗi thường gặp
#
# **1. Tưởng biến trong hàm ảnh hưởng ra ngoài.** Biến cục bộ chết theo hàm, không
# tự động cập nhật ra ngoài.
#
# **2. Tham số mặc định là list/dict.** Đừng bao giờ viết
# `def them(item, ds=[])`. Giá trị mặc định chỉ được tạo **một lần duy nhất** lúc
# định nghĩa hàm, nên mọi lần gọi hàm mà không truyền `ds` sẽ **dùng chung một list**,
# gây lỗi rất khó phát hiện. Cách đúng: dùng `None` làm mặc định, rồi tạo list mới
# bên trong hàm.
#
# **3. Tham số có mặc định phải đứng sau tham số không có mặc định** — viết ngược
# thứ tự sẽ báo lỗi cú pháp ngay.

# %%
# Bẫy tham số mặc định dùng chung - MINH HOẠ LỖI, không nên viết thế này
def them_loi(item, ds=[]):
    ds.append(item)
    return ds


print(them_loi("a"))  # ['a']
print(them_loi("b"))  # ['a', 'b']  <- bug: lẽ ra phải là ['b'] nếu gọi độc lập


# Cách viết đúng
def them_dung(item, ds=None):
    if ds is None:
        ds = []
    ds.append(item)
    return ds


print(them_dung("a"))  # ['a']
print(them_dung("b"))  # ['b']  <- đúng, độc lập mỗi lần gọi

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
# `ds[i]` truy cập theo chỉ số, bắt đầu từ 0. Chỉ số âm đếm từ cuối lên: `ds[-1]`
# là phần tử cuối, `ds[-2]` là phần tử áp chót. `ds[start:stop:step]` cắt lát;
# `ds[-3:]` là ba phần tử cuối, `ds[::-1]` đảo ngược toàn bộ list. `.append()` thêm
# cuối, `.pop()` lấy ra và xoá phần tử cuối, `.remove(x)` xoá theo giá trị.
#
# `for` duyệt qua từng phần tử của một list/string/`range()`. `while` lặp theo
# điều kiện, phải tự cập nhật biến điều kiện để tránh lặp vô hạn.
#
# `break` thoát hẳn vòng lặp. `continue` bỏ qua phần còn lại của lượt lặp hiện
# tại, nhảy sang lượt tiếp theo.

# %%
lidar_readings = [5.2, 3.1, 0.8, 4.5, 1.2, 0.3]
canh_bao = []

for khoang_cach in lidar_readings:
    if khoang_cach < 1.0:
        print(f"Nguy hiem! Vat can o {khoang_cach} m")
        canh_bao.append(khoang_cach)

print("Cac khoang cach can chu y:", canh_bao)
print("Gia tri cuoi:", lidar_readings[-1])
print("Ba gia tri cuoi:", lidar_readings[-3:])
print("Dao nguoc thu tu:", lidar_readings[::-1])

# %% [markdown]
# ### Lỗi thường gặp
#
# **1. Sai chỉ số (off-by-one).** `range(len(ds))` chạy từ `0` đến `len(ds) - 1`,
# không phải đến `len(ds)`.
#
# **2. Sửa list ngay trong lúc đang duyệt nó bằng `for`.** Xoá/thêm phần tử của
# chính list đang duyệt làm chỉ số bị lệch, bỏ sót hoặc lặp lại phần tử. Muốn lọc,
# hãy tạo list mới (như ví dụ trên) thay vì sửa list gốc khi đang duyệt.
#
# **3. Vòng `while` quên cập nhật điều kiện** → lặp vô hạn, Colab bị treo (bấm nút
# dừng để ngắt).
#
# ### List comprehension
#
# Khi logic bên trong vòng `for` chỉ là "lọc và giữ lại", list comprehension viết
# gọn cả vòng lặp lẫn `.append()` vào một dòng.

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
# Viết hàm `ma_hoa_caesar(van_ban, dich_chuyen)`: dịch mỗi chữ cái trong `van_ban`
# đi `dich_chuyen` vị trí trong bảng chữ cái, vòng lại từ đầu nếu vượt quá `z`/`Z`.
# Giữ nguyên hoa/thường, giữ nguyên số và ký tự khác (dấu câu, khoảng trắng).
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
vehicle_config = {
    "toc_do_toi_da": 40,
    "do_phan_giai_camera": "1080p",
    "pid_lai": [0.1, 0.01, 0.5],
}
cam_bien_dang_bat = {"lidar", "sieu_am", "camera"}

vehicle_config["toc_do_toi_da"] = 30
print(f"Do phan giai camera: {vehicle_config['do_phan_giai_camera']}")
print(f"Cam bien dang bat: {cam_bien_dang_bat}")

cam_bien_yeu_cau = {"lidar", "gps"}
print("Cam bien con thieu:", cam_bien_yeu_cau - cam_bien_dang_bat)

# %% [markdown]
# ### Lỗi thường gặp
#
# **1. Truy cập khóa không tồn tại bằng `[]`** → `KeyError`. Dùng
# `config.get("khoa", gia_tri_mac_dinh)` khi không chắc khóa có tồn tại.
#
# **2. Nhầm `{}` là set rỗng.** `{}` luôn là dict. Set rỗng là `set()`.
#
# **3. Tưởng set giữ thứ tự chèn vào.** Set không đảm bảo thứ tự — nếu cần giữ thứ
# tự mà vẫn loại trùng lặp, phải tự viết logic (xem bài tập 3.1), không thể chỉ
# `list(set(ds))`.
#
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
# Viết hàm `loc_trung_lap(ds)` trả về một **list** chỉ giữ lần xuất hiện **đầu
# tiên** của mỗi phần tử, theo đúng thứ tự ban đầu.
#
# Ví dụ: `loc_trung_lap([1, 2, 2, 3, 1, 4])` → `[1, 2, 3, 4]`.
#
# Gợi ý: dùng một `set` để nhớ những giá trị đã gặp, kết hợp một `list` kết quả.

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
# `quan_ly_cau_hinh(config_mac_dinh, config_tuy_chinh, quyen_nguoi_dung, quyen_yeu_cau)`
# trả về một `dict`:
#
# ```python
# {
#     "cau_hinh": ...,   # kết quả hop_nhat_cau_hinh(config_mac_dinh, config_tuy_chinh)
#     "duoc_phep": ...,  # kết quả kiem_tra_quyen_truy_cap(quyen_nguoi_dung, quyen_yeu_cau)
# }
# ```
#
# Đây là bài đầu tiên bạn gọi lại chính các hàm mình đã viết ở trên, thay vì chép
# lại logic đã có.

# %%
def quan_ly_cau_hinh(config_mac_dinh, config_tuy_chinh, quyen_nguoi_dung, quyen_yeu_cau):
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