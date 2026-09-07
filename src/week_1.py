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
# # Tuần 1 — Nền tảng & Cú pháp cơ bản
#
# **Mục tiêu sau tuần này, bạn phải làm được:**
#
# 1. Khai báo biến đúng quy ước và phân biệt 4 kiểu dữ liệu cơ bản.
# 2. Dùng thành thạo toán tử số học và định dạng chuỗi bằng f-string.
# 3. Viết được logic ra quyết định bằng `if / elif / else`.
#
# Đọc phần lý thuyết, chạy ô ví dụ để xem kết quả, rồi làm ô bài tập. Mỗi bài tập có
# một ô kiểm tra ngay bên dưới.
#
# **Quy tắc:** không sửa nội dung các ô kiểm tra. Chỉ viết code vào chỗ có `# TODO`.

# %%
# Ô thiết lập - chạy đầu tiên, mỗi lần mở notebook.
import os
import sys
import urllib.request

REPO_RAW = "https://raw.githubusercontent.com/dongthethang2k15kkk/AI-for-Automotive-Course-v2/main"

if not os.path.isdir("tests"):
    os.makedirs("tests", exist_ok=True)
    open(os.path.join("tests", "__init__.py"), "w").close()
    for ten_file in ("runner.py", "test_week1.py"):
        urllib.request.urlretrieve(
            f"{REPO_RAW}/tests/{ten_file}", os.path.join("tests", ten_file)
        )

if os.getcwd() not in sys.path:
    sys.path.insert(0, os.getcwd())

from tests.test_week1 import (
    kiem_tra_1_1,
    kiem_tra_1_2,
    kiem_tra_2_1,
    kiem_tra_2_2,
    kiem_tra_2_3,
    kiem_tra_3_1,
    kiem_tra_3_2,
    kiem_tra_du_an,
)

print("Moi truong san sang. Phien ban Python:", sys.version.split()[0])

# %% [markdown]
# ---
# ## Bài 1 — Biến và kiểu dữ liệu
#
# Biến là một cái tên gắn với một giá trị trong bộ nhớ. Python không cần khai báo
# kiểu trước, kiểu được suy ra từ giá trị bạn gán.
#
# Bốn kiểu cơ bản dùng nhiều nhất:
#
# | Kiểu | Ý nghĩa | Ví dụ trong hệ thống xe |
# |---|---|---|
# | `int` | số nguyên | `toc_do_dong_co = 120` (vòng/phút) |
# | `float` | số thực | `dien_ap_pin = 11.5` (V) |
# | `str` | chuỗi ký tự | `trang_thai_he_thong = "Dang chay"` |
# | `bool` | đúng/sai | `cam_bien_hoat_dong = True` |
#
# Quy ước đặt tên (PEP 8): biến dùng `snake_case`, viết thường, các từ nối bằng dấu
# gạch dưới. Hằng số viết HOA: `TOC_DO_TOI_DA = 120`.

# %%
# Khai báo các thông số của một hệ thống
toc_do_dong_co = 120               # int
dien_ap_pin = 11.5                 # float
trang_thai_he_thong = "Dang chay"  # str
cam_bien_hoat_dong = True          # bool

TOC_DO_TOI_DA = 150                # hằng số: viết HOA

print(toc_do_dong_co, type(toc_do_dong_co))     # lệnh type() để check kiểu dữ liệu
print(dien_ap_pin, type(dien_ap_pin))
print(trang_thai_he_thong, type(trang_thai_he_thong))
print(cam_bien_hoat_dong, type(cam_bien_hoat_dong))

# %% [markdown]
# Bốn điểm hay gây lỗi ở bài này:
#
# 1. `"10"` và `10` là hai thứ khác nhau. Dữ liệu đọc từ cảm biến hay từ `input()`
#    luôn là chuỗi, phải ép kiểu trước khi tính toán. 
#    VD: Nhập số nguyên từ bàn phím phải ép `int():` `int(input(...))`
# 2. Dùng biến chưa gán thì Python báo `NameError`. Biến phải được gán trước khi dùng.
# 3. Nên đặt tên theo nội dung:
#    `toc_do_xe`, `so_lan_doc_cam_bien`.
# 4. `type(True)` trả về `bool`, không phải `int` — dù trong Python `True == 1`.

