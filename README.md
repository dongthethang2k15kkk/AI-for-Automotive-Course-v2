# AI Course v2 — BK-AUTO

Khóa học Python/AI 6 tuần dành cho newbies mảng AI for Automobile/BK-Auto.

| Tuần | Chủ đề | Mở trên Colab |
|---|---|---|
| 1 | Nền tảng & cú pháp cơ bản | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dongthethang2k15kkk/AI-for-Automotive-Course-v2/blob/main/week1/week_1.ipynb) |
| 2 | Scope, vòng lặp & cấu trúc dữ liệu cơ bản | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dongthethang2k15kkk/AI-for-Automotive-Course-v2/blob/main/week2/week_2.ipynb) |
| 3 | Xử lý lỗi & tư duy hướng đối tượng | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dongthethang2k15kkk/AI-for-Automotive-Course-v2/blob/main/week3/week_3.ipynb) |
| 4 | OOP nâng cao & cấu trúc dữ liệu tuyến tính | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dongthethang2k15kkk/AI-for-Automotive-Course-v2/blob/main/week4/week_4.ipynb) |
| 5 | Thuật toán cốt lõi & bảng băm | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dongthethang2k15kkk/AI-for-Automotive-Course-v2/blob/main/week5/week_5.ipynb) |
| 6 | Cấu trúc dữ liệu phi tuyến & tổng kết | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dongthethang2k15kkk/AI-for-Automotive-Course-v2/blob/main/week6/week_6.ipynb) |
| — | Đề thi cuối khóa | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dongthethang2k15kkk/AI-for-Automotive-Course-v2/blob/main/final/final_test.ipynb) |

## Cách học

Đọc lý thuyết, làm bài, chạy ô kiểm tra để biết đúng/sai ngay. Mentor (nếu có) chỉ gỡ chỗ vướng.

## Nộp bài

1. Mở notebook bằng badge phía trên (yêu cầu đăng nhập Google).
2. Làm bài, chạy hết các ô kiểm tra cho đến khi đạt.
3. `File → Save a copy in GitHub`, chọn repo cá nhân của bạn (được cấp qua GitHub Classroom), commit vào đúng thư mục tuần.
4. Repo tự chấm lại, kết quả ở tab Actions.

## Cấu trúc repo

week1/ .. week6/ notebook từng tuần
final/ đề thi cuối khóa
tests/ bộ máy chấm dùng chung (runner.py) + test case từng tuần
src/ mã nguồn dạng .py (jupytext) dùng để sinh lại notebook khi cần sửa

## Dành cho người chỉnh sửa nội dung

Notebook được sinh ra từ file nguồn `.py` trong `src/` bằng [jupytext](https://jupytext.readthedocs.io/), để diff Git luôn sạch. Sửa nội dung thì sửa file `.py`, không sửa trực tiếp `.ipynb`:

```bash
pip install jupytext
jupytext --to ipynb src/week_2.py -o week2/week_2.ipynb
```