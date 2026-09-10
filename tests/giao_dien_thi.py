"""Giao diện thi cuối khóa bằng ipywidgets: một ô chạy duy nhất, hai phần nối tiếp.

Luồng: chay_bai_thi() -> Phần 1 trắc nghiệm 20 câu -> bấm NỘP BÀI -> chấm ngay và
tự chuyển sang Phần 2 viết code -> bấm NỘP BÀI CODE -> chấm bằng test case ->
bảng điểm tổng kết.

Ba nhánh thoái hoá, không nhánh nào được ném lỗi ra ngoài:
  1. AUTOGRADE=1 (máy chấm GitHub Actions, không cài ipywidgets) -> in một dòng, thoát.
  2. Không có ipywidgets -> in bản chữ toàn bộ đề, thoát.
  3. Dựng widget lỗi vì lý do khác -> bắt hết, in một dòng cảnh báo, thoát.
"""

from __future__ import annotations

import html
import io
import os
import re
import traceback
from contextlib import redirect_stdout

try:
    from .de_thi_cau_hoi import CAU_HOI
    from .test_final import _MA_DAP_AN, _bam, kiem_tra_gop_khung
except ImportError:
    from de_thi_cau_hoi import CAU_HOI
    from test_final import _MA_DAP_AN, _bam, kiem_tra_gop_khung


MA_KHOI_DAU = """def gop_khung_thoi_gian(intervals):
    # TODO:
    # 1. Nếu intervals rỗng, trả về []
    # 2. Sắp xếp intervals theo start tăng dần
    # 3. Duyệt qua từng khung đã sắp xếp: nếu start của khung hiện tại <= end của
    #    khung cuối cùng trong kết quả -> gộp (cập nhật end = max của 2 end);
    #    không thì thêm khung hiện tại như một khung mới vào kết quả
    pass
"""

DE_BAI_CODE = """
<div class='bkauto-qnum'>Phần 2 — Bài thực hành</div>
<div class='bkauto-qtext'>
Cảm biến Lidar được lập lịch quét theo các khung thời gian (mili-giây). Do nhận lệnh từ
nhiều module, các khung thường chồng chéo, gây lãng phí CPU và hao pin.
<br><br>
Viết hàm <code>gop_khung_thoi_gian(intervals)</code> nhận list các khung
<code>[start, end]</code>. Gộp mọi khung chồng chéo, trả về lịch trình đã gộp, sắp theo
<code>start</code> tăng dần.
<br><br>
<b>Ví dụ 1:</b> <code>[[1, 3], [2, 6], [8, 10], [15, 18]]</code> →
<code>[[1, 6], [8, 10], [15, 18]]</code><br>
<b>Ví dụ 2:</b> <code>[[1, 4], [4, 5]]</code> → <code>[[1, 5]]</code> (chạm nhau tại mốc 4
vẫn tính là chồng chéo)
<br><br>
Đầu vào có thể chưa sắp xếp. Yêu cầu <code>O(n log n)</code>: gọi
<code>sorted(intervals)</code> trước, sau đó duyệt một lượt để gộp.
</div>
"""

CSS = """
<style>
.bkauto-container { max-width: 860px; font-family: -apple-system, "Segoe UI", Roboto, sans-serif; }
.bkauto-title { font-size: 1.05em; font-weight: 600; margin: 4px 0 8px 0; }
.bkauto-card { background: rgba(127,127,127,0.08); border: 1px solid rgba(127,127,127,0.35);
  border-radius: 8px; padding: 12px 14px; margin: 8px 0; }
.bkauto-qnum { font-weight: 600; opacity: 0.75; margin-bottom: 4px; }
.bkauto-qtext { font-size: 1.02em; margin-bottom: 4px; line-height: 1.45; }
.bkauto-qtext code, .bkauto-review-card code, .bkauto-score code {
  background: rgba(127,127,127,0.18); padding: 1px 4px; border-radius: 4px;
  font-family: "Courier New", monospace; }
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
.bkauto-code textarea { font-family: "Courier New", monospace !important; font-size: 13px !important; }
.bkauto-ketqua { font-family: "Courier New", monospace; font-size: 12.5px; line-height: 1.45;
  white-space: pre-wrap; margin: 0; }
.bkauto-pass { color: #3fae4e; }
.bkauto-fail { color: #e5484d; }
</style>
"""


def _dap_an_dung(so_cau: int) -> str:
    for chu in "ABCD":
        if _bam(so_cau, chu) == _MA_DAP_AN[so_cau]:
            return chu
    return "?"


def _bo_backtick(s: str) -> str:
    return s.replace("`", "")


