"""Giao diện thi trắc nghiệm bằng ipywidgets cho đề thi cuối khóa.

Hai hàm dùng trong final_test.py: bat_dau_thi(...) dựng giao diện, bang_diem(...) in
thẻ kết quả cuối cùng. Không chứa đề bài (nằm ở de_thi_cau_hoi.py), không chứa đáp án
thô (chỉ dò qua bản băm trong test_final.py).

Ba nhánh thoái hoá, không nhánh nào được ném lỗi ra ngoài:
  1. AUTOGRADE=1 (máy chấm GitHub Actions, không cài ipywidgets) -> in một dòng, thoát.
  2. Không có ipywidgets (Jupyter/VS Code chưa cài) -> in bản chữ toàn bộ đề, thoát.
  3. Dựng widget lỗi vì lý do khác -> bắt hết, in một dòng cảnh báo, thoát.
"""

from __future__ import annotations

import html
import os
import re

try:
    from .de_thi_cau_hoi import CAU_HOI
    from .test_final import _MA_DAP_AN, _bam
except ImportError:
    from de_thi_cau_hoi import CAU_HOI
    from test_final import _MA_DAP_AN, _bam


def _dap_an_dung(so_cau: int) -> str:
    for chu in "ABCD":
        if _bam(so_cau, chu) == _MA_DAP_AN[so_cau]:
            return chu
    return "?"


def _bo_backtick(s: str) -> str:
    return s.replace("`", "")


def _dinh_dang_html(s: str) -> str:
    """Escape HTML, giữ lại đoạn trong dấu backtick dưới dạng <code>."""
    phan = re.split(r"(`[^`]*`)", s)
    ra = []
    for p in phan:
        if p.startswith("`") and p.endswith("`") and len(p) >= 2:
            ra.append("<code>" + html.escape(p[1:-1]) + "</code>")
        else:
            ra.append(html.escape(p))
    return "".join(ra)


def _co_ipywidgets() -> bool:
    try:
        import ipywidgets  # noqa: F401
        return True
    except ImportError:
        return False


def _in_de_bang_chu() -> None:
    print("Khong tim thay ipywidgets trong moi truong nay.")
    print("Sua truc tiep dict dap_an_cua_ban ben tren: gan chu cai A/B/C/D cho tung")
    print("so cau, roi chay o kiem_tra_toan_bo_trac_nghiem ben duoi.")
    for q in CAU_HOI:
        print(f"\nCau {q['so']}: {_bo_backtick(q['de'])}")
        for k in "ABCD":
            print(f"  {k}. {_bo_backtick(q['lua_chon'][k])}")


CSS = """
<style>
.bkauto-container { max-width: 820px; font-family: -apple-system, "Segoe UI", Roboto, sans-serif; }
.bkauto-title { font-size: 1.05em; font-weight: 600; margin: 4px 0 8px 0; }
.bkauto-card { background: rgba(127,127,127,0.08); border: 1px solid rgba(127,127,127,0.35);
  border-radius: 8px; padding: 12px 14px; margin: 8px 0; }
.bkauto-qnum { font-weight: 600; opacity: 0.75; margin-bottom: 4px; }
.bkauto-qtext { font-size: 1.02em; margin-bottom: 4px; line-height: 1.4; }
.bkauto-qtext code, .bkauto-review-card code { background: rgba(127,127,127,0.18);
  padding: 1px 4px; border-radius: 4px; font-family: "Courier New", monospace; }
.bkauto-canhbao { color: #b45309; font-weight: 600; padding: 4px 0; min-height: 1.2em; }
.bkauto-legend { opacity: 0.7; font-size: 0.85em; margin-top: 4px; }
.bkauto-done { background: rgba(63,174,78,0.35) !important; }
.bkauto-current { border: 2px solid #3b82f6 !important; }
.bkauto-score { border-radius: 8px; padding: 14px; margin-top: 10px;
  background: rgba(127,127,127,0.10); border: 1px solid rgba(127,127,127,0.35); }
.bkauto-review-card { border-radius: 6px; padding: 8px 10px; margin: 6px 0; border-left: 4px solid; }
.bkauto-review-ok { border-color: #3fae4e; background: rgba(63,174,78,0.08); }
.bkauto-review-bad { border-color: #e5484d; background: rgba(229,72,77,0.08); }
.bkauto-review-line { margin-top: 4px; font-weight: 600; }
.bkauto-review-giai { margin-top: 4px; opacity: 0.85; }
.bkauto-review-tuan { margin-top: 4px; font-size: 0.8em; opacity: 0.6; }
</style>
"""


