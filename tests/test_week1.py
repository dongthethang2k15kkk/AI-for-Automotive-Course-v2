"""Bộ test tuần 1 - Nền tảng & Cú pháp cơ bản.

Mỗi bài tập trong notebook tương ứng một hàm kiem_tra_* ở đây.
Học viên chỉ cần gọi, ví dụ:  kiem_tra_1_1(diem_trung_binh)
"""

from __future__ import annotations

try:
    from .runner import Case, kiem_tra
except ImportError:  # khi chạy trực tiếp trong Colab, không qua package
    from runner import Case, kiem_tra


# --------------------------------------------------------------------------
# Bài 1: Biến và kiểu dữ liệu
# --------------------------------------------------------------------------

def kiem_tra_1_1(ham) -> bool:
    """diem_trung_binh(toan, ly, hoa) -> float, làm tròn 2 chữ số."""
    return kiem_tra(
        "Bài 1.1 - Điểm trung bình",
        ham,
        [
            Case(args=(8, 9, 10), expected=9.0),
            Case(args=(7.5, 6, 8), expected=7.17, mo_ta="làm tròn 2 chữ số"),
            Case(args=(10, 10, 10), expected=10.0),
            Case(args=(0, 0, 0), expected=0.0),
        ],
    )


def kiem_tra_1_2(ham) -> bool:
    """ten_kieu_du_lieu(gia_tri) -> str: 'int' | 'float' | 'str' | 'bool'."""
    return kiem_tra(
        "Bài 1.2 - Nhận diện kiểu dữ liệu",
        ham,
        [
            Case(args=(120,), expected="int"),
            Case(args=(11.5,), expected="float"),
            Case(args=("Đang chạy",), expected="str"),
            Case(args=(True,), expected="bool", mo_ta="bool phải ra 'bool', không phải 'int'"),
        ],
    )


# --------------------------------------------------------------------------
# Bài 2: Toán tử, chuỗi và ép kiểu
# --------------------------------------------------------------------------

def kiem_tra_2_1(ham) -> bool:
    """chia_hoa_don(tong_tien, phan_tram_tip, so_nguoi) -> float, làm tròn 2 chữ số."""
    return kiem_tra(
        "Bài 2.1 - Chia hoá đơn",
        ham,
        [
            Case(args=(300000, 10, 3), expected=110000.0),
            Case(args=(250000, 0, 4), expected=62500.0, mo_ta="không tip"),
            Case(args=(100000, 15, 3), expected=38333.33, mo_ta="làm tròn 2 chữ số"),
            Case(args=(500000, 20, 1), expected=600000.0, mo_ta="đi một mình"),
        ],
    )


def kiem_tra_2_2(ham) -> bool:
    """bao_cao_quang_duong(van_toc, thoi_gian) -> str theo đúng mẫu f-string."""
    return kiem_tra(
        "Bài 2.2 - Báo cáo quãng đường",
        ham,
        [
            Case(args=(15.5, 4), expected="Xe đã đi được 62.0 mét trong 4 giây."),
            Case(args=(20.0, 3), expected="Xe đã đi được 60.0 mét trong 3 giây."),
            Case(args=(12.25, 2), expected="Xe đã đi được 24.5 mét trong 2 giây."),
        ],
    )


# --------------------------------------------------------------------------
# Bài 3: Boolean và câu lệnh điều kiện
# --------------------------------------------------------------------------

def kiem_tra_3_1(ham) -> bool:
    """canh_bao_vat_can(khoang_cach) -> 'PHANH_KHAN_CAP' | 'GIAM_TOC' | 'AN_TOAN'."""
    return kiem_tra(
        "Bài 3.1 - Cảnh báo vật cản",
        ham,
        [
            Case(args=(0.5,), expected="PHANH_KHAN_CAP"),
            Case(args=(2.0,), expected="PHANH_KHAN_CAP", mo_ta="biên 2.0 vẫn là khẩn cấp"),
            Case(args=(3.7,), expected="GIAM_TOC"),
            Case(args=(5.0,), expected="GIAM_TOC", mo_ta="biên 5.0 vẫn là giảm tốc"),
            Case(args=(12.0,), expected="AN_TOAN"),
        ],
    )


def kiem_tra_3_2(ham) -> bool:
    """gia_ve(tuoi, la_buoi_toi) -> int (đơn vị VND)."""
    return kiem_tra(
        "Bài 3.2 - Giá vé xem phim",
        ham,
        [
            Case(args=(4, False), expected=0, mo_ta="dưới 6 tuổi miễn phí"),
            Case(args=(10, False), expected=45000),
            Case(args=(10, True), expected=60000, mo_ta="trẻ em, suất tối"),
            Case(args=(25, False), expected=75000),
            Case(args=(25, True), expected=100000),
            Case(args=(70, True), expected=50000, mo_ta="người cao tuổi, đồng giá"),
        ],
    )


# --------------------------------------------------------------------------
# Dự án tuần 1
# --------------------------------------------------------------------------

def kiem_tra_du_an(ham) -> bool:
    """quyet_dinh_lai_xe(khoang_cach, toc_do, muc_pin) -> str.

    Thứ tự ưu tiên: DUNG_KHAN_CAP > VE_TRAM_SAC > GIAM_TOC > BINH_THUONG
    """
    return kiem_tra(
        "Dự án tuần 1 - Bộ ra quyết định lái xe",
        ham,
        [
            Case(args=(1.5, 30, 80), expected="DUNG_KHAN_CAP"),
            Case(args=(1.5, 30, 5), expected="DUNG_KHAN_CAP", mo_ta="an toàn ưu tiên hơn pin"),
            Case(args=(20.0, 40, 10), expected="VE_TRAM_SAC"),
            Case(args=(4.0, 40, 90), expected="GIAM_TOC", mo_ta="vật cản gần"),
            Case(args=(30.0, 75, 90), expected="GIAM_TOC", mo_ta="chạy quá 60 km/h"),
            Case(args=(30.0, 50, 90), expected="BINH_THUONG"),
            Case(args=(5.0, 60, 15), expected="GIAM_TOC", mo_ta="đúng các giá trị biên"),
        ],
    )