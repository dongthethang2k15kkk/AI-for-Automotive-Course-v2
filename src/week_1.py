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
# **Cách học notebook này:** đọc lý thuyết, chạy ô ví dụ để thấy kết quả, rồi làm ô
# bài tập. Mỗi bài tập có một ô kiểm tra ngay bên dưới — chạy nó để biết mình đúng
# hay sai.
#
# **Quy tắc:** không sửa nội dung các ô kiểm tra. Chỉ viết code vào chỗ có `# TODO`.
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
    kiem_tra_3_1,
    kiem_tra_3_2,
    kiem_tra_du_an,
)

print("Moi truong san sang. Phien ban Python:", sys.version.split()[0])

# %% [markdown]
# ---
# ## Bài 1 — Biến và kiểu dữ liệu
#
# ### Lý thuyết
#
# Biến là một cái tên gắn với một giá trị trong bộ nhớ. Python không cần khai báo
# kiểu trước — kiểu được suy ra từ giá trị bạn gán.
#
# Bốn kiểu cơ bản dùng nhiều nhất:
#
# | Kiểu | Ý nghĩa | Ví dụ trong hệ thống xe |
# |---|---|---|
# | `int` | số nguyên | `motor_speed = 120` (vòng/phút) |
# | `float` | số thực | `battery_voltage = 11.5` (V) |
# | `str` | chuỗi ký tự | `system_status = "Dang chay"` |
# | `bool` | đúng/sai | `sensor_active = True` |
#
# **Quy ước đặt tên (PEP 8):** biến dùng `snake_case`, viết thường, các từ nối bằng
# dấu gạch dưới. Hằng số viết HOA: `MAX_SPEED = 120`.

# %%
# Khai báo các thông số của một hệ thống
motor_speed = 120            # int
battery_voltage = 11.5       # float
system_status = "Dang chay"  # str
sensor_active = True         # bool

MAX_SPEED = 150              # hằng số: viết HOA

print(motor_speed, type(motor_speed))
print(battery_voltage, type(battery_voltage))
print(system_status, type(system_status))
print(sensor_active, type(sensor_active))

# %% [markdown]
# ### Lỗi thường gặp
#
# **1. Nhầm chuỗi với số.** `"10"` và `10` là hai thứ khác nhau. Dữ liệu đọc từ cảm
# biến hay từ `input()` luôn là chuỗi, phải ép kiểu trước khi tính toán.
#
# **2. Dùng biến chưa gán.** Python báo `NameError`. Biến phải được gán trước khi dùng.
#
# **3. Đặt tên kiểu `x`, `a1`, `data2`.** Code chạy được nhưng ba tuần sau chính bạn
# cũng không hiểu. Tên biến là tài liệu rẻ nhất bạn có.
#
# **4. `type(True)` trả về `bool`, không phải `int`** — dù trong Python `True == 1`.

# %%
# Chuỗi và số khác nhau như thế nào
gia_tri_tho = "10"           # dữ liệu thô đọc về, luôn là chuỗi
print(gia_tri_tho + "5")     # nối chuỗi -> "105"
print(int(gia_tri_tho) + 5)  # ép kiểu rồi cộng -> 15

# %% [markdown]
# ### Bài tập 1.1 — Điểm trung bình
#
# Viết hàm `diem_trung_binh(toan, ly, hoa)` trả về điểm trung bình cộng của ba môn,
# **làm tròn 2 chữ số thập phân**.
#
# Gợi ý: dùng `round(gia_tri, 2)`.

# %%
def diem_trung_binh(toan, ly, hoa):
    # TODO: tính trung bình cộng ba môn, làm tròn 2 chữ số rồi trả về
    pass


# %%
kiem_tra_1_1(diem_trung_binh)