def _dung_giao_dien(dap_an_cua_ban: dict, hien_dap_an_khi_xem_lai: bool, widgets, display):
    trang_thai = {"idx": 0, "da_nop": False, "xac_nhan_nop": False, "dang_dat_lai": False}

    style_html = widgets.HTML(value=CSS)
    tieu_de = widgets.HTML(value="<div class='bkauto-title'>ĐỀ THI CUỐI KHOÁ · Phần trắc nghiệm</div>")

    thanh_tien_trinh = widgets.IntProgress(min=0, max=20, value=0, layout=widgets.Layout(width="60%"))
    nhan_tien_trinh = widgets.HTML(value="0/20 câu đã trả lời")
    hang_tien_trinh = widgets.HBox([thanh_tien_trinh, nhan_tien_trinh])

    de_html = widgets.HTML(value="")
    radio = widgets.RadioButtons(options=[], layout=widgets.Layout(width="100%"))
    the_cau_hoi = widgets.VBox([de_html, radio])
    the_cau_hoi.add_class("bkauto-card")

    canh_bao_html = widgets.HTML(value="")

    nut_truoc = widgets.Button(description="< Câu trước")
    nut_sau = widgets.Button(description="Câu sau >")
    nut_nop = widgets.Button(description="NỘP BÀI", button_style="success")
    hang_dieu_huong = widgets.HBox([nut_truoc, nut_sau, nut_nop])

    nut_luoi = [
        widgets.Button(description=str(i + 1), layout=widgets.Layout(width="32px", height="30px", margin="1px"))
        for i in range(20)
    ]
    luoi = widgets.GridBox(
        children=nut_luoi,
        layout=widgets.Layout(grid_template_columns="repeat(10, 1fr)", grid_gap="2px"),
    )
    chu_thich = widgets.HTML(
        value="<div class='bkauto-legend'>xanh đậm = đã trả lời &nbsp; viền xanh dương = câu đang xem</div>"
    )

    vung_diem = widgets.VBox([])

    container = widgets.VBox(
        [style_html, tieu_de, hang_tien_trinh, the_cau_hoi, canh_bao_html, hang_dieu_huong, luoi, chu_thich, vung_diem]
    )
    container.add_class("bkauto-container")

    def _cap_nhat_tien_trinh():
        dem = sum(1 for v in dap_an_cua_ban.values() if v in ("A", "B", "C", "D"))
        thanh_tien_trinh.value = dem
        nhan_tien_trinh.value = f"{dem}/20 câu đã trả lời"

    def _cap_nhat_luoi():
        for i, nut in enumerate(nut_luoi):
            so = i + 1
            nut.remove_class("bkauto-done")
            nut.remove_class("bkauto-current")
            if dap_an_cua_ban.get(so, "?") in ("A", "B", "C", "D"):
                nut.add_class("bkauto-done")
            if i == trang_thai["idx"]:
                nut.add_class("bkauto-current")

    def _hien_cau(idx):
        idx = max(0, min(19, idx))
        trang_thai["idx"] = idx
        q = CAU_HOI[idx]
        so = q["so"]
        de_html.value = (
            f"<div class='bkauto-qnum'>Câu {so} / 20</div>"
            f"<div class='bkauto-qtext'>{_dinh_dang_html(q['de'])}</div>"
        )
        trang_thai["dang_dat_lai"] = True
        radio.options = [(f"{k}. {_bo_backtick(q['lua_chon'][k])}", k) for k in "ABCD"]
        hien_tai = dap_an_cua_ban.get(so, "?")
        radio.value = hien_tai if hien_tai in ("A", "B", "C", "D") else None
        trang_thai["dang_dat_lai"] = False
        nut_truoc.disabled = idx == 0
        nut_sau.disabled = idx == 19
        _cap_nhat_luoi()

    def _khi_chon(change):
        if trang_thai["dang_dat_lai"] or trang_thai["da_nop"]:
            return
        if change["name"] != "value" or change["new"] not in ("A", "B", "C", "D"):
            return
        so = CAU_HOI[trang_thai["idx"]]["so"]
        dap_an_cua_ban[so] = change["new"]
        _cap_nhat_tien_trinh()
        _cap_nhat_luoi()

    radio.observe(_khi_chon, names="value")
    nut_truoc.on_click(lambda _: _hien_cau(trang_thai["idx"] - 1))
    nut_sau.on_click(lambda _: _hien_cau(trang_thai["idx"] + 1))

    for i, nut in enumerate(nut_luoi):
        def _tao_handler(idx=i):
            return lambda _: _hien_cau(idx)
        nut.on_click(_tao_handler())

    def _hien_diem():
        so_dung = sum(1 for so in range(1, 21) if dap_an_cua_ban.get(so, "?") == _dap_an_dung(so))
        noi_dung = [
            widgets.HTML(
                value=(
                    "<div class='bkauto-score'>"
                    f"<b>Kết quả tạm thời: {so_dung}/20</b><br>"
                    "Tiêu chí chính thức: đúng toàn bộ 20/20. Chạy ô "
                    "<code>kiem_tra_toan_bo_trac_nghiem(dap_an_cua_ban)</code> bên dưới để "
                    "lưu kết quả chính thức vào file nộp."
                    "</div>"
                )
            )
        ]
        if hien_dap_an_khi_xem_lai:
            nut_xem_lai = widgets.Button(description="Xem chi tiết từng câu")
            khu_xem_lai = widgets.VBox([])
            khu_xem_lai.layout.display = "none"

            def _bam_xem_lai(_):
                if khu_xem_lai.layout.display == "none":
                    if not khu_xem_lai.children:
                        the_xem_lai = []
                        for q in CAU_HOI:
                            so = q["so"]
                            dung_dap = _dap_an_dung(so)
                            chon = dap_an_cua_ban.get(so, "?")
                            dung = chon == dung_dap
                            lop = "bkauto-review-ok" if dung else "bkauto-review-bad"
                            chon_hien = chon if chon in ("A", "B", "C", "D") else "(chưa chọn)"
                            the_xem_lai.append(
                                widgets.HTML(
                                    value=(
                                        f"<div class='bkauto-review-card {lop}'>"
                                        f"<b>Câu {so}.</b> {_dinh_dang_html(q['de'])}"
                                        f"<div class='bkauto-review-line'>Bạn chọn: {chon_hien} "
                                        f"— Đáp án đúng: {dung_dap}</div>"
                                        f"<div class='bkauto-review-giai'>{_dinh_dang_html(q['giai_thich'])}</div>"
                                        f"<div class='bkauto-review-tuan'>Tuần {q['tuan']}</div>"
                                        "</div>"
                                    )
                                )
                            )
                        khu_xem_lai.children = tuple(the_xem_lai)
                    khu_xem_lai.layout.display = None
                    nut_xem_lai.description = "Ẩn chi tiết từng câu"
                else:
                    khu_xem_lai.layout.display = "none"
                    nut_xem_lai.description = "Xem chi tiết từng câu"

            nut_xem_lai.on_click(_bam_xem_lai)
            noi_dung.append(nut_xem_lai)
            noi_dung.append(khu_xem_lai)
        vung_diem.children = tuple(noi_dung)

    def _nop_bai():
        trang_thai["da_nop"] = True
        radio.disabled = True
        nut_truoc.disabled = True
        nut_sau.disabled = True
        nut_nop.disabled = True
        for nut in nut_luoi:
            nut.disabled = True
        canh_bao_html.value = ""
        _hien_diem()

    def _khi_bam_nop(_):
        if trang_thai["da_nop"]:
            return
        con_thieu = sum(1 for so in range(1, 21) if dap_an_cua_ban.get(so, "?") not in ("A", "B", "C", "D"))
        if con_thieu > 0 and not trang_thai["xac_nhan_nop"]:
            trang_thai["xac_nhan_nop"] = True
            canh_bao_html.value = (
                f"<div class='bkauto-canhbao'>Còn {con_thieu} câu chưa trả lời. "
                "Bấm NỘP BÀI lần nữa để nộp.</div>"
            )
            return
        _nop_bai()

    nut_nop.on_click(_khi_bam_nop)

    display(container)
    _cap_nhat_tien_trinh()
    _hien_cau(0)
    return container