# %%
# Chuỗi và số khác nhau như thế nào
gia_tri_tho = "10"           # dữ liệu thô đọc về, luôn là chuỗi
print(gia_tri_tho + "5")     # nối chuỗi -> "105"
print(int(gia_tri_tho) + 5)  # ép kiểu rồi cộng -> 15

# %% [markdown]
# Tính chất ép kiểu:
#
# 1. `int()` và `float()` chỉ chấp nhận chuỗi đúng định dạng số: 
#    * `int("10")` hoạt động vì chuỗi biểu diễn đúng một số nguyên ở hệ cơ số 10.
#    * `float("10.5")` hoạt động vì chuỗi biểu diễn đúng dạng số thực (có tối đa một dấu chấm thập phân).
#
# 2. `int("10.5")` sẽ phát sinh lỗi `ValueError: invalid literal for int() with base 10: '10.5'` do `int()` không xử lý ký tự dấu chấm `.` trong chuỗi. Để lấy phần nguyên từ một chuỗi số thực, phải ép kiểu qua `float()` trước rồi mới ép về `int()` sau: `int(float("10.5"))`.
#
# 3. `int(10.9)` thực hiện **cắt bỏ phần thập phân** (truncation), cho ra `10`. Trong khi đó, `round(10.9)`HOẶC `round(10.9,0)` thực hiện **làm tròn 0 chữ số sau dấu phẩy** theo quy tắc toán học, cho ra `11`.
#
# 4. Thứ tự thực thi và bản chất của toán tử `+`:
#    * `int("10") + int("5")`: Ép hai chuỗi thành hai số nguyên trước, sau đó toán tử `+` thực hiện **phép cộng đại số**, cho ra `15`.
#    * `int("10" + "5")`: Toán tử `+` thực hiện **nối chuỗi** trước thành `"105"`, sau đó `int()`

# %%
print(int("10"), float("10.5"))    # ep duoc vi dung dang so: 10 10.5
print(int(10.9))                   # cat bo phan thap phan, khong lam tron: 10
print(int("10") + int("5"))        # cong hai so da ep: 15
print(int("10" + "5"))             # noi chuoi truoc roi moi ep: 105

# %% [markdown]
# ### Bài tập 1.1 — Điểm trung bình
#
# Có hai bộ điểm ba môn Toán, Lý, Hoá. Với mỗi bộ, gán biến `diem_tb_*` bằng trung
# bình cộng ba môn.

# %%
toan_1, ly_1, hoa_1 = 8, 9, 10
toan_2, ly_2, hoa_2 = 7.5, 6, 8

diem_tb_1 = None  # TODO: trung bình cộng của toan_1, ly_1, hoa_1
diem_tb_2 = None  # TODO: trung bình cộng của toan_2, ly_2, hoa_2

# %%
kiem_tra_1_1(diem_tb_1, diem_tb_2)

# %% [markdown]
# ### Bài tập 1.2 — Ép kiểu dữ liệu
#
# Cho chuỗi `gia_tri_tho_2`. Gán `noi_chuoi` bằng cách nối nó với chuỗi `"5"`, và
# gán `tong_so` bằng cách ép nó sang số nguyên rồi cộng thêm `5`. Xem lại ô ví dụ
# ngay phía trên nếu chưa rõ khác nhau ở đâu.

# %%
gia_tri_tho_2 = "20"

noi_chuoi = None  # TODO: gia_tri_tho_2 nối với "5"
tong_so = None    # TODO: ép gia_tri_tho_2 sang int rồi cộng 5

# %%
kiem_tra_1_2(noi_chuoi, tong_so)

