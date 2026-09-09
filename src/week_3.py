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
# Đọc kết quả: lệnh đầu vào chuỗi hợp lệ, khối `try` chạy trọn, `except` bị bỏ
# qua, `finally` vẫn in dòng "Da hoan tat". Lệnh hai vào chuỗi lỗi, `float("N/A")`
# ném `ValueError` ngay giữa khối `try`, nhảy thẳng xuống `except ValueError`, và
# `finally` vẫn in dòng đó lần thứ hai — dù lần này có lỗi.
#
# Tính chất của `try/except/finally`:
#
# 1. `finally` luôn chạy, bất kể `try` có lỗi hay không, kể cả khi `try` hoặc
#    `except` có `return`.
# 2. Nhiều khối `except` được xét từ trên xuống, gặp loại lỗi khớp đầu tiên là
#    dừng, không xét tiếp các `except` sau. Đặt `except Exception` (bắt mọi lỗi)
#    lên trước sẽ nuốt luôn các `except` cụ thể đứng sau nó, chúng không bao giờ
#    được chạy tới.
# 3. Một khối `try` nhận nhiều `except`, mỗi `except` ứng với một loại lỗi khác
#    nhau, không cần lồng nhiều `try` riêng lẻ.
# 4. `raise TenLoi("thong bao")` chủ động tạo lỗi ngay tại chỗ, dùng khi dữ liệu
#    sai theo logic nghiệp vụ dù cú pháp Python không tự phát hiện ra.

# %%
def chia_hai_chuoi(a_str, b_str):
    try:
        a = float(a_str)
        b = float(b_str)
        return a / b
    except ValueError:
        return "LOI_DINH_DANG"
    except ZeroDivisionError:
        return "LOI_CHIA_CHO_KHONG"


print(chia_hai_chuoi("10", "2"))     # 5.0
print(chia_hai_chuoi("10", "abc"))   # LOI_DINH_DANG - float("abc") nem ValueError
print(chia_hai_chuoi("10", "0"))     # LOI_CHIA_CHO_KHONG - 10.0 / 0.0 nem ZeroDivisionError

# %% [markdown]
# Vết chạy hai lệnh gọi trên, theo tính chất 2 và 3 ở trên:
#
# | Lệnh gọi | Dòng chạy trong `try` | Lỗi ném ra | `except` khớp |
# |---|---|---|---|
# | `chia_hai_chuoi("10", "abc")` | `a = float("10")` chạy xong, `b = float("abc")` ném lỗi | `ValueError` | `except ValueError` |
# | `chia_hai_chuoi("10", "0")` | `a = float("10")`, `b = float("0")` chạy xong, `return a / b` ném lỗi | `ZeroDivisionError` | `except ZeroDivisionError` |
#
# Ở lệnh gọi thứ hai, `float("0")` không lỗi — `"0"` là chuỗi số hợp lệ. Lỗi chỉ
# xảy ra ở bước chia, dòng `return a / b`.
#
# Lỗi thường gặp: bắt lỗi quá rộng bằng `except:` trống (không chỉ rõ loại lỗi)
# nuốt luôn cả lỗi do chính bạn viết sai code, ví dụ gõ nhầm tên biến — chương
# trình chạy sai âm thầm mà không báo gì. Luôn chỉ rõ loại lỗi như `except
# ValueError:`. Ngoài ra không phải lỗi nào cũng nên "nuốt" bằng `except` — dữ
# liệu sai đến mức không thể tiếp tục thì nên để chương trình dừng lại, không
# âm thầm trả về giá trị sai (tính chất 4: `raise` để dừng có kiểm soát).
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
# Quản lý ba tài khoản bằng biến rời rạc thì phải nhớ đúng bộ tên-số dư cho từng
# tài khoản, và mọi hàm thao tác phải nhận đủ cả bộ đó làm tham số:

# %%
ten_1, so_du_1 = "Nguyen Van A", 1000000
ten_2, so_du_2 = "Tran Thi B", 200000


def nap_tien_rieng(so_du, so_tien):
    return so_du + so_tien


so_du_1 = nap_tien_rieng(so_du_1, 500000)
so_du_2 = nap_tien_rieng(so_du_2, 200000)
# them tai khoan thu 3 la them 2 bien moi (ten_3, so_du_3), va phai nho
# goi dung ten bien do o moi noi can dung den tai khoan thu 3.