def bat_dau_thi(dap_an_cua_ban: dict, *, hien_dap_an_khi_xem_lai: bool = True):
    """Dựng giao diện thi trắc nghiệm. Ghi lựa chọn của học viên vào dap_an_cua_ban tại chỗ.

    Trả về widget gốc, hoặc None nếu môi trường không dựng được giao diện — trong
    trường hợp đó, sửa trực tiếp dict dap_an_cua_ban ở ô phía trên rồi chạy ô kiểm tra.
    """
    if os.environ.get("AUTOGRADE") == "1":
        print("Che do tu cham: bo qua giao dien thi.")
        return None

    try:
        import ipywidgets as widgets
        from IPython.display import display
    except ImportError:
        _in_de_bang_chu()
        return None

    try:
        return _dung_giao_dien(dap_an_cua_ban, hien_dap_an_khi_xem_lai, widgets, display)
    except Exception as loi:  # noqa: BLE001 - moi truong hien thi ngoai tam kiem soat
        print(f"Khong dung duoc giao dien thi ({type(loi).__name__}: {loi}).")
        print("Sua truc tiep dict dap_an_cua_ban ben tren roi chay lai o kiem tra.")
        return None


def _in_bang_diem_chu(diem_trac_nghiem: bool, diem_thuc_hanh: bool) -> None:
    print("\n" + "=" * 40)
    print(f"Trac nghiem: {'DAT' if diem_trac_nghiem else 'CHUA DAT (xem lai cac cau SAI o tren)'}")
    print(f"Thuc hanh:   {'DAT' if diem_thuc_hanh else 'CHUA DAT (xem lai cac test FAIL o tren)'}")
    print("=" * 40)