# %% [markdown]
# ---
# ## Bài 2 — Toán tử, chuỗi và ép kiểu
#
# Toán tử số học: `+` cộng, `-` trừ `*` nhân, `/` chia, `//` chia lấy phần nguyên, `%` chia lấy phần dư, `**` lũy thừa(mũ).
#
# - `/` luôn trả về `float`, VD `10 / 2` cho `5.0`.
# - `//`, `%` — hay dùng để chia chu kỳ, đổi đơn vị.
#
# f-string ghép chuỗi bằng cách đặt `f` trước dấu nháy rồi nhúng biểu thức trong
# `{}`. Thay vì Ghép bằng `+`, phải tự gọi `str()` cho từng số;
# f-string tự làm việc đó, nên ngắn hơn và ít lỗi hơn.

# %%
tong_giay = 3725

gio_vd = tong_giay // 3600
phut_vd = (tong_giay % 3600) // 60
giay_vd = tong_giay % 60

print(f"Thoi gian chay: {gio_vd} gio {phut_vd} phut {giay_vd} giay")

# %% [markdown]
# Tính chất của `//` và `%` khi `a`, `b` là số nguyên dương:
#
# 1. `a == (a // b) * b + a % b` luôn đúng: `//` cho thương, `%` cho số dư.
# 2. `a % b` luôn nằm trong khoảng từ `0` đến `b - 1`. Dùng để bắt phần dư sau khi
#    chia hết cho một chu kỳ, ví dụ `gio % 24` luôn ra giờ trong ngày, từ 0 đến 23.
# 3. `//` giữa hai `int` cho `int`. Còn 2 toán hạng trong đó có 1 là `float` thì kết quả cũng là
#    `float`: `7.0 // 2` ra `3.0`.
# 4. Với số âm, `//` làm tròn về phía âm vô cực: `-7 // 2` ra `-4`.

