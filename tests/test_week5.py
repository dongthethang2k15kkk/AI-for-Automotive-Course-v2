"""Bộ test tuần 5 - Thuật toán cốt lõi & Bảng băm."""

from __future__ import annotations

try:
    from .runner import Case, kiem_tra
except ImportError:
    from runner import Case, kiem_tra


# --------------------------------------------------------------------------
# Bài 1 (Dự án cấp chứng chỉ 5): Đệ quy - Tháp Hà Nội
# --------------------------------------------------------------------------

def kiem_tra_1_1(ham) -> bool:
    """thap_ha_noi(so_dia, cot_nguon="A", cot_dich="C", cot_trung_gian="B") -> list[tuple].

    Trả về danh sách các bước di chuyển theo đúng thứ tự thực hiện, mỗi bước là
    tuple `(cot_nguon, cot_dich)`. Phải theo đúng chiến lược đệ quy chuẩn:
    chuyển (n-1) đĩa sang cột trung gian -> chuyển đĩa lớn nhất sang đích ->
    chuyển (n-1) đĩa từ trung gian sang đích. Có vậy thứ tự bước mới xác định
    được (không phải giải nào "đúng kiểu chuyển 3 cột" cũng cho cùng thứ tự).
    """
    return kiem_tra(
        "Bài 1.1 - Tháp Hà Nội",
        ham,
        [
            Case(args=(1,), expected=[("A", "C")], mo_ta="1 đĩa"),
            Case(args=(2,), expected=[("A", "B"), ("A", "C"), ("B", "C")], mo_ta="2 đĩa"),
            Case(
                args=(3,),
                expected=[("A", "C"), ("A", "B"), ("C", "B"), ("A", "C"), ("B", "A"), ("B", "C"), ("A", "C")],
                mo_ta="3 đĩa - đúng 7 bước (2^3 - 1)",
            ),
        ],
    )


# --------------------------------------------------------------------------
# Bài 2: Sắp xếp và Tìm kiếm
# --------------------------------------------------------------------------

def kiem_tra_2_1(ham) -> bool:
    """sap_xep_vat_can(danh_sach) -> list, sắp theo "khoang_cach" tăng dần (Merge Sort).

    Mỗi phần tử của danh_sach là dict có khoá "ten" và "khoang_cach".
    """
    return kiem_tra(
        "Bài 2.1 - Sắp xếp mảng vật cản (Merge Sort)",
        ham,
        [
            Case(
                args=([
                    {"ten": "a", "khoang_cach": 5.0},
                    {"ten": "b", "khoang_cach": 1.0},
                    {"ten": "c", "khoang_cach": 3.0},
                ],),
                expected=[
                    {"ten": "b", "khoang_cach": 1.0},
                    {"ten": "c", "khoang_cach": 3.0},
                    {"ten": "a", "khoang_cach": 5.0},
                ],
            ),
            Case(args=([],), expected=[], mo_ta="danh sách rỗng"),
            Case(args=([{"ten": "solo", "khoang_cach": 2.0}],), expected=[{"ten": "solo", "khoang_cach": 2.0}], mo_ta="1 phần tử"),
        ],
    )


def kiem_tra_2_2(ham) -> bool:
    """binary_search_log(log_timestamps, target_time) -> index hoặc -1 nếu không tìm thấy."""
    return kiem_tra(
        "Bài 2.2 - Tìm kiếm nhị phân trong log",
        ham,
        [
            Case(args=([100, 150, 200, 250, 300, 350, 400], 250), expected=3),
            Case(args=([100, 150, 200, 250, 300, 350, 400], 999), expected=-1, mo_ta="không tồn tại"),
            Case(args=([100], 100), expected=0, mo_ta="mảng chỉ có 1 phần tử"),
        ],
    )


# --------------------------------------------------------------------------
# Dự án 4 - Hash Table tự cài đặt
# --------------------------------------------------------------------------

def _chay_kich_ban_bb(TenLop, so_kich_ban):
    if so_kich_ban == 1:
        bb = TenLop()
        bb.insert("a", 1)
        return bb.get("a")
    if so_kich_ban == 2:
        bb = TenLop()
        return bb.get("khong_ton_tai")
    if so_kich_ban == 3:
        bb = TenLop()
        bb.insert("x", 1)
        bb.insert("x", 2)  # insert lại cùng khoá -> phải ghi đè, không nhân đôi
        return bb.get("x")
    if so_kich_ban == 4:
        bb = TenLop()
        bb.insert("y", 5)
        da_xoa = bb.delete("y")
        return (da_xoa, bb.get("y"))
    if so_kich_ban == 5:
        bb = TenLop()
        return bb.delete("khong_ton_tai")
    if so_kich_ban == 6:
        # kich_thuoc=1 -> ép mọi khoá vào CÙNG một ngăn để kiểm tra xử lý xung đột
        bb = TenLop(kich_thuoc=1)
        bb.insert("a", 1)
        bb.insert("b", 2)
        return (bb.get("a"), bb.get("b"))
    raise ValueError(f"kịch bản không hợp lệ: {so_kich_ban}")


def kiem_tra_du_an(TenLop) -> bool:
    """class BangBam tự cài đặt bằng list (KHÔNG dùng dict/set có sẵn của Python).

    __init__(self, kich_thuoc=16)
    insert(self, khoa, gia_tri) -> nếu khoa đã tồn tại thì GHI ĐÈ giá trị, không thêm trùng
    get(self, khoa) -> giá trị, hoặc None nếu không tồn tại
    delete(self, khoa) -> True nếu xoá được, False nếu khoá không tồn tại
    Phải tự viết hàm băm và xử lý xung đột (2 khoá cùng rơi vào 1 ngăn vẫn phải
    truy xuất đúng, xem kịch bản 6 dùng kich_thuoc=1 để ép xung đột).
    """
    ham = lambda so: _chay_kich_ban_bb(TenLop, so)
    return kiem_tra(
        "Dự án tuần 5 - Bảng băm tự cài đặt",
        ham,
        [
            Case(args=(1,), expected=1, mo_ta="insert rồi get"),
            Case(args=(2,), expected=None, mo_ta="get khoá không tồn tại"),
            Case(args=(3,), expected=2, mo_ta="insert 2 lần cùng khoá -> ghi đè"),
            Case(args=(4,), expected=(True, None), mo_ta="xoá rồi get lại phải ra None"),
            Case(args=(5,), expected=False, mo_ta="xoá khoá không tồn tại"),
            Case(args=(6,), expected=(1, 2), mo_ta="2 khoá cùng ngăn (xung đột) vẫn phải lấy đúng giá trị từng khoá"),
        ],
    )