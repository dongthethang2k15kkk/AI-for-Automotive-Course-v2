"""Bộ test tuần 6 - Cấu trúc dữ liệu phi tuyến (Đồ thị, Cây) & Tổng kết."""

from __future__ import annotations

try:
    from .runner import Case, kiem_tra
except ImportError:
    from runner import Case, kiem_tra


# --------------------------------------------------------------------------
# Bài 1: Cây tìm kiếm nhị phân (BST)
# --------------------------------------------------------------------------

_KICH_BAN_BST = {
    1: [5, 3, 8, 1, 4],
    2: [10],
    3: [7, 7, 7],
    4: [20, 10, 30, 5, 15, 25, 35, 1],
}


def _chay_kich_ban_bst(NutBST, chen_bst, tim_nho_nhat, so_kich_ban):
    danh_sach_gia_tri = _KICH_BAN_BST[so_kich_ban]
    goc = None
    for gia_tri in danh_sach_gia_tri:
        goc = chen_bst(goc, gia_tri)
    return tim_nho_nhat(goc)


def kiem_tra_1_1(NutBST, chen_bst, tim_nho_nhat) -> bool:
    """class NutBST + 2 hàm chen_bst và tim_nho_nhat.

    class NutBST: __init__(self, gia_tri) -> self.gia_tri, self.trai=None, self.phai=None
    chen_bst(goc, gia_tri) -> chèn gia_tri vào cây BST có gốc `goc` (đệ quy),
        trả về NÚT GỐC (tạo mới nếu goc là None). Quy tắc: nhỏ hơn -> rẽ trái,
        lớn hơn hoặc bằng -> rẽ phải.
    tim_nho_nhat(goc) -> trả về giá trị nhỏ nhất trong cây (đệ quy rẽ trái liên tục).
    """
    ham = lambda so: _chay_kich_ban_bst(NutBST, chen_bst, tim_nho_nhat, so)
    return kiem_tra(
        "Bài 1.1 - Cây tìm kiếm nhị phân (tìm vật cản gần nhất)",
        ham,
        [
            Case(args=(1,), expected=1, mo_ta="chèn [5,3,8,1,4] -> nhỏ nhất là 1"),
            Case(args=(2,), expected=10, mo_ta="cây chỉ có 1 node"),
            Case(args=(3,), expected=7, mo_ta="toàn giá trị trùng nhau"),
            Case(args=(4,), expected=1, mo_ta="cây lớn hơn, nhiều tầng"),
        ],
    )


# --------------------------------------------------------------------------
# Bài 2: Đồ thị (DFS) và Quy hoạch động
# --------------------------------------------------------------------------

def kiem_tra_2_1(ham) -> bool:
    """tim_tat_ca_duong_di(do_thi, diem_dau, diem_cuoi, duong_di=None) -> list[list].

    do_thi là dict biểu diễn Danh sách kề. Trả về TẤT CẢ các đường đi khả thi từ
    diem_dau tới diem_cuoi (không lặp lại đỉnh trong một đường đi), theo đúng thứ
    tự duyệt DFS (duyệt láng giềng theo đúng thứ tự xuất hiện trong list của
    do_thi[node]).
    """
    return kiem_tra(
        "Bài 2.1 - Tìm tất cả đường đi bằng DFS",
        ham,
        [
            Case(
                args=({"A": ["B", "C"], "B": ["A", "D"], "C": ["A", "D"], "D": ["B", "C", "E"]}, "A", "E"),
                expected=[["A", "B", "D", "E"], ["A", "C", "D", "E"]],
            ),
            Case(
                args=({"A": ["B"], "B": ["A"]}, "A", "A"),
                expected=[["A"]],
                mo_ta="điểm đầu trùng điểm cuối",
            ),
            Case(
                args=({"A": ["B"], "B": []}, "A", "C"),
                expected=[],
                mo_ta="không có đường đi nào tới đích",
            ),
        ],
    )


def kiem_tra_2_2(ham) -> bool:
    """fibonacci_memo(n, cache=None) -> số Fibonacci thứ n (fib(0)=0, fib(1)=1), có memoization."""
    return kiem_tra(
        "Bài 2.2 - Fibonacci với Memoization",
        ham,
        [
            Case(args=(0,), expected=0),
            Case(args=(1,), expected=1),
            Case(args=(10,), expected=55),
            Case(args=(20,), expected=6765, mo_ta="n lớn - nếu không memoization sẽ chạy rất chậm"),
        ],
    )