"""Bộ test tuần 3 - Xử lý lỗi & tư duy hướng đối tượng (OOP)."""

from __future__ import annotations

try:
    from .runner import Case, kiem_tra
except ImportError:
    from runner import Case, kiem_tra


# --------------------------------------------------------------------------
# Bài 1: Xử lý ngoại lệ
# --------------------------------------------------------------------------

def kiem_tra_1_1(ham) -> bool:
    """tinh_van_toc_an_toan(quang_duong_str, thoi_gian_str) -> float | "LOI_DINH_DANG" | "LOI_CHIA_CHO_KHONG".

    Đầu vào là CHUỖI (mô phỏng input()). Trả về vận tốc làm tròn 2 chữ số nếu hợp
    lệ; "LOI_DINH_DANG" nếu không ép kiểu được sang số; "LOI_CHIA_CHO_KHONG" nếu
    thời gian bằng 0.
    """
    return kiem_tra(
        "Bài 1.1 - Tính vận tốc an toàn",
        ham,
        [
            Case(args=("100", "4"), expected=25.0),
            Case(args=("100", "abc"), expected="LOI_DINH_DANG", mo_ta="thời gian không phải số"),
            Case(args=("100", "0"), expected="LOI_CHIA_CHO_KHONG", mo_ta="thời gian bằng 0"),
            Case(args=("50.5", "2"), expected=25.25),
            Case(args=("abc", "5"), expected="LOI_DINH_DANG", mo_ta="quãng đường không phải số"),
        ],
    )


# --------------------------------------------------------------------------
# Bài 2: Class & Object cơ bản
# --------------------------------------------------------------------------

def _chay_kich_ban_tk(TenLop, so_kich_ban):
    if so_kich_ban == 1:
        tk = TenLop("Nguyen Van A", 1000000)
        tk.nap_tien(500000)
        return tk.xem_so_du()
    if so_kich_ban == 2:
        tk = TenLop("Tran Thi B", 200000)
        tk.rut_tien(150000)
        return tk.xem_so_du()
    if so_kich_ban == 3:
        tk = TenLop("Le Van C", 100000)
        thanh_cong = tk.rut_tien(500000)
        return (thanh_cong, tk.xem_so_du())
    if so_kich_ban == 4:
        tk = TenLop("Pham Thi D")
        return tk.xem_so_du()
    raise ValueError(f"kịch bản không hợp lệ: {so_kich_ban}")


def kiem_tra_2_1(TenLop) -> bool:
    """class TaiKhoanNganHang.

    __init__(self, chu_the, so_du=0)
    nap_tien(self, so_tien) -> None
    rut_tien(self, so_tien) -> bool (False và KHÔNG đổi số dư nếu không đủ tiền)
    xem_so_du(self) -> số dư hiện tại
    """
    ham = lambda so: _chay_kich_ban_tk(TenLop, so)
    return kiem_tra(
        "Bài 2.1 - Tài khoản ngân hàng",
        ham,
        [
            Case(args=(1,), expected=1500000, mo_ta="nạp 500k vào tài khoản có sẵn 1tr"),
            Case(args=(2,), expected=50000, mo_ta="rút 150k từ 200k"),
            Case(args=(3,), expected=(False, 100000), mo_ta="rút vượt số dư -> thất bại, số dư không đổi"),
            Case(args=(4,), expected=0, mo_ta="không truyền so_du -> mặc định 0"),
        ],
    )


# --------------------------------------------------------------------------
# Dự án 2 - Budget App
# --------------------------------------------------------------------------

def _chay_kich_ban_hm(TenLop, so_kich_ban):
    if so_kich_ban == 1:
        hm = TenLop("An uong")
        hm.nap_tien(500000)
        return hm.so_du()
    if so_kich_ban == 2:
        hm = TenLop("An uong")
        hm.nap_tien(500000)
        hm.rut_tien(200000)
        return hm.so_du()
    if so_kich_ban == 3:
        hm = TenLop("An uong")
        hm.nap_tien(100000)
        thanh_cong = hm.rut_tien(200000)
        return (thanh_cong, hm.so_du())
    if so_kich_ban == 4:
        a = TenLop("Xang xe")
        b = TenLop("Sua chua")
        a.nap_tien(300000)
        a.chuyen_tien(b, 100000)
        return (a.so_du(), b.so_du())
    if so_kich_ban == 5:
        hm = TenLop("Giai tri")
        hm.nap_tien(50000)
        return str(hm)
    raise ValueError(f"kịch bản không hợp lệ: {so_kich_ban}")


def kiem_tra_du_an(TenLop) -> bool:
    """class HangMuc (Category).

    __init__(self, ten)
    nap_tien(self, so_tien, mo_ta="") -> None
    rut_tien(self, so_tien, mo_ta="") -> bool (False và KHÔNG trừ nếu không đủ tiền)
    chuyen_tien(self, hang_muc_khac, so_tien) -> bool
    so_du(self) -> tổng các giao dịch trong ledger
    __str__(self) -> "{ten}: {so_du} VND"
    """
    ham = lambda so: _chay_kich_ban_hm(TenLop, so)
    return kiem_tra(
        "Dự án tuần 3 - Budget App (Category)",
        ham,
        [
            Case(args=(1,), expected=500000, mo_ta="nạp tiền"),
            Case(args=(2,), expected=300000, mo_ta="nạp rồi rút"),
            Case(args=(3,), expected=(False, 100000), mo_ta="rút vượt số dư -> thất bại"),
            Case(args=(4,), expected=(200000, 100000), mo_ta="chuyển tiền giữa 2 hạng mục"),
            Case(args=(5,), expected="Giai tri: 50000 VND", mo_ta="định dạng chuỗi qua __str__"),
        ],
    )