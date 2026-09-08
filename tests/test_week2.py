"""Bộ test tuần 2 - Scope, vòng lặp & cấu trúc dữ liệu cơ bản."""

from __future__ import annotations

try:
    from .runner import Case, kiem_tra
except ImportError:
    from runner import Case, kiem_tra


# --------------------------------------------------------------------------
# Bài 1: Hàm và phạm vi biến
# --------------------------------------------------------------------------

def kiem_tra_1_1(ham) -> bool:
    """ap_dung_giam_gia(gia_goc, phan_tram=0) -> float, làm tròn 2 chữ số."""
    return kiem_tra(
        "Bài 1.1 - Áp dụng giảm giá",
        ham,
        [
            Case(args=(500000,), expected=500000.0, mo_ta="không truyền phần trăm -> dùng mặc định 0"),
            Case(args=(500000, 10), expected=450000.0),
            Case(args=(199000, 25), expected=149250.0),
            Case(args=(100000, 100), expected=0.0, mo_ta="giảm 100%"),
        ],
    )


def kiem_tra_1_2(ham) -> bool:
    """nhan_sat_thuong(mau_hien_tai, sat_thuong) -> int, không âm."""
    return kiem_tra(
        "Bài 1.2 - Nhân vật nhận sát thương",
        ham,
        [
            Case(args=(100, 30), expected=70),
            Case(args=(20, 30), expected=0, mo_ta="sát thương vượt máu hiện có -> về 0, không âm"),
            Case(args=(50, 0), expected=50, mo_ta="không nhận sát thương"),
        ],
    )


# --------------------------------------------------------------------------
# Bài 2: Chuỗi tuần tự và vòng lặp
# --------------------------------------------------------------------------

def kiem_tra_2_1(ham) -> bool:
    """ma_hoa_caesar(van_ban, dich_chuyen) -> str.

    Chỉ dịch chữ cái a-z/A-Z, giữ nguyên số/dấu câu/khoảng trắng, có vòng qua chữ z/Z.
    """
    return kiem_tra(
        "Bài 2.1 - Mã hoá Caesar",
        ham,
        [
            Case(args=("Hello, World!", 3), expected="Khoor, Zruog!"),
            Case(args=("abc XYZ", 2), expected="cde ZAB"),
            Case(args=("Python 3.11", 5), expected="Udymts 3.11", mo_ta="số và dấu chấm giữ nguyên"),
            Case(args=("xyz", 3), expected="abc", mo_ta="vòng qua từ z về a"),
        ],
    )


def kiem_tra_2_2(ham) -> bool:
    """loc_vat_can_gan(khoang_cach, nguong=1.0) -> list các khoảng cách < nguong."""
    return kiem_tra(
        "Bài 2.2 - Lọc vật cản gần",
        ham,
        [
            Case(args=([5.2, 3.1, 0.8, 4.5, 1.2, 0.3],), expected=[0.8, 0.3]),
            Case(args=([2.0, 1.0, 0.5],), expected=[0.5], mo_ta="đúng bằng ngưỡng thì không tính là gần"),
            Case(args=([1.5, 2.5, 0.9], 1.5), expected=[0.9], mo_ta="ngưỡng tuỳ chỉnh"),
        ],
    )


# --------------------------------------------------------------------------
# Bài 3: Dictionary, Set & Dự án 1
# --------------------------------------------------------------------------

def kiem_tra_3_1(ham) -> bool:
    """loc_trung_lap(ds) -> list, loại phần tử trùng nhưng giữ thứ tự xuất hiện đầu tiên."""
    return kiem_tra(
        "Bài 3.1 - Lọc phần tử trùng lặp",
        ham,
        [
            Case(args=([1, 2, 2, 3, 1, 4],), expected=[1, 2, 3, 4]),
            Case(args=(["a", "b", "a", "c"],), expected=["a", "b", "c"]),
            Case(args=([],), expected=[], mo_ta="danh sách rỗng"),
        ],
    )


def kiem_tra_3_2(ham) -> bool:
    """hop_nhat_cau_hinh(mac_dinh, tuy_chinh) -> dict, tuỳ chỉnh ghi đè mặc định."""
    return kiem_tra(
        "Bài 3.2 - Hợp nhất cấu hình",
        ham,
        [
            Case(
                args=({"toc_do": 30, "camera": "1080p"}, {"toc_do": 40}),
                expected={"toc_do": 40, "camera": "1080p"},
            ),
            Case(args=({"a": 1}, {}), expected={"a": 1}, mo_ta="không có tuỳ chỉnh nào"),
            Case(args=({}, {"b": 2}), expected={"b": 2}, mo_ta="không có mặc định nào"),
        ],
    )


def kiem_tra_3_3(ham) -> bool:
    """kiem_tra_quyen_truy_cap(quyen_nguoi_dung, quyen_yeu_cau) -> bool."""
    return kiem_tra(
        "Bài 3.3 - Kiểm tra quyền truy cập",
        ham,
        [
            Case(args=({"doc", "ghi", "xoa"}, {"doc", "ghi"}), expected=True, mo_ta="có đủ quyền yêu cầu"),
            Case(args=({"doc"}, {"doc", "ghi"}), expected=False, mo_ta="thiếu quyền 'ghi'"),
            Case(args=(set(), set()), expected=True, mo_ta="không yêu cầu quyền nào"),
        ],
    )


# --------------------------------------------------------------------------
# Dự án 1
# --------------------------------------------------------------------------

def kiem_tra_du_an(ham) -> bool:
    """quan_ly_cau_hinh(config_mac_dinh, config_tuy_chinh, quyen_nguoi_dung, quyen_yeu_cau)
    -> dict {"cau_hinh": ..., "duoc_phep": ...}
    """
    return kiem_tra(
        "Dự án tuần 2 - Bộ quản lý cấu hình người dùng",
        ham,
        [
            Case(
                args=({"toc_do": 30}, {"toc_do": 40}, {"doc"}, {"doc"}),
                expected={"cau_hinh": {"toc_do": 40}, "duoc_phep": True},
            ),
            Case(
                args=({"toc_do": 30}, {}, {"doc"}, {"ghi"}),
                expected={"cau_hinh": {"toc_do": 30}, "duoc_phep": False},
                mo_ta="đúng cấu hình nhưng thiếu quyền",
            ),
        ],
    )