def _dinh_dang_html(s: str) -> str:
    """Escape HTML, giữ lại đoạn trong dấu backtick dưới dạng <code>."""
    ra = []
    for p in re.split(r"(`[^`]*`)", s):
        if p.startswith("`") and p.endswith("`") and len(p) >= 2:
            ra.append("<code>" + html.escape(p[1:-1]) + "</code>")
        else:
            ra.append(html.escape(p))
    return "".join(ra)


def _bo_ansi(s: str) -> str:
    return re.sub(r"\x1b\[[0-9;]*m", "", s)


def _to_mau_ket_qua(van_ban: str) -> str:
    """Đổi output test thành HTML, tô xanh dòng PASS và đỏ dòng FAIL."""
    dong_html = []
    for dong in _bo_ansi(van_ban).splitlines():
        an_toan = html.escape(dong)
        if dong.strip().startswith("PASS") or "— Đạt!" in dong:
            dong_html.append(f"<span class='bkauto-pass'>{an_toan}</span>")
        elif dong.strip().startswith("FAIL") or "Xem lại các test" in dong:
            dong_html.append(f"<span class='bkauto-fail'>{an_toan}</span>")
        else:
            dong_html.append(an_toan)
    return "<pre class='bkauto-ketqua'>" + "\n".join(dong_html) + "</pre>"


def _in_de_bang_chu() -> None:
    print("Khong tim thay ipywidgets trong moi truong nay.")
    print("Lam bai bang cach doc de o phan Phu luc trong notebook.")
    for q in CAU_HOI:
        print(f"\nCau {q['so']}: {_bo_backtick(q['de'])}")
        for k in "ABCD":
            print(f"  {k}. {_bo_backtick(q['lua_chon'][k])}")
    print("\nPhan 2: viet ham gop_khung_thoi_gian(intervals) - gop cac khung [start, end]")
    print("bi chong cheo, tra ve list da gop, sap theo start tang dan.")


