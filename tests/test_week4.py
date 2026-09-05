"""Bộ test tuần 4 - OOP nâng cao & cấu trúc dữ liệu tuyến tính."""

from __future__ import annotations
from collections import deque

try:
    from .runner import Case, kiem_tra
except ImportError:
    from runner import Case, kiem_tra


# --------------------------------------------------------------------------
# Bài 1: Kế thừa và Đa hình
# --------------------------------------------------------------------------

def _chay_kich_ban_ns(NhanVien, QuanLy, LapTrinhVien, so_kich_ban):
    if so_kich_ban == 1:
        nv = NhanVien("A", 10_000_000)
        return nv.tinh_tong_luong()
    if so_kich_ban == 2:
        ql = QuanLy("B", 15_000_000, 3_000_000)
        return ql.tinh_tong_luong()
    if so_kich_ban == 3:
        dv = LapTrinhVien("C", 12_000_000, 10)
        return dv.tinh_tong_luong()
    if so_kich_ban == 4:
        ql = QuanLy("D", 10_000_000, 2_000_000)
        return isinstance(ql, NhanVien)
    raise ValueError(f"kịch bản không hợp lệ: {so_kich_ban}")


def kiem_tra_1_1(NhanVien, QuanLy, LapTrinhVien) -> bool:
    """3 class: NhanVien (lớp cha), QuanLy và LapTrinhVien (kế thừa NhanVien).

    NhanVien.__init__(self, ten, luong_co_ban); tinh_tong_luong(self) -> luong_co_ban
    QuanLy.__init__(self, ten, luong_co_ban, phu_cap); tinh_tong_luong ghi đè: += phu_cap
    LapTrinhVien.__init__(self, ten, luong_co_ban, so_gio_ot, don_gia_ot=100000);
        tinh_tong_luong ghi đè: += so_gio_ot * don_gia_ot
    """
    ham = lambda so: _chay_kich_ban_ns(NhanVien, QuanLy, LapTrinhVien, so)
    return kiem_tra(
        "Bài 1.1 - Hệ thống nhân sự (kế thừa & đa hình)",
        ham,
        [
            Case(args=(1,), expected=10_000_000, mo_ta="nhân viên thường"),
            Case(args=(2,), expected=18_000_000, mo_ta="quản lý: lương cơ bản + phụ cấp"),
            Case(args=(3,), expected=13_000_000, mo_ta="lập trình viên: lương cơ bản + OT"),
            Case(args=(4,), expected=True, mo_ta="QuanLy phải là một NhanVien (kế thừa đúng)"),
        ],
    )


# --------------------------------------------------------------------------
# Bài 2: Stack & Queue
# --------------------------------------------------------------------------

def kiem_tra_2_1(ham) -> bool:
    """dao_nguoc_bang_stack(danh_sach) -> list đảo ngược, dùng nguyên lý LIFO (Stack)."""
    return kiem_tra(
        "Bài 2.1 - Đảo ngược bằng Stack",
        ham,
        [
            Case(args=([1, 2, 3],), expected=[3, 2, 1]),
            Case(args=(["a"],), expected=["a"], mo_ta="1 phần tử"),
            Case(args=([],), expected=[], mo_ta="danh sách rỗng"),
        ],
    )


def kiem_tra_2_2(ham) -> bool:
    """dieu_huong_waypoint(danh_sach_toa_do) -> list thông báo theo đúng thứ tự FIFO (Queue).

    Mỗi thông báo có dạng: f"Dang di chuyen toi toa do {toa_do}"
    """
    return kiem_tra(
        "Bài 2.2 - Điều hướng Waypoint bằng Queue",
        ham,
        [
            Case(
                args=([(0, 0), (1, 2)],),
                expected=["Dang di chuyen toi toa do (0, 0)", "Dang di chuyen toi toa do (1, 2)"],
            ),
            Case(args=([],), expected=[], mo_ta="không có waypoint nào"),
        ],
    )


# --------------------------------------------------------------------------
# Bài 3: Linked List
# --------------------------------------------------------------------------

def _chay_kich_ban_ll(TenLop, so_kich_ban):
    if so_kich_ban == 1:
        ds = TenLop()
        ds.them_cuoi("a")
        ds.them_cuoi("b")
        ds.them_cuoi("c")
        return ds.duyet()
    if so_kich_ban == 2:
        ds = TenLop()
        return ds.duyet()
    if so_kich_ban == 3:
        ds = TenLop()
        ds.them_cuoi(1)
        return ds.duyet()
    raise ValueError(f"kịch bản không hợp lệ: {so_kich_ban}")


def kiem_tra_3_1(TenLop) -> bool:
    """class DanhSachLienKet (dùng Node đã có sẵn ở ô ví dụ).

    __init__(self) -> self.head = None
    them_cuoi(self, data) -> nối Node mới vào cuối danh sách
    duyet(self) -> list chứa data của mọi Node theo đúng thứ tự
    """
    ham = lambda so: _chay_kich_ban_ll(TenLop, so)
    return kiem_tra(
        "Bài 3.1 - Danh sách liên kết đơn",
        ham,
        [
            Case(args=(1,), expected=["a", "b", "c"], mo_ta="thêm 3 phần tử vào cuối"),
            Case(args=(2,), expected=[], mo_ta="danh sách rỗng"),
            Case(args=(3,), expected=[1], mo_ta="chỉ 1 phần tử"),
        ],
    )


# --------------------------------------------------------------------------
# Dự án 3 - Polygon Area Calculator
# --------------------------------------------------------------------------

def _chay_kich_ban_hinh(HinhChuNhat, HinhVuong, so_kich_ban):
    if so_kich_ban == 1:
        hcn = HinhChuNhat(5, 3)
        return (hcn.dien_tich(), hcn.chu_vi())
    if so_kich_ban == 2:
        hv = HinhVuong(4)
        return (hv.dien_tich(), hv.chu_vi())
    if so_kich_ban == 3:
        hv = HinhVuong(4)
        hv.dat_canh(6)
        return (hv.dien_tich(), hv.chieu_dai, hv.chieu_rong)
    if so_kich_ban == 4:
        hv = HinhVuong(2)
        return isinstance(hv, HinhChuNhat)
    raise ValueError(f"kịch bản không hợp lệ: {so_kich_ban}")


def kiem_tra_du_an(HinhChuNhat, HinhVuong) -> bool:
    """2 class: HinhChuNhat (lớp cha) và HinhVuong (kế thừa HinhChuNhat).

    HinhChuNhat.__init__(self, chieu_dai, chieu_rong)
    HinhChuNhat.dien_tich(self); HinhChuNhat.chu_vi(self)
    HinhVuong.__init__(self, canh) -> gọi super().__init__(canh, canh)
    HinhVuong.dat_canh(self, canh_moi) -> đổi CẢ chieu_dai và chieu_rong để luôn bằng nhau
    """
    ham = lambda so: _chay_kich_ban_hinh(HinhChuNhat, HinhVuong, so)
    return kiem_tra(
        "Dự án tuần 4 - Máy tính diện tích đa giác",
        ham,
        [
            Case(args=(1,), expected=(15, 16), mo_ta="hình chữ nhật 5x3"),
            Case(args=(2,), expected=(16, 16), mo_ta="hình vuông cạnh 4"),
            Case(args=(3,), expected=(36, 6, 6), mo_ta="đổi cạnh -> cả 2 chiều phải bằng nhau"),
            Case(args=(4,), expected=True, mo_ta="HinhVuong phải là một HinhChuNhat"),
        ],
    )