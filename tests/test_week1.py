"""Bộ test tuần 1 - Nền tảng & Cú pháp cơ bản.

Tuần 1 chưa dạy `def`, nên các hàm kiem_tra_* ở đây nhận thẳng GIÁ TRỊ biến học
viên đã gán trong notebook, không nhận hàm. Gọi ví dụ: kiem_tra_1_1(diem_tb_1, diem_tb_2)
"""

from __future__ import annotations

try:
    from .runner import kiem_tra_gia_tri
except ImportError:  # khi chạy trực tiếp trong Colab, không qua package
    from runner import kiem_tra_gia_tri


# --------------------------------------------------------------------------
# Bài 1: Biến và kiểu dữ liệu
# --------------------------------------------------------------------------

def kiem_tra_1_1(diem_tb_1, diem_tb_2) -> bool:
    """diem_tb_1, diem_tb_2 -> trung bình cộng ba môn, không làm tròn."""
    return kiem_tra_gia_tri(
        "Bài 1.1 - Điểm trung bình",
        [
            ("diem_tb_1 (toan=8, ly=9, hoa=10)", diem_tb_1, (8 + 9 + 10) / 3),
            ("diem_tb_2 (toan=7.5, ly=6, hoa=8)", diem_tb_2, (7.5 + 6 + 8) / 3),
        ],
    )


def kiem_tra_1_2(noi_chuoi, tong_so) -> bool:
    """noi_chuoi -> nối chuỗi "20" với "5". tong_so -> ép "20" sang số rồi +5."""
    return kiem_tra_gia_tri(
        "Bài 1.2 - Ép kiểu dữ liệu",
        [
            ("noi_chuoi (gia_tri_tho_2 + \"5\")", noi_chuoi, "205"),
            ("tong_so (int(gia_tri_tho_2) + 5)", tong_so, 25),
        ],
    )


# --------------------------------------------------------------------------
# Bài 2: Toán tử, chuỗi và ép kiểu
# --------------------------------------------------------------------------

def kiem_tra_2_1(moi_nguoi_tra_1, moi_nguoi_tra_2) -> bool:
    """moi_nguoi_tra_1, moi_nguoi_tra_2 -> tiền mỗi người sau tip, làm tròn 2 chữ số."""
    return kiem_tra_gia_tri(
        "Bài 2.1 - Chia hoá đơn",
        [
            ("moi_nguoi_tra_1 (300000, tip 10%, 3 người)", moi_nguoi_tra_1, 110000.0),
            ("moi_nguoi_tra_2 (100000, tip 15%, 3 người)", moi_nguoi_tra_2, 38333.33),
        ],
    )


def kiem_tra_2_2(bao_cao) -> bool:
    """bao_cao -> chuỗi đúng mẫu, van_toc_bc=20.0, thoi_gian_bc=3."""
    return kiem_tra_gia_tri(
        "Bài 2.2 - Báo cáo quãng đường",
        [
            ("bao_cao", bao_cao, "Xe đã đi được 60.0 mét trong 3 giây."),
        ],
    )


def kiem_tra_2_3(gio, phut, giay) -> bool:
    """gio, phut, giay -> đổi tong_giay_bt=5000 sang giờ/phút/giây."""
    return kiem_tra_gia_tri(
        "Bài 2.3 - Đổi giây sang giờ phút giây",
        [
            ("gio (5000 giây)", gio, 1),
            ("phut (5000 giây)", phut, 23),
            ("giay (5000 giây)", giay, 20),
        ],
    )


# --------------------------------------------------------------------------
# Bài 3: Boolean và câu lệnh điều kiện
# --------------------------------------------------------------------------

def kiem_tra_3_1(trang_thai_a, trang_thai_b, trang_thai_c, trang_thai_d) -> bool:
    """trang_thai_a..d -> phân loại theo khoang_cach_a=0.5, _b=2.0, _c=5.0, _d=12.0."""
    return kiem_tra_gia_tri(
        "Bài 3.1 - Cảnh báo vật cản",
        [
            ("trang_thai_a (khoang_cach_a=0.5)", trang_thai_a, "PHANH_KHAN_CAP"),
            ("trang_thai_b (khoang_cach_b=2.0, biên)", trang_thai_b, "PHANH_KHAN_CAP"),
            ("trang_thai_c (khoang_cach_c=5.0, biên)", trang_thai_c, "GIAM_TOC"),
            ("trang_thai_d (khoang_cach_d=12.0)", trang_thai_d, "AN_TOAN"),
        ],
    )


def kiem_tra_3_2(gia_ve_1, gia_ve_2, gia_ve_3) -> bool:
    """gia_ve_1..3 -> giá vé theo bảng tuổi/suất chiếu."""
    return kiem_tra_gia_tri(
        "Bài 3.2 - Giá vé xem phim",
        [
            ("gia_ve_1 (4 tuổi, suất sáng)", gia_ve_1, 0),
            ("gia_ve_2 (10 tuổi, suất tối)", gia_ve_2, 60000),
            ("gia_ve_3 (70 tuổi, suất tối)", gia_ve_3, 50000),
        ],
    )


# --------------------------------------------------------------------------
# Dự án tuần 1
# --------------------------------------------------------------------------

def kiem_tra_du_an(lenh_1, lenh_2, lenh_3, lenh_4) -> bool:
    """lenh_1..4 -> mã lệnh theo thứ tự ưu tiên DUNG_KHAN_CAP > VE_TRAM_SAC > GIAM_TOC > BINH_THUONG."""
    return kiem_tra_gia_tri(
        "Dự án tuần 1 - Bộ ra quyết định lái xe",
        [
            ("lenh_1 (khoang_cach=1.5, toc_do=30, muc_pin=5)", lenh_1, "DUNG_KHAN_CAP"),
            ("lenh_2 (khoang_cach=20.0, toc_do=40, muc_pin=10)", lenh_2, "VE_TRAM_SAC"),
            ("lenh_3 (khoang_cach=30.0, toc_do=75, muc_pin=90)", lenh_3, "GIAM_TOC"),
            ("lenh_4 (khoang_cach=30.0, toc_do=50, muc_pin=90)", lenh_4, "BINH_THUONG"),
        ],
    )