# %%
a, b = 17, 5
print(a // b, a % b, (a // b) * b + a % b)   # 3 2 17 -> cong thuc dung
print(7.0 // 2)                               # 3.0 - float vi co toan hang float
print(-7 // 2)                                # -4 - lam tron ve am vo cuc

# %% [markdown]
# `round(giá trị, số chữ số dc làm tròn đến)` làm tròn *giá trị* của một số. Trong f-string, có thể thay round(,) bằng `{x:.2f}` sẽ cho giá trị gốc của biến không đổi(cũng là làm tròn đến 2 chứ số). Khi đề bài yêu cầu trả về một số đã làm tròn (không phải chỉ in ra), phải dùng `round()`.

# %%
gia_goc = 21.5 / 3

gia_lam_tron = round(gia_goc, 2)         # giá trị thật sự đổi thành 7.17
print(gia_lam_tron, type(gia_lam_tron))

print(f"{gia_goc:.2f}")                  # chỉ đổi cách hiển thị, gia_goc vẫn là 7.1666...
print(gia_goc)

# %% [markdown]
# ### Bài tập 2.1 — Chia hoá đơn
#
# Có hai hoá đơn, mỗi hoá đơn gồm tổng tiền, phần trăm tip, số người chia. Với mỗi
# hoá đơn, gán `moi_nguoi_tra_*`: cộng tip vào tổng tiền, chia đều cho số người, làm
# tròn 2 chữ số bằng `round()`.

# %%
tong_tien_1, phan_tram_tip_1, so_nguoi_1 = 300000, 10, 3
tong_tien_2, phan_tram_tip_2, so_nguoi_2 = 100000, 15, 3

moi_nguoi_tra_1 = None  # TODO: hoá đơn 1
moi_nguoi_tra_2 = None  # TODO: hoá đơn 2

# %%
kiem_tra_2_1(moi_nguoi_tra_1, moi_nguoi_tra_2)

# %% [markdown]
# ### Bài tập 2.2 — Báo cáo quãng đường
#
# Gán `bao_cao` bằng một chuỗi(f-string) đúng theo mẫu:
#
# ```
# Xe đã đi được {quang_duong} mét trong {thoi_gian} giây.
# ```
#
# Trong đó `quang_duong = van_toc_bc * thoi_gian_bc`, không làm tròn. Dấu chấm cuối
# câu và dấu tiếng Việt phải khớp chính xác.

# %%
van_toc_bc, thoi_gian_bc = 20.0, 3

bao_cao = None  # TODO: tính quãng đường rồi gán chuỗi đúng mẫu bằng f-string

# %%
kiem_tra_2_2(bao_cao)

# %% [markdown]
# ### Ô tự do — thử `input()`
#
# Ô này không chấm điểm. Bỏ dấu `#` để chạy thử.

# %%
# tong = float(input("Tong hoa don: "))
# nguoi = int(input("So nguoi: "))
# print(f"Moi nguoi tra {tong / nguoi:.2f}")

# %% [markdown]
# ### Bài tập 2.3 — Đổi giây sang giờ phút giây
#
# Ô ví dụ ở đầu Bài 2 đổi `tong_giay = 3725` sang giờ/phút/giây bằng `//` và `%`.
# Làm lại đúng phép tính đó cho `tong_giay_bt = 5000`, gán vào `gio`, `phut`, `giay`.

# %%
tong_giay_bt = 5000

gio = None   # TODO
phut = None  # TODO
giay = None  # TODO

# %%
kiem_tra_2_3(gio, phut, giay)

# %% [markdown]
# ---
# ## Bài 3 — Boolean và câu lệnh điều kiện
#
# Toán tử so sánh cho ra `True`/`False`: `==` (bằng), `!=` (khác(ko bằng)), `>` , `<` , `>=` (lớn hơn hoặc bằng), `<=` (bé hơn hoặc bằng).
#
# Toán tử logic: `and` (cả hai đúng), `or` (một trong hai đúng), `not` (đảo ngược từ đúng thành sai và ngược lại).
#
# Cấu trúc rẽ nhánh:
#
# ```python
# if dieu_kien_1:
#     ...
# elif dieu_kien_2:
#     ...
# else:
#     ...
# ```
#
# Python dùng thụt lề để xác định khối lệnh, không dùng ngoặc nhọn. Thụt lề sai thì
# Python báo `IndentationError` và dừng chạy. PEP 8 quy định 4 dấu cách cho mỗi cấp
# thụt lề. Ấn TAB để thụt lề đúng.
#
# Các nhánh `if / elif / else` được xét lần lượt từ trên xuống, gặp nhánh đúng đầu
# tiên là dừng — nên thứ tự các nhánh quyết định kết quả.

# %%
khoang_cach = 3.7

if khoang_cach <= 2.0:
    trang_thai_vi_du = "PHANH_KHAN_CAP"
elif khoang_cach <= 5.0:
    trang_thai_vi_du = "GIAM_TOC"
else:
    trang_thai_vi_du = "AN_TOAN"

print(f"Khoang cach {khoang_cach} m -> {trang_thai_vi_du}")

# %% [markdown]
# Bốn điểm hay gây lỗi ở bài này:
#
# 1. Dùng `=` thay cho `==`. `=` là gán, `==` là so sánh. Trong `if` phải dùng `==`.
# 2. Viết nhiều `if` liên tiếp thay vì `elif`. Nhiều `if` đứng riêng sẽ được xét
#    *tất cả*, nên biến kết quả có thể bị nhánh sau ghi đè lên nhánh trước.
# 3. Sai thứ tự nhánh. Nếu đặt `if khoang_cach <= 5.0` lên trước, thì khoảng cách
#    1.5 m cũng rơi vào nhánh đó và không bao giờ chạm tới nhánh khẩn cấp.
# 4. Quên xét giá trị biên. Đề nói "nhỏ hơn hoặc bằng 2.0" thì phải là `<= 2.0`,
#    không phải `< 2.0`. Test luôn kiểm tra đúng chỗ này.

# %% [markdown]
# ### Bài tập 3.1 — Cảnh báo vật cản
#
# Có bốn khoảng cách cho sẵn. Với mỗi khoảng cách, viết một khối `if/elif/else`
# riêng và gán kết quả vào `trang_thai_*` theo bảng:
#
# | Điều kiện | Kết quả |
# |---|---|
# | `khoang_cach <= 2.0` | `"PHANH_KHAN_CAP"` |
# | `khoang_cach <= 5.0` | `"GIAM_TOC"` |
# | còn lại | `"AN_TOAN"` |

# %%
khoang_cach_a = 0.5
khoang_cach_b = 2.0
khoang_cach_c = 5.0
khoang_cach_d = 12.0

# Khởi tạo sẵn để ô kiểm tra chạy được ngay cả khi bạn chưa làm gì.
trang_thai_a = None
trang_thai_b = None
trang_thai_c = None
trang_thai_d = None

# ---------- Trường hợp a: làm sẵn để bạn xem mẫu ----------
if khoang_cach_a <= 2.0:
    trang_thai_a = "PHANH_KHAN_CAP"
elif khoang_cach_a <= 5.0:
    trang_thai_a = "GIAM_TOC"
else:
    trang_thai_a = "AN_TOAN"

# ---------- Trường hợp b: viết khối if/elif/else của bạn vào ngay dưới dòng này ----------


# ---------- Trường hợp c: viết khối if/elif/else của bạn vào ngay dưới dòng này ----------


# ---------- Trường hợp d: viết khối if/elif/else của bạn vào ngay dưới dòng này ----------


# %%
kiem_tra_3_1(trang_thai_a, trang_thai_b, trang_thai_c, trang_thai_d)

# %% [markdown]
# ### Bài tập 3.2 — Giá vé xem phim
#
# Có ba khách cho sẵn tuổi và suất chiếu (`la_buoi_toi` là `True`/`False`). Với mỗi
# khách, gán `gia_ve_*` (số nguyên, đơn vị VND) theo bảng:
#
# | Độ tuổi | Suất sáng | Suất tối |
# |---|---|---|
# | dưới 6 | 0 | 0 |
# | 6 đến 12 | 45000 | 60000 |
# | 13 đến 59 | 75000 | 100000 |
# | từ 60 trở lên | 50000 | 50000 |

# %%
tuoi_1, la_buoi_toi_1 = 4, False
tuoi_2, la_buoi_toi_2 = 10, True
tuoi_3, la_buoi_toi_3 = 70, True

# Khởi tạo sẵn để ô kiểm tra chạy được ngay cả khi bạn chưa làm gì.
gia_ve_1 = None
gia_ve_2 = None
gia_ve_3 = None

# ---------- Khách 1: làm sẵn để bạn xem mẫu ----------
# Bảng có hai chiều: trước hết chia theo tuổi, trong mỗi bậc tuổi mới xét suất chiếu.
if tuoi_1 < 6:
    gia_ve_1 = 0
elif tuoi_1 <= 12:
    if la_buoi_toi_1:
        gia_ve_1 = 60000
    else:
        gia_ve_1 = 45000
elif tuoi_1 <= 59:
    if la_buoi_toi_1:
        gia_ve_1 = 100000
    else:
        gia_ve_1 = 75000
else:
    gia_ve_1 = 50000

# ---------- Khách 2: viết khối if/elif/else của bạn vào ngay dưới dòng này ----------


# ---------- Khách 3: viết khối if/elif/else của bạn vào ngay dưới dòng này ----------


# %%
kiem_tra_3_2(gia_ve_1, gia_ve_2, gia_ve_3)

# %% [markdown]
# ---
# ## Dự án tuần 1 — Bộ ra quyết định lái xe
#
# Ghép cả ba bài lại. Có bốn tình huống, mỗi tình huống gồm khoảng cách vật cản
# (mét), tốc độ (km/h), mức pin (%). Với mỗi tình huống, gán `lenh_*` bằng một trong
# bốn mã lệnh, xét theo đúng thứ tự ưu tiên sau:
#
# 1. `khoang_cach <= 2.0` → `"DUNG_KHAN_CAP"`
# 2. `muc_pin < 15` → `"VE_TRAM_SAC"`
# 3. `khoang_cach <= 5.0` hoặc `toc_do > 60` → `"GIAM_TOC"`
# 4. còn lại → `"BINH_THUONG"`
#
# An toàn luôn được xét trước năng lượng: xe sắp hết pin nhưng có vật cản ngay
# trước mặt thì vẫn phải dừng khẩn cấp trước đã — tình huống `lenh_1` bên dưới kiểm
# tra đúng chỗ này.

# %%
khoang_cach_1, toc_do_1, muc_pin_1 = 1.5, 30, 5
khoang_cach_2, toc_do_2, muc_pin_2 = 20.0, 40, 10
khoang_cach_3, toc_do_3, muc_pin_3 = 30.0, 75, 90
khoang_cach_4, toc_do_4, muc_pin_4 = 30.0, 50, 90

# Khởi tạo sẵn để ô kiểm tra chạy được ngay cả khi bạn chưa làm gì.
lenh_1 = None
lenh_2 = None
lenh_3 = None
lenh_4 = None

# Dự án không làm mẫu sẵn. Bài 3.1 và 3.2 đã đi qua đúng cấu trúc này hai lần.
# Khối của bạn có dạng:
#     if <điều kiện ưu tiên 1>:
#         lenh_N = "..."
#     elif <điều kiện ưu tiên 2>:
#         ...
#     else:
#         lenh_N = "BINH_THUONG"
# Bốn điều kiện và thứ tự ưu tiên nằm ở phần đề bài ngay trên.

# ---------- Tình huống 1: viết khối if/elif/else của bạn vào ngay dưới dòng này ----------


# ---------- Tình huống 2: viết khối if/elif/else của bạn vào ngay dưới dòng này ----------


# ---------- Tình huống 3: viết khối if/elif/else của bạn vào ngay dưới dòng này ----------


# ---------- Tình huống 4: viết khối if/elif/else của bạn vào ngay dưới dòng này ----------


# %%
kiem_tra_du_an(lenh_1, lenh_2, lenh_3, lenh_4)

# %% [markdown]
# ---
# ## Tổng kết tuần 1
#
# Chạy ô dưới để kiểm tra toàn bộ bài trong tuần. Đạt hết mới coi là xong.

# %%
ket_qua = [
    kiem_tra_1_1(diem_tb_1, diem_tb_2),
    kiem_tra_1_2(noi_chuoi, tong_so),
    kiem_tra_2_1(moi_nguoi_tra_1, moi_nguoi_tra_2),
    kiem_tra_2_2(bao_cao),
    kiem_tra_2_3(gio, phut, giay),
    kiem_tra_3_1(trang_thai_a, trang_thai_b, trang_thai_c, trang_thai_d),
    kiem_tra_3_2(gia_ve_1, gia_ve_2, gia_ve_3),
    kiem_tra_du_an(lenh_1, lenh_2, lenh_3, lenh_4),
]

print(f"\nTONG KET TUAN 1: {sum(ket_qua)}/{len(ket_qua)} bai dat.")

# %% [markdown]
# Nhìn lại bài tập 3.1 và dự án: mỗi tình huống là một khối `if/elif/else` chép lại
# gần y hệt, chỉ khác tên biến đầu vào và biến kết quả. Bốn tình huống thì chép bốn
# lần; nếu có mười tình huống, phải chép mười lần. Tuần 2 gói khối đó lại thành một
# hàm, gọi lại bao nhiêu lần cũng chỉ viết logic một lần duy nhất.
#
# ### Nộp bài
#
# 1. `File > Save a copy in Drive` nếu bạn muốn giữ bản nháp riêng.
# 2. `File > Save a copy in GitHub`, chọn repo của bạn, đường dẫn `week1/week_1.ipynb`,
#    ghi commit message dạng `week1: hoan thanh bai tap`.
# 3. Hệ thống sẽ tự chấm lại và hiện kết quả trong tab Actions của repo.