# %% [markdown]
# ### Bài tập 1.2 — Nhận diện kiểu dữ liệu
#
# Viết hàm `ten_kieu_du_lieu(gia_tri)` trả về **tên kiểu** của giá trị dưới dạng
# chuỗi: `"int"`, `"float"`, `"str"` hoặc `"bool"`.
#
# Gợi ý: `type(x)` cho ra đối tượng kiểu, còn `type(x).__name__` cho ra tên kiểu
# dưới dạng chuỗi.

# %%
def ten_kieu_du_lieu(gia_tri):
    # TODO: trả về tên kiểu của gia_tri dưới dạng chuỗi
    pass


# %%
kiem_tra_1_2(ten_kieu_du_lieu)

# %% [markdown]
# ---
# ## Bài 2 — Toán tử, chuỗi và ép kiểu
#
# ### Lý thuyết
#
# **Toán tử số học:** `+` `-` `*` `/` `//` `%` `**`
#
# - `/` luôn trả về `float`, kể cả `10 / 2` cho `5.0`.
# - `//` chia lấy phần nguyên, `%` lấy phần dư — rất hay dùng để chia chu kỳ, đổi đơn vị.
# - `**` là lũy thừa.
#
# **f-string** là cách ghép chuỗi chuẩn hiện nay. Đặt `f` trước dấu nháy, rồi nhúng
# biểu thức trong `{}`. Có thể định dạng ngay: `{x:.2f}` in số thực với 2 chữ số.
#
# **Ép kiểu:** `int()`, `float()`, `str()`.

# %%
tong_giay = 3725

gio = tong_giay // 3600
phut = (tong_giay % 3600) // 60
giay = tong_giay % 60

print(f"Thoi gian chay: {gio} gio {phut} phut {giay} giay")

# %%
van_toc = 15.5
thoi_gian = 4
quang_duong = van_toc * thoi_gian

print(f"Quang duong: {quang_duong} m")
print(f"Lam tron 2 chu so: {quang_duong:.2f} m")
print(f"Van toc trung binh: {quang_duong / thoi_gian:.1f} m/s")

# %% [markdown]
# ### Lỗi thường gặp
#
# **1. Quên ép kiểu sau `input()`.** `input()` luôn trả về `str`. `input() * 2` sẽ
# lặp lại chuỗi chứ không nhân đôi số.
#
# **2. Nhầm `round()` với định dạng `:.2f`.** `round()` đổi *giá trị*, `:.2f` chỉ đổi
# *cách hiển thị*. Khi bài yêu cầu trả về số đã làm tròn, phải dùng `round()`.
#
# **3. Ghép chuỗi bằng `+` với số** — `"Toc do: " + 120` báo `TypeError`. Dùng f-string.
#
# ### Cách viết chuẩn
#
# Ưu tiên f-string thay cho `+` hay `%` hay `.format()`. Ngắn hơn, đọc rõ hơn, nhanh hơn.

# %%
toc_do = 120

# Cách cũ, dài dòng
print("Toc do: " + str(toc_do) + " km/h")

# Cách nên dùng
print(f"Toc do: {toc_do} km/h")

# %% [markdown]
# ### Bài tập 2.1 — Chia hoá đơn
#
# Viết hàm `chia_hoa_don(tong_tien, phan_tram_tip, so_nguoi)` trả về **số tiền mỗi
# người phải trả**, đã cộng tiền tip, làm tròn 2 chữ số.
#
# Ví dụ: `chia_hoa_don(300000, 10, 3)` → tổng sau tip là 330000, chia 3 người → `110000.0`.

# %%
def chia_hoa_don(tong_tien, phan_tram_tip, so_nguoi):
    # TODO: cộng tip vào tổng, chia đều cho số người, làm tròn 2 chữ số
    pass


# %%
kiem_tra_2_1(chia_hoa_don)

