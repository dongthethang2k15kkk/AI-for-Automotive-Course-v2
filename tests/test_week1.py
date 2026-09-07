"""Bộ test tuần 1 - Nền tảng & Cú pháp cơ bản.

Tuần 1 chấm theo hai kiểu, tuỳ bài đã dạy tới đâu:

  - Bài 1 đến Bài 3 chưa có `def`, nên các hàm kiem_tra_* nhận thẳng GIÁ TRỊ biến
    học viên đã gán. Gọi ví dụ: kiem_tra_1_1(diem_tb_1, diem_tb_2)
  - Bài 4 và Dự án đã dạy `def`, nên nhận HÀM và tự chọn đầu vào để gọi.
    Gọi ví dụ: kiem_tra_4_1(canh_bao_vat_can)
"""

from __future__ import annotations

try:
    from .runner import Case, kiem_tra, kiem_tra_gia_tri
except ImportError:  # khi chạy trực tiếp trong Colab, không qua package
    from runner import Case, kiem_tra, kiem_tra_gia_tri


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
    """bao_cao -> chuỗi f-string đúng mẫu, quãng đường = 20.0 * 3."""
    return kiem_tra_gia_tri(
        "Bài 2.2 - Báo cáo quãng đường",
        [
            ("bao_cao", bao_cao, "Xe đã đi được 60.0 mét trong 3 giây."),
        ],
    )


def kiem_tra_2_3(gio, phut, giay) -> bool:
    """gio, phut, giay -> đổi 5000 giây bằng // và %."""
    return kiem_tra_gia_tri(
        "Bài 2.3 - Đổi giây sang giờ phút giây",
        [
            ("gio (5000 giây)", gio, 1),
            ("phut (5000 giây)", phut, 23),
            ("giay (5000 giây)", giay, 20),
        ],
    )


# --------------------------------------------------------------------------
# Bài 3: Boolean và câu lệnh điều kiện - chấm theo giá trị, mỗi bài một trường hợp
# --------------------------------------------------------------------------

def kiem_tra_3_1(trang_thai) -> bool:
    """trang_thai -> phân loại khoang_cach = 3.7 theo bảng ngưỡng."""
    return kiem_tra_gia_tri(
        "Bài 3.1 - Cảnh báo vật cản",
        [
            ("trang_thai (khoang_cach = 3.7)", trang_thai, "GIAM_TOC"),
        ],
    )


def kiem_tra_3_2(gioi_han) -> bool:
    """gioi_han -> tốc độ cho phép trên duong_tinh khi trời mưa."""
    return kiem_tra_gia_tri(
        "Bài 3.2 - Giới hạn tốc độ",
        [
            ('gioi_han (loai_duong = "duong_tinh", troi_mua = True)', gioi_han, 60),
        ],
    )


# --------------------------------------------------------------------------
# Bài 4: Hàm - chấm bằng cách gọi hàm với đầu vào do bộ chấm chọn
# --------------------------------------------------------------------------

def kiem_tra_4_1(canh_bao_vat_can) -> bool:
    """canh_bao_vat_can(khoang_cach) -> chuỗi cảnh báo, kiểm cả giá trị biên."""
    return kiem_tra(
        "Bài 4.1 - Hàm cảnh báo vật cản",
        canh_bao_vat_can,
        [
            Case(args=(0.5,), expected="PHANH_KHAN_CAP", mo_ta="canh_bao_vat_can(0.5)"),
            Case(args=(2.0,), expected="PHANH_KHAN_CAP", mo_ta="canh_bao_vat_can(2.0) - biên dưới"),
            Case(args=(3.7,), expected="GIAM_TOC", mo_ta="canh_bao_vat_can(3.7)"),
            Case(args=(5.0,), expected="GIAM_TOC", mo_ta="canh_bao_vat_can(5.0) - biên trên"),
            Case(args=(12.0,), expected="AN_TOAN", mo_ta="canh_bao_vat_can(12.0)"),
        ],
    )


def kiem_tra_4_2(gioi_han_toc_do) -> bool:
    """gioi_han_toc_do(loai_duong, troi_mua) -> giới hạn km/h theo bảng hai chiều."""
    return kiem_tra(
        "Bài 4.2 - Hàm giới hạn tốc độ",
        gioi_han_toc_do,
        [
            Case(args=("khu_truong_hoc", False), expected=30,
                 mo_ta='gioi_han_toc_do("khu_truong_hoc", False)'),
            Case(args=("khu_truong_hoc", True), expected=30,
                 mo_ta='gioi_han_toc_do("khu_truong_hoc", True) - mưa không đổi'),
            Case(args=("khu_dan_cu", False), expected=50,
                 mo_ta='gioi_han_toc_do("khu_dan_cu", False)'),
            Case(args=("khu_dan_cu", True), expected=40,
                 mo_ta='gioi_han_toc_do("khu_dan_cu", True)'),
            Case(args=("duong_tinh", True), expected=60,
                 mo_ta='gioi_han_toc_do("duong_tinh", True)'),
            Case(args=("cao_toc", False), expected=120,
                 mo_ta='gioi_han_toc_do("cao_toc", False)'),
            Case(args=("cao_toc", True), expected=90,
                 mo_ta='gioi_han_toc_do("cao_toc", True)'),
        ],
    )


# --------------------------------------------------------------------------
# Dự án tuần 1
# --------------------------------------------------------------------------

def kiem_tra_du_an(quyet_dinh_lai_xe) -> bool:
    """quyet_dinh_lai_xe(khoang_cach, toc_do, muc_pin) -> mã lệnh, xét theo ưu tiên."""
    return kiem_tra(
        "Dự án tuần 1 - Bộ ra quyết định lái xe",
        quyet_dinh_lai_xe,
        [
            Case(args=(1.5, 30, 5), expected="DUNG_KHAN_CAP",
                 mo_ta="vật cản 1.5 m, pin 5% - an toàn xét trước pin"),
            Case(args=(2.0, 30, 90), expected="DUNG_KHAN_CAP",
                 mo_ta="vật cản đúng 2.0 m - biên"),
            Case(args=(20.0, 40, 10), expected="VE_TRAM_SAC",
                 mo_ta="đường thoáng, pin 10%"),
            Case(args=(20.0, 40, 15), expected="BINH_THUONG",
                 mo_ta="pin đúng 15% - biên, chưa phải về sạc"),
            Case(args=(30.0, 75, 90), expected="GIAM_TOC",
                 mo_ta="tốc độ 75 km/h"),
            Case(args=(4.0, 50, 90), expected="GIAM_TOC",
                 mo_ta="vật cản 4.0 m"),
            Case(args=(30.0, 50, 90), expected="BINH_THUONG",
                 mo_ta="mọi thứ trong ngưỡng"),
        ],
    )
