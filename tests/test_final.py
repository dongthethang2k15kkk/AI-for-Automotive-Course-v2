"""Bộ test đề thi cuối khóa - trắc nghiệm (băm đáp án) + bài code."""

from __future__ import annotations
import hashlib

try:
    from .runner import Case, kiem_tra
except ImportError:
    from runner import Case, kiem_tra


# --------------------------------------------------------------------------
# Phần 1: Trắc nghiệm (20 câu) - đáp án được BĂM, không lưu dạng chữ thô
# --------------------------------------------------------------------------

_MA_DAP_AN = {
    1: "af63f7236e2d940cb0b07371f09e1be23d027163d72db26946ba889ce9e038ae",
    2: "0f1b8a6928099f9f444b01bbc4d8ce15d1143f5e771c03398acc1e275476882b",
    3: "f21f96aa5c6df6c39335b50335fdc5a2ece0858b7d02db8f9ff30f08994327ca",
    4: "5d1f105a09e7bfe031f889b71bd6798748293443b79c2826edfeb0777427609e",
    5: "1771f0ee7d52a6595d25bf26063102a8873ec3392475ecde53f5ab28fea57427",
    6: "8e796ae7582dce9a698f318b4ab840a6d55c2f44b9b16230f0abd6c7d3f66f7a",
    7: "219a5bf00a1a79248048579332aa03d56d526965d4b934a431a68160cf1a8bee",
    8: "ca4ac03f2b4fca5cd0762de61696eb19bec0fdeb7f560c3d86b9573b578b9d57",
    9: "72331365d78d03a32bc4126b6faef0ec336b23b4c31b71a1122a316e62d11d1c",
    10: "c7d9e5b40e31aabb0667396959cc781552c0876620b1a3c45a2abd816af54f29",
    11: "94a0fa92ac1916b2b197c82bd2bd9d094b4fb5d235c0537a37b22cc3609d54d2",
    12: "961072f9494a3816947ef25ea34d8e5bb37af7a8af9f5ee2ffa78702c2da9cd2",
    13: "2d1e42aa5b8ba9f4623bea4dd1832357ba89430fdd6a1a4a2f84112576e776a7",
    14: "07c1dffef22f03fd40c6c5e88042baf275266630b8aef3938a91ee7003c19867",
    15: "1f80117448280a688fe3856ea6e9e2a2f62fcc3329fe7c15050a25a43fde368a",
    16: "30617187817083e4224ee817bb952e0104ebe252c09611e8f0dcdd21cccd40bd",
    17: "5a7d196b08caff5e63321ea7e6274b8ddefe860c93d68bf82cc7ed17ff93fdb2",
    18: "e7c9e0ba0fa98be85ce155f3a60e18ac0662b83330313970f03248abac959a2c",
    19: "21698b1c35e3f7d3b66ce8b2eaf894d30eb075724dbfffc4f2c71b42ba9f24ab",
    20: "8b110bed77f095de2375abd422c1c990d091aa1c225eb166a356dda116598f4f",
}


def _bam(so_cau: int, dap_an: str) -> str:
    chuan_hoa = str(dap_an).strip().upper()
    return hashlib.sha256(f"cau_{so_cau}:{chuan_hoa}".encode()).hexdigest()


def kiem_tra_cau(so_cau: int, dap_an: str) -> bool:
    """Chấm 1 câu trắc nghiệm. dap_an: 'A' | 'B' | 'C' | 'D' (không phân biệt hoa/thường)."""
    dung = _bam(so_cau, dap_an) == _MA_DAP_AN[so_cau]
    trang_thai = "DUNG" if dung else "SAI"
    print(f"Cau {so_cau}: ban chon '{str(dap_an).strip().upper()}' -> {trang_thai}")
    return dung


def kiem_tra_toan_bo_trac_nghiem(dap_an_cua_ban: dict) -> bool:
    """dap_an_cua_ban: dict {so_cau: chu_cai}, ví dụ {1: "B", 2: "D", ...}."""
    print("=== KET QUA TRAC NGHIEM ===")
    so_dung = 0
    for so_cau in range(1, 21):
        dap_an = dap_an_cua_ban.get(so_cau, "")
        if kiem_tra_cau(so_cau, dap_an):
            so_dung += 1
    print(f"\nTONG DIEM TRAC NGHIEM: {so_dung}/20")
    return so_dung == 20


# --------------------------------------------------------------------------
# Phần 2: Bài code - Tối ưu hoá lịch trình quét Lidar (Merge Intervals)
# --------------------------------------------------------------------------

def kiem_tra_gop_khung(ham) -> bool:
    """gop_khung_thoi_gian(intervals) -> list các [start, end] đã gộp, sắp theo start tăng dần.

    Yêu cầu độ phức tạp O(n log n): sắp xếp trước, sau đó duyệt 1 lượt để gộp.
    """
    return kiem_tra(
        "Bai thuc hanh - Gop khung thoi gian quet Lidar",
        ham,
        [
            Case(args=([[1, 3], [2, 6], [8, 10], [15, 18]],), expected=[[1, 6], [8, 10], [15, 18]]),
            Case(args=([[1, 4], [4, 5]],), expected=[[1, 5]], mo_ta="chạm nhau tại mốc 4 vẫn phải gộp"),
            Case(args=([[5, 8], [1, 3]],), expected=[[1, 3], [5, 8]], mo_ta="đầu vào CHƯA sắp xếp"),
            Case(args=([[1, 10]],), expected=[[1, 10]], mo_ta="chỉ 1 khung"),
            Case(args=([],), expected=[], mo_ta="danh sách rỗng"),
            Case(args=([[1, 2], [3, 4], [5, 6]],), expected=[[1, 2], [3, 4], [5, 6]], mo_ta="không khung nào chồng chéo"),
        ],
    )