def bang_diem(diem_trac_nghiem: bool, diem_thuc_hanh: bool) -> None:
    """Thẻ kết quả gộp hai phần. Không có widget thì in dạng chữ (giữ nguyên nội dung cũ)."""
    if os.environ.get("AUTOGRADE") == "1" or not _co_ipywidgets():
        _in_bang_diem_chu(diem_trac_nghiem, diem_thuc_hanh)
        return

    try:
        import ipywidgets as widgets
        from IPython.display import display

        lop_tn = "bkauto-review-ok" if diem_trac_nghiem else "bkauto-review-bad"
        lop_th = "bkauto-review-ok" if diem_thuc_hanh else "bkauto-review-bad"
        chu_tn = "DAT" if diem_trac_nghiem else "CHUA DAT (xem lai cac cau SAI o tren)"
        chu_th = "DAT" if diem_thuc_hanh else "CHUA DAT (xem lai cac test FAIL o tren)"
        the = widgets.HTML(
            value=(
                CSS
                + "<div class='bkauto-container'><div class='bkauto-score'>"
                f"<div class='bkauto-review-card {lop_tn}'>Trắc nghiệm: <b>{chu_tn}</b></div>"
                f"<div class='bkauto-review-card {lop_th}'>Thực hành: <b>{chu_th}</b></div>"
                "</div></div>"
            )
        )
        display(the)
    except Exception:  # noqa: BLE001 - khong de bang diem lam vo o cuoi bai
        _in_bang_diem_chu(diem_trac_nghiem, diem_thuc_hanh)
