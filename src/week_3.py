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
# # Tuần 3 — Xử lý lỗi & Tư duy hướng đối tượng (OOP)
#
# **Mục tiêu sau tuần này, bạn phải làm được:**
#
# 1. Bọc code có rủi ro bằng `try/except`, chủ động `raise` khi dữ liệu sai.
# 2. Định nghĩa `class`, hiểu `__init__` và `self`.
# 3. Viết một hệ thống nhỏ có trạng thái (Budget App) hoàn toàn bằng OOP.

# %%
# Ô thiết lập - chạy đầu tiên, mỗi lần mở notebook.
import os
import sys
import urllib.request

REPO_RAW = "https://raw.githubusercontent.com/dongthethang2k15kkk/AI-for-Automotive-Course-v2/main"

if not os.path.isdir("tests"):
    os.makedirs("tests", exist_ok=True)
    open(os.path.join("tests", "__init__.py"), "w").close()
    for ten_file in ("runner.py", "test_week3.py"):
        urllib.request.urlretrieve(
            f"{REPO_RAW}/tests/{ten_file}", os.path.join("tests", ten_file)
        )

if os.getcwd() not in sys.path:
    sys.path.insert(0, os.getcwd())

from tests.test_week3 import kiem_tra_1_1, kiem_tra_2_1, kiem_tra_du_an

print("Moi truong san sang. Phien ban Python:", sys.version.split()[0])

# %% [markdown]
# ---
# ## Bài 1 — Xử lý ngoại lệ (Error Handling)
#
# Lỗi cú pháp (Syntax Error) khiến code không chạy được ngay từ đầu, Python báo
# trước khi thực thi bất kỳ dòng nào. Lỗi thực thi (Exception) xảy ra khi code cú
# pháp đúng nhưng gặp tình huống không xử lý được lúc chạy, ví dụ `ValueError` (ép
# kiểu thất bại), `ZeroDivisionError` (chia cho 0), `TypeError` (sai kiểu dữ liệu).
#
# ```python
# try:
#     ... code có rủi ro ...
# except LoaiLoi1:
#     ... xử lý khi gặp LoaiLoi1 ...
# except LoaiLoi2:
#     ... xử lý khi gặp LoaiLoi2 ...
# else:
#     ... chạy khi KHÔNG có lỗi ...
# finally:
#     ... luôn luôn chạy, dù có lỗi hay không ...
# ```
#
# `raise` dùng để **chủ động** báo lỗi khi dữ liệu vi phạm logic nghiệp vụ, dù cú
# pháp Python không tự phát hiện ra.

# %%
def doc_cam_bien(chuoi_du_lieu):
    try:
        nhiet_do = float(chuoi_du_lieu)
        print(f"Nhiet do hien tai: {nhiet_do} do C")
    except ValueError:
        print(f"Loi dinh dang: '{chuoi_du_lieu}' khong phai la so.")
    finally:
        print("Da hoan tat chu ky doc cam bien.\n")


doc_cam_bien("30.2")   # dữ liệu chuẩn
doc_cam_bien("N/A")    # dữ liệu bị nhiễu

# %% [markdown]
# ### Lỗi thường gặp
#
# **1. Bắt lỗi quá rộng bằng `except:` trống.** Cách này nuốt luôn cả lỗi do chính
# bạn viết sai code (ví dụ gõ nhầm tên biến), khiến chương trình chạy sai âm thầm
# mà không báo gì. Luôn chỉ rõ loại lỗi: `except ValueError:`.
#
# **2. Quên rằng `else` trong `try/except` chỉ chạy khi KHÔNG có lỗi** — nhiều
# người nhầm tưởng `else` là "trường hợp còn lại của except".
#
# **3. Không phân biệt được nên `except` hay nên để chương trình dừng hẳn.** Không
# phải lỗi nào cũng nên "nuốt" — có lỗi nên để chương trình dừng lại để người dùng
# biết mà sửa dữ liệu đầu vào, thay vì âm thầm trả về giá trị sai.
#
# ### Trả lỗi ra sao khi hàm cần trả kết quả
#
# Khi hàm cần trả kết quả thay vì chỉ in ra, hãy trả về một mã lỗi hoặc `raise`
# lại, đừng `print()` rồi `return None`: chỗ gọi hàm nhận `None` thường dùng luôn
# giá trị đó ở bước tính tiếp theo, gây lỗi mới khó truy ngược lại nguyên nhân gốc.