# %% [markdown]
# ### Bài tập 2.2 — Báo cáo quãng đường
#
# Viết hàm `bao_cao_quang_duong(van_toc, thoi_gian)` trả về chuỗi **đúng theo mẫu**:
#
# ```
# Xe đã đi được {quang_duong} mét trong {thoi_gian} giây.
# ```
#
# Trong đó `quang_duong = van_toc * thoi_gian`, **không làm tròn**.
#
# Ví dụ: `bao_cao_quang_duong(15.5, 4)` → `"Xe đã đi được 62.0 mét trong 4 giây."`
#
# Chú ý dấu chấm cuối câu và dấu tiếng Việt phải khớp chính xác.

# %%
def bao_cao_quang_duong(van_toc, thoi_gian):
    # TODO: tính quãng đường và trả về chuỗi đúng mẫu bằng f-string
    pass


# %%
kiem_tra_2_2(bao_cao_quang_duong)

# %% [markdown]
# ### Ô tự do — thử `input()`
#
# Ô này không chấm điểm. Bỏ dấu `#` để chạy thử. Lưu ý: khi chạy, notebook sẽ **dừng
# lại chờ bạn gõ** vào ô nhập hiện ra bên dưới.

# %%
# tong = float(input("Tong hoa don: "))
# nguoi = int(input("So nguoi: "))
# print(f"Moi nguoi tra {tong / nguoi:.2f}")

# %% [markdown]
# ---
# ## Bài 3 — Boolean và câu lệnh điều kiện
#
# ### Lý thuyết
#
# **Toán tử so sánh** cho ra `True`/`False`: `==` `!=` `>` `<` `>=` `<=`
#
# **Toán tử logic:** `and` (cả hai đúng), `or` (một trong hai đúng), `not` (đảo ngược).
#
# **Cấu trúc rẽ nhánh:**
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
# Python dùng **thụt lề** để xác định khối lệnh, không dùng ngoặc nhọn. Thụt lề sai
# là lỗi cú pháp, không phải chuyện thẩm mỹ. Chuẩn là 4 dấu cách.
#
# Các nhánh `if / elif / else` được xét **lần lượt từ trên xuống**, gặp nhánh đúng
# đầu tiên là dừng. Thứ tự các nhánh vì thế quyết định kết quả.

# %%
khoang_cach = 3.7

if khoang_cach <= 2.0:
    trang_thai = "PHANH_KHAN_CAP"
elif khoang_cach <= 5.0:
    trang_thai = "GIAM_TOC"
else:
    trang_thai = "AN_TOAN"

print(f"Khoang cach {khoang_cach} m -> {trang_thai}")

# %% [markdown]
# ### Lỗi thường gặp
#
# **1. Dùng `=` thay cho `==`.** `=` là gán, `==` là so sánh. Trong `if` phải dùng `==`.
#
# **2. Viết nhiều `if` liên tiếp thay vì `elif`.** Nhiều `if` sẽ được xét *tất cả*,
# nên biến kết quả có thể bị nhánh sau ghi đè lên nhánh trước.
#
# **3. Sai thứ tự nhánh.** Nếu đặt `if khoang_cach <= 5.0` lên trước, thì trường hợp
# 1.5 m cũng rơi vào nhánh đó và không bao giờ chạm tới nhánh khẩn cấp.
#
# **4. Quên xét giá trị biên.** Đề nói "nhỏ hơn hoặc bằng 2.0" thì phải là `<= 2.0`,
# không phải `< 2.0`. Test luôn kiểm tra đúng chỗ này.
#
# ### Cách viết chuẩn
#
# Với hàm chỉ để phân loại, `return` thẳng trong từng nhánh gọn hơn là gán biến rồi
# `return` ở cuối.

# %%
def phan_loai(khoang_cach):
    if khoang_cach <= 2.0:
        return "PHANH_KHAN_CAP"
    if khoang_cach <= 5.0:
        return "GIAM_TOC"
    return "AN_TOAN"


print(phan_loai(1.0), phan_loai(3.0), phan_loai(9.0))