# %% [markdown]
# OOP gom dữ liệu và hành vi của một thứ vào một đối tượng (object) duy nhất, để
# không phải nhớ và truyền tay bộ biến rời rạc đó nữa. Class là bản thiết kế;
# object là thực thể cụ thể được tạo ra từ bản thiết kế đó.
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
# Vết chạy lệnh `RoLe(chan_so=12)`:
#
# | Bước | Việc | Kết quả |
# |---|---|---|
# | 1 | Python tạo một object trống | object chưa có thuộc tính nào |
# | 2 | Gọi `__init__(self, chan_so)`; `self` trỏ vào object vừa tạo, `chan_so = 12` | |
# | 3 | Chạy `self.chan = chan_so` | object có thuộc tính `chan = 12` |
# | 4 | Chạy `self.dang_bat = False` | object có thêm thuộc tính `dang_bat = False` |
# | 5 | `__init__` kết thúc, object được gán cho `ro_le_camera` | `ro_le_camera.chan == 12` |
#
# `self` không phải từ khoá đặc biệt — nó chỉ là tên tham số đầu tiên, được
# Python tự truyền vào là chính object đang gọi phương thức. Gọi
# `ro_le_camera.bat()` thì bên trong `bat`, `self` chính là `ro_le_camera`.
#
# Lỗi thường gặp: quên tham số `self` ở phương thức mới định nghĩa làm số tham số
# truyền vào không khớp, Python báo lỗi ngay khi gọi. Gọi phương thức không qua
# object — viết `TenClass.phuong_thuc()` thay vì `object.phuong_thuc()` — thiếu
# `self` cũng báo lỗi tương tự. Sửa thuộc tính trực tiếp từ bên ngoài
# (`obj.so_du = -999999`) thay vì qua phương thức thì bỏ qua mọi kiểm tra logic mà
# class đã cài đặt — bài tập dưới đây yêu cầu số dư chỉ được đổi qua
# `nap_tien`/`rut_tien`, không gán tay.

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
# Trước bài tập, một class có phương thức từ chối thay đổi trạng thái khi dữ
# liệu không hợp lệ, cùng cách nghĩ mà `rut_tien` dưới đây cần: kiểm tra trước,
# chỉ đổi trạng thái khi hợp lệ, báo lại bằng giá trị `True`/`False`.

# %%
class DongHoToc:
    def __init__(self, toc_do_ban_dau=0):
        self.toc_do = toc_do_ban_dau

    def dat_toc_do(self, gia_tri_moi):
        if gia_tri_moi < 0:
            return False
        self.toc_do = gia_tri_moi
        return True

    def xem_toc_do(self):
        return self.toc_do


dong_ho = DongHoToc()
print(dong_ho.dat_toc_do(60))    # True - hop le, toc_do doi thanh 60
print(dong_ho.dat_toc_do(-10))   # False - khong hop le, toc_do KHONG doi
print(dong_ho.xem_toc_do())      # 60 - van la gia tri truoc do

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
# Dự án dưới đây cần một object tự giữ một **danh sách** giao dịch bên trong nó,
# thay vì chỉ vài thuộc tính đơn lẻ như `RoLe` hay `XeTuHanh`. Trước dự án, một
# class nhỏ theo đúng khuôn đó: mỗi lần nạp/xả pin là một `dict` được thêm vào
# một `list`, và một phương thức cộng dồn toàn bộ `list` đó thành một con số.

# %%
class NhatKyPin:
    def __init__(self):
        self.ban_ghi = []   # list các dict, mỗi dict la mot lan nap/xa

    def sac(self, luong, ly_do=""):
        self.ban_ghi.append({"thay_doi": luong, "ly_do": ly_do})

    def xa(self, luong, ly_do=""):
        self.ban_ghi.append({"thay_doi": -luong, "ly_do": ly_do})

    def muc_pin(self):
        tong = 0
        for ban_ghi in self.ban_ghi:
            tong += ban_ghi["thay_doi"]
        return tong


pin = NhatKyPin()
pin.sac(50, "sac qua dem")
pin.xa(20, "chay thu nghiem")
print(pin.muc_pin())    # 30 = 50 - 20
print(pin.ban_ghi)      # list 2 dict, dung thu tu da them vao

# %% [markdown]
# `muc_pin` không lưu sẵn một con số — nó tính lại từ đầu `self.ban_ghi` mỗi lần
# được gọi. `sac`/`xa` chỉ thêm bản ghi, không tự cộng dồn.
#
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
# - `chuyen_tien(self, hang_muc_khac, so_tien)` — gọi `self.rut_tien(...)`; nếu
#   thành công thì gọi thêm `hang_muc_khac.nap_tien(...)`; trả về kết quả của
#   việc rút (`True`/`False`)
# - `so_du(self)` — trả về tổng tất cả giao dịch trong `ledger`, cùng cách
#   `muc_pin` cộng dồn `ban_ghi` ở trên, chỉ đổi tên khoá dict thành `"so_tien"`
# - `__str__(self)` — trả về đúng định dạng: `"{ten}: {so_du} VND"`
#
# `chuyen_tien` là chỗ mới nhất so với `NhatKyPin`: một phương thức gọi phương
# thức của chính object mình (`self.rut_tien`), rồi gọi tiếp phương thức của một
# object `HangMuc` khác (`hang_muc_khac.nap_tien`).

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