# %%
def chia_an_toan(tu_so, mau_so):
    if mau_so == 0:
        raise ValueError("Mau so khong duoc bang 0")
    return tu_so / mau_so


try:
    print(chia_an_toan(10, 0))
except ValueError as loi:
    print(f"Da chan dung: {loi}")

# %% [markdown]
# ### Bài tập 1.1 — Tính vận tốc an toàn
#
# Viết hàm `tinh_van_toc_an_toan(quang_duong_str, thoi_gian_str)`. Cả hai tham số
# là **chuỗi** (mô phỏng dữ liệu từ `input()`). Hàm phải:
#
# 1. Ép hai chuỗi sang `float`.
# 2. Nếu ép kiểu thất bại → trả về chuỗi `"LOI_DINH_DANG"`.
# 3. Nếu thời gian bằng 0 → trả về chuỗi `"LOI_CHIA_CHO_KHONG"`.
# 4. Ngược lại → trả về vận tốc = quãng đường / thời gian, **làm tròn 2 chữ số**.

# %%
def tinh_van_toc_an_toan(quang_duong_str, thoi_gian_str):
    # TODO: try ép kiểu + chia, except ValueError, except ZeroDivisionError
    pass


# %%
kiem_tra_1_1(tinh_van_toc_an_toan)

# %% [markdown]
# ---
# ## Bài 2 — Nhập môn Lập trình hướng đối tượng
#
# Thay vì để dữ liệu (biến) và hành vi (hàm) rời rạc, OOP gom chúng vào một đối
# tượng (object) duy nhất. Class là bản thiết kế; object là thực thể cụ thể được
# tạo ra từ bản thiết kế đó.
#
# `__init__` là phương thức chạy tự động khi object vừa được tạo — dùng để thiết
# lập trạng thái ban đầu. `self` là tham số đầu tiên của mọi phương thức, đại diện
# cho chính object đang gọi phương thức đó — dùng để truy cập thuộc tính/phương
# thức nội bộ.

# %%
class RoLe:
    def __init__(self, chan_so):
        self.chan = chan_so
        self.dang_bat = False

    def bat(self):
        self.dang_bat = True
        print(f"Ro-le tai chan {self.chan} DA BAT.")

    def tat(self):
        self.dang_bat = False
        print(f"Ro-le tai chan {self.chan} DA TAT.")


ro_le_camera = RoLe(chan_so=12)
ro_le_camera.bat()

# %% [markdown]
# ### Lỗi thường gặp
#
# **1. Quên tham số `self`.** Mọi phương thức trong class (trừ một số trường hợp
# đặc biệt chưa học tới) đều phải nhận `self` làm tham số đầu tiên, kể cả khi
# không dùng đến nó bên trong.
#
# **2. Gọi phương thức không qua object.** Phải gọi `object.phuong_thuc()`, không
# phải `TenClass.phuong_thuc()` (trừ khi bạn hiểu rõ mình đang làm gì với
# classmethod — chưa học tới trong tuần này).
#
# **3. Thay đổi thuộc tính trực tiếp từ bên ngoài** (`obj.so_du = -999999`) thay vì
# qua phương thức — bỏ qua mọi kiểm tra logic mà class đã cài đặt. Bài tập dưới
# đây yêu cầu số dư chỉ được đổi qua `nap_tien`/`rut_tien`, không được gán tay.

# %%
class DemPhanTram:
    tong_so_lan_tao = 0  # dùng chung cho MỌI object của class này

    def __init__(self):
        DemPhanTram.tong_so_lan_tao += 1
        self.thu_tu = DemPhanTram.tong_so_lan_tao


a = DemPhanTram()
b = DemPhanTram()
c = DemPhanTram()
print(a.thu_tu, b.thu_tu, c.thu_tu)          # 1 2 3 - riêng từng object
print(DemPhanTram.tong_so_lan_tao)           # 3 - dùng chung

# %% [markdown]
# ### Bài tập 2.1 — Tài khoản ngân hàng
#
# Viết class `TaiKhoanNganHang` với:
#
# - `__init__(self, chu_the, so_du=0)`
# - `nap_tien(self, so_tien)` — cộng thêm vào số dư
# - `rut_tien(self, so_tien)` — trả về `True` nếu rút thành công; nếu số dư không
#   đủ, trả về `False` và **không được thay đổi số dư**
# - `xem_so_du(self)` — trả về số dư hiện tại