def _dung_giao_dien(widgets, display, hien_dap_an_khi_xem_lai):
    dap_an = {i: "?" for i in range(1, 21)}
    trang_thai = {"idx": 0, "dat_lai": False, "xac_nhan": False,
                  "so_dung": 0, "da_nop_tn": False, "diem_code": False}

    style_html = widgets.HTML(value=CSS)
    tieu_de = widgets.HTML(value="<div class='bkauto-title'>ĐỀ THI CUỐI KHOÁ · AI Course v2</div>")

    # ---------------- Phần 1: trắc nghiệm ----------------
    thanh_tien_trinh = widgets.IntProgress(min=0, max=20, value=0, layout=widgets.Layout(width="55%"))
    nhan_tien_trinh = widgets.HTML(value="0/20 câu đã trả lời")
    hang_tien_trinh = widgets.HBox([thanh_tien_trinh, nhan_tien_trinh])

    de_html = widgets.HTML(value="")
    radio = widgets.RadioButtons(options=[], layout=widgets.Layout(width="100%"))
    the_cau_hoi = widgets.VBox([de_html, radio])
    the_cau_hoi.add_class("bkauto-card")

    canh_bao_html = widgets.HTML(value="")
    nut_truoc = widgets.Button(description="< Câu trước")
    nut_sau = widgets.Button(description="Câu sau >")
    nut_nop_tn = widgets.Button(description="NỘP BÀI", button_style="success")
    hang_dieu_huong = widgets.HBox([nut_truoc, nut_sau, nut_nop_tn])

    nut_luoi = [
        widgets.Button(description=str(i + 1),
                       layout=widgets.Layout(width="32px", height="30px", margin="1px"))
        for i in range(20)
    ]
    luoi = widgets.GridBox(
        children=nut_luoi,
        layout=widgets.Layout(grid_template_columns="repeat(10, 1fr)", grid_gap="2px"),
    )
    chu_thich = widgets.HTML(
        value="<div class='bkauto-legend'>xanh đậm = đã trả lời &nbsp; viền xanh dương = câu đang xem</div>"
    )
    phan_1 = widgets.VBox([hang_tien_trinh, the_cau_hoi, canh_bao_html, hang_dieu_huong, luoi, chu_thich])

    # ---------------- Phần 2: viết code ----------------
    tom_tat_tn = widgets.HTML(value="")
    nut_xem_lai = widgets.Button(description="Xem lại phần trắc nghiệm")
    khu_xem_lai = widgets.VBox([])
    khu_xem_lai.layout.display = "none"

    de_code_html = widgets.HTML(value=DE_BAI_CODE)
    o_code = widgets.Textarea(value=MA_KHOI_DAU, layout=widgets.Layout(width="100%", height="240px"))
    o_code.add_class("bkauto-code")
    the_code = widgets.VBox([de_code_html, o_code])
    the_code.add_class("bkauto-card")

    nut_nop_code = widgets.Button(description="NỘP BÀI CODE", button_style="success")
    ket_qua_code_html = widgets.HTML(value="")
    bang_diem_html = widgets.HTML(value="")
    phan_2 = widgets.VBox([tom_tat_tn, nut_xem_lai, khu_xem_lai, the_code,
                           nut_nop_code, ket_qua_code_html, bang_diem_html])
    phan_2.layout.display = "none"

    container = widgets.VBox([style_html, tieu_de, phan_1, phan_2])
    container.add_class("bkauto-container")

    # ---------------- Hành vi phần 1 ----------------
    def _cap_nhat_tien_trinh():
        dem = sum(1 for v in dap_an.values() if v in ("A", "B", "C", "D"))
        thanh_tien_trinh.value = dem
        nhan_tien_trinh.value = f"{dem}/20 câu đã trả lời"

    def _cap_nhat_luoi():
        for i, nut in enumerate(nut_luoi):
            nut.remove_class("bkauto-done")
            nut.remove_class("bkauto-current")
            if dap_an.get(i + 1, "?") in ("A", "B", "C", "D"):
                nut.add_class("bkauto-done")
            if i == trang_thai["idx"]:
                nut.add_class("bkauto-current")

    def _hien_cau(idx):
        idx = max(0, min(19, idx))
        trang_thai["idx"] = idx
        q = CAU_HOI[idx]
        de_html.value = (
            f"<div class='bkauto-qnum'>Câu {q['so']} / 20</div>"
            f"<div class='bkauto-qtext'>{_dinh_dang_html(q['de'])}</div>"
        )
        trang_thai["dat_lai"] = True
        radio.options = [(f"{k}. {_bo_backtick(q['lua_chon'][k])}", k) for k in "ABCD"]
        hien_tai = dap_an.get(q["so"], "?")
        radio.value = hien_tai if hien_tai in ("A", "B", "C", "D") else None
        trang_thai["dat_lai"] = False
        nut_truoc.disabled = idx == 0
        nut_sau.disabled = idx == 19
        _cap_nhat_luoi()

    def _khi_chon(change):
        if trang_thai["dat_lai"] or trang_thai["da_nop_tn"]:
            return
        if change["name"] != "value" or change["new"] not in ("A", "B", "C", "D"):
            return
        dap_an[CAU_HOI[trang_thai["idx"]]["so"]] = change["new"]
        _cap_nhat_tien_trinh()
        _cap_nhat_luoi()

    radio.observe(_khi_chon, names="value")
    nut_truoc.on_click(lambda _: _hien_cau(trang_thai["idx"] - 1))
    nut_sau.on_click(lambda _: _hien_cau(trang_thai["idx"] + 1))
    for i, nut in enumerate(nut_luoi):
        nut.on_click((lambda idx: lambda _: _hien_cau(idx))(i))

    def _dung_the_xem_lai():
        the = []
        for q in CAU_HOI:
            so = q["so"]
            dung_dap = _dap_an_dung(so)
            chon = dap_an.get(so, "?")
            lop = "bkauto-review-ok" if chon == dung_dap else "bkauto-review-bad"
            chon_hien = chon if chon in ("A", "B", "C", "D") else "(chưa chọn)"
            phan_dap_an = (
                f"Bạn chọn: {chon_hien} — Đáp án đúng: {dung_dap}"
                if hien_dap_an_khi_xem_lai else f"Bạn chọn: {chon_hien}"
            )
            phan_giai = (
                f"<div class='bkauto-review-giai'>{_dinh_dang_html(q['giai_thich'])}</div>"
                if hien_dap_an_khi_xem_lai else ""
            )
            the.append(widgets.HTML(
                value=(
                    f"<div class='bkauto-review-card {lop}'>"
                    f"<b>Câu {so}.</b> {_dinh_dang_html(q['de'])}"
                    f"<div class='bkauto-review-line'>{phan_dap_an}</div>"
                    f"{phan_giai}"
                    f"<div class='bkauto-review-tuan'>Tuần {q['tuan']}</div></div>"
                )
            ))
        khu_xem_lai.children = tuple(the)

    def _bam_xem_lai(_):
        if khu_xem_lai.layout.display == "none":
            if not khu_xem_lai.children:
                _dung_the_xem_lai()
            khu_xem_lai.layout.display = None
            nut_xem_lai.description = "Ẩn phần trắc nghiệm"
        else:
            khu_xem_lai.layout.display = "none"
            nut_xem_lai.description = "Xem lại phần trắc nghiệm"

    nut_xem_lai.on_click(_bam_xem_lai)

    def _sang_phan_2():
        trang_thai["da_nop_tn"] = True
        so_dung = sum(1 for so in range(1, 21) if dap_an.get(so, "?") == _dap_an_dung(so))
        trang_thai["so_dung"] = so_dung
        lop = "bkauto-review-ok" if so_dung == 20 else "bkauto-review-bad"
        tom_tat_tn.value = (
            f"<div class='bkauto-review-card {lop}'>"
            f"<b>Phần 1 đã nộp: {so_dung}/20 câu đúng.</b> "
            "Tiêu chí đạt là đúng cả 20 câu.</div>"
        )
        phan_1.layout.display = "none"
        phan_2.layout.display = None

    def _khi_nop_tn(_):
        if trang_thai["da_nop_tn"]:
            return
        con_thieu = sum(1 for so in range(1, 21) if dap_an.get(so, "?") not in ("A", "B", "C", "D"))
        if con_thieu > 0 and not trang_thai["xac_nhan"]:
            trang_thai["xac_nhan"] = True
            canh_bao_html.value = (
                f"<div class='bkauto-canhbao'>Còn {con_thieu} câu chưa trả lời. "
                "Bấm NỘP BÀI lần nữa để nộp và sang phần 2.</div>"
            )
            return
        _sang_phan_2()

    nut_nop_tn.on_click(_khi_nop_tn)

    # ---------------- Hành vi phần 2 ----------------
    def _hien_bang_diem():
        so_dung = trang_thai["so_dung"]
        dat_tn = so_dung == 20
        dat_code = trang_thai["diem_code"]
        lop_tn = "bkauto-review-ok" if dat_tn else "bkauto-review-bad"
        lop_code = "bkauto-review-ok" if dat_code else "bkauto-review-bad"
        bang_diem_html.value = (
            "<div class='bkauto-score'><b>BẢNG ĐIỂM TỔNG KẾT</b>"
            f"<div class='bkauto-review-card {lop_tn}'>Trắc nghiệm: {so_dung}/20 — "
            f"{'ĐẠT' if dat_tn else 'CHƯA ĐẠT'}</div>"
            f"<div class='bkauto-review-card {lop_code}'>Bài code: "
            f"{'ĐẠT' if dat_code else 'CHƯA ĐẠT'}</div>"
            "Kết quả chỉ nằm trong phiên làm bài này. Chụp màn hình bảng điểm gửi mentor."
            "</div>"
        )

    def _khi_nop_code(_):
        khong_gian = {}
        bo_dem = io.StringIO()
        try:
            with redirect_stdout(bo_dem):
                exec(compile(o_code.value, "<bai_lam>", "exec"), khong_gian)
        except SyntaxError as loi:
            ket_qua_code_html.value = _to_mau_ket_qua(
                f"FAIL  Code bị lỗi cú pháp ở dòng {loi.lineno}: {loi.msg}"
            )
            return
        except Exception as loi:  # noqa: BLE001 - code hoc vien, loi gi cung co the
            ket_qua_code_html.value = _to_mau_ket_qua(
                "FAIL  Code chạy lỗi:\n" + "".join(traceback.format_exception_only(type(loi), loi))
            )
            return

        ham = khong_gian.get("gop_khung_thoi_gian")
        if not callable(ham):
            ket_qua_code_html.value = _to_mau_ket_qua(
                "FAIL  Chưa tìm thấy hàm gop_khung_thoi_gian. Giữ nguyên tên hàm như đề bài."
            )
            return

        bo_dem = io.StringIO()
        try:
            with redirect_stdout(bo_dem):
                dat = kiem_tra_gop_khung(ham)
        except Exception as loi:  # noqa: BLE001 - runner co the nem loi o che do STRICT
            dat = False
            bo_dem.write(f"\nFAIL  {type(loi).__name__}: {loi}")

        trang_thai["diem_code"] = bool(dat)
        ket_qua_code_html.value = _to_mau_ket_qua(bo_dem.getvalue())
        _hien_bang_diem()

    nut_nop_code.on_click(_khi_nop_code)

    display(container)
    _cap_nhat_tien_trinh()
    _hien_cau(0)


def chay_bai_thi(*, hien_dap_an_khi_xem_lai: bool = True) -> None:
    """Chạy toàn bộ bài thi trong một ô: trắc nghiệm rồi tự chuyển sang bài code."""
    if os.environ.get("AUTOGRADE") == "1":
        print("Che do tu cham: bo qua giao dien thi.")
        return

    try:
        import ipywidgets as widgets
        from IPython.display import display
    except ImportError:
        _in_de_bang_chu()
        return

    try:
        _dung_giao_dien(widgets, display, hien_dap_an_khi_xem_lai)
    except Exception as loi:  # noqa: BLE001 - moi truong hien thi ngoai tam kiem soat
        print(f"Khong dung duoc giao dien thi ({type(loi).__name__}: {loi}).")
        print("Doc de o phan Phu luc cuoi notebook de lam bai.")