# %% [markdown]
# ### Bài tập 3.1 — Cảnh báo vật cản
#
# Viết hàm `canh_bao_vat_can(khoang_cach)` trả về:
#
# | Điều kiện | Kết quả |
# |---|---|
# | `khoang_cach <= 2.0` | `"PHANH_KHAN_CAP"` |
# | `khoang_cach <= 5.0` | `"GIAM_TOC"` |
# | còn lại | `"AN_TOAN"` |

# %%
def canh_bao_vat_can(khoang_cach):
    # TODO: trả về mã trạng thái theo bảng trên
    pass


# %%
kiem_tra_3_1(canh_bao_vat_can)

# %% [markdown]
# ### Bài tập 3.2 — Giá vé xem phim
#
# Viết hàm `gia_ve(tuoi, la_buoi_toi)` trả về giá vé (số nguyên, đơn vị VND).
# `la_buoi_toi` là `True`/`False`.
#
# | Độ tuổi | Suất sáng | Suất tối |
# |---|---|---|
# | dưới 6 | 0 | 0 |
# | 6 đến 12 | 45000 | 60000 |
# | 13 đến 59 | 75000 | 100000 |
# | từ 60 trở lên | 50000 | 50000 |

# %%
def gia_ve(tuoi, la_buoi_toi):
    # TODO: trả về giá vé theo bảng trên
    pass


# %%
kiem_tra_3_2(gia_ve)

# %% [markdown]
# ---
# ## Dự án tuần 1 — Bộ ra quyết định lái xe
#
# Ghép cả ba bài lại: viết hàm `quyet_dinh_lai_xe(khoang_cach, toc_do, muc_pin)`
# trả về một trong bốn mã lệnh, xét **theo đúng thứ tự ưu tiên** sau:
#
# 1. `khoang_cach <= 2.0` → `"DUNG_KHAN_CAP"`
# 2. `muc_pin < 15` → `"VE_TRAM_SAC"`
# 3. `khoang_cach <= 5.0` **hoặc** `toc_do > 60` → `"GIAM_TOC"`
# 4. còn lại → `"BINH_THUONG"`
#
# An toàn luôn được xét trước năng lượng: xe sắp hết pin nhưng có vật cản ngay trước
# mặt thì vẫn phải dừng khẩn cấp trước đã.
#
# Đơn vị: `khoang_cach` mét, `toc_do` km/h, `muc_pin` phần trăm.

# %%
def quyet_dinh_lai_xe(khoang_cach, toc_do, muc_pin):
    # TODO: cài đặt đúng thứ tự ưu tiên ở trên
    pass


# %%
kiem_tra_du_an(quyet_dinh_lai_xe)

# %% [markdown]
# ---
# ## Tổng kết tuần 1
#
# Chạy ô dưới để kiểm tra toàn bộ bài trong tuần. Đạt hết mới coi là xong.

# %%
ket_qua = [
    kiem_tra_1_1(diem_trung_binh),
    kiem_tra_1_2(ten_kieu_du_lieu),
    kiem_tra_2_1(chia_hoa_don),
    kiem_tra_2_2(bao_cao_quang_duong),
    kiem_tra_3_1(canh_bao_vat_can),
    kiem_tra_3_2(gia_ve),
    kiem_tra_du_an(quyet_dinh_lai_xe),
]

print(f"\nTONG KET TUAN 1: {sum(ket_qua)}/{len(ket_qua)} bai dat.")

# %% [markdown]
# ### Nộp bài
#
# 1. `File > Save a copy in Drive` nếu bạn muốn giữ bản nháp riêng.
# 2. `File > Save a copy in GitHub`, chọn repo của bạn, đường dẫn `week1/week_1.ipynb`,
#    ghi commit message dạng `week1: hoan thanh bai tap`.
# 3. Hệ thống sẽ tự chấm lại và hiện kết quả trong tab Actions của repo.