# %%
class TaiKhoanNganHang:
    def __init__(self, chu_the, so_du=0):
        # TODO: lưu chu_the và so_du thành thuộc tính
        pass

    def nap_tien(self, so_tien):
        # TODO: cộng so_tien vào số dư
        pass

    def rut_tien(self, so_tien):
        # TODO: nếu đủ tiền thì trừ và trả True, không thì trả False
        pass

    def xem_so_du(self):
        # TODO: trả về số dư hiện tại
        pass


# %%
kiem_tra_2_1(TaiKhoanNganHang)

# %% [markdown]
# ---
# ## Bài 3 — Quản lý trạng thái đối tượng
#
# Thuộc tính của Class (Class Variable) dùng chung cho mọi object, ví dụ
# `tong_so_lan_tao` ở trên. Thuộc tính của Object (Instance Variable), khai báo
# trong `__init__` bằng `self.ten = ...`, độc lập cho từng object.
#
# `__str__(self)` tùy chỉnh chuỗi hiển thị khi `print(object)` được gọi, thay vì
# phải tự viết `print(f"...")` mỗi lần cần in trạng thái của object đó.

# %%
class XeTuHanh:
    ten_doi = "Racing Team"  # class variable — mọi xe dùng chung

    def __init__(self, ma_xe):
        self.ma_xe = ma_xe          # instance variable — riêng từng xe
        self.toc_do_hien_tai = 0

    def __str__(self):
        return f"Xe [{self.ma_xe}] - Van toc: {self.toc_do_hien_tai} km/h"


xe_1 = XeTuHanh("CAR-01")
print(xe_1)  # tự động gọi __str__

# %% [markdown]
# ---
# ## Dự án 2 — Budget App (Ứng dụng quản lý ngân sách)
#
# Đây là bài kiểm tra toàn diện: thiết kế class, quản lý danh sách giao dịch bên
# trong object, và định dạng chuỗi qua `__str__`.
#
# Viết class `HangMuc` (đại diện một hạng mục chi tiêu, ví dụ "Ăn uống",
# "Xăng xe"):
#
# - `__init__(self, ten)` — khởi tạo với tên hạng mục, `ledger` (sổ giao dịch) rỗng
# - `nap_tien(self, so_tien, mo_ta="")` — thêm giao dịch dương vào `ledger`
# - `rut_tien(self, so_tien, mo_ta="")` — nếu đủ số dư thì thêm giao dịch âm vào
#   `ledger` và trả `True`; nếu không đủ, trả `False` và **không thay đổi ledger**
# - `chuyen_tien(self, hang_muc_khac, so_tien)` — rút từ hạng mục này, nạp vào
#   `hang_muc_khac`; trả về kết quả của việc rút (`True`/`False`)
# - `so_du(self)` — trả về tổng tất cả giao dịch trong `ledger`
# - `__str__(self)` — trả về đúng định dạng: `"{ten}: {so_du} VND"`
#
# Gợi ý cấu trúc `ledger`: một `list` các `dict`, mỗi phần tử dạng
# `{"so_tien": ..., "mo_ta": ...}`. `so_du()` chỉ cần cộng dồn `so_tien` của từng
# phần tử.

# %%
class HangMuc:
    def __init__(self, ten):
        # TODO: lưu ten, khởi tạo ledger = []
        pass

    def nap_tien(self, so_tien, mo_ta=""):
        # TODO: thêm {"so_tien": so_tien, "mo_ta": mo_ta} vào ledger
        pass

    def rut_tien(self, so_tien, mo_ta=""):
        # TODO: nếu đủ số dư thì thêm giao dịch âm, trả True; không thì trả False
        pass

    def chuyen_tien(self, hang_muc_khac, so_tien):
        # TODO: gọi self.rut_tien(...), nếu thành công thì hang_muc_khac.nap_tien(...)
        pass

    def so_du(self):
        # TODO: cộng dồn so_tien của mọi giao dịch trong ledger
        pass

    def __str__(self):
        # TODO: trả về "{ten}: {so_du} VND"
        pass


# %%
kiem_tra_du_an(HangMuc)

# %% [markdown]
# ---
# ## Tổng kết tuần 3

# %%
ket_qua = [
    kiem_tra_1_1(tinh_van_toc_an_toan),
    kiem_tra_2_1(TaiKhoanNganHang),
    kiem_tra_du_an(HangMuc),
]

print(f"\nTONG KET TUAN 3: {sum(ket_qua)}/{len(ket_qua)} bai dat.")

# %% [markdown]
# ### Nộp bài
#
# `File > Save a copy in GitHub`, chọn repo của bạn, đường dẫn `week3/week_3.ipynb`.