"""Dữ liệu 20 câu trắc nghiệm đề thi cuối khóa. Không chứa đáp án đúng.

Đề và bốn lựa chọn chép nguyên văn từ khối markdown gốc (src/final_test.py), kể cả
backtick đánh dấu code trong câu chữ - không rút gọn, không đổi ký tự nào. Đáp án đúng
nằm ở dạng băm trong tests/test_final.py, không lặp lại ở đây.
"""

from __future__ import annotations

CAU_HOI = [
    {
        "so": 1,
        "de": 'Đâu là cách khai báo một hằng số cấu hình hệ thống (theo quy ước) trong Python?',
        "lua_chon": {
            "A": '`const MAX_SPEED = 40`',
            "B": '`MAX_SPEED = 40`',
            "C": '`let MAX_SPEED = 40`',
            "D": '`final MAX_SPEED = 40`',
        },
        "giai_thich": 'Python không có từ khoá hằng số. Quy ước PEP 8 là đặt tên viết HOA toàn bộ.',
        "tuan": 1,
    },
    {
        "so": 2,
        "de": 'Cho `lidar_data = [1.2, 2.5, 3.1, 0.8, 4.5]`. Cú pháp nào để lấy 3 giá trị cuối cùng?',
        "lua_chon": {
            "A": '`lidar_data[2:5]`',
            "B": '`lidar_data[-3:]`',
            "C": '`lidar_data[:-3]`',
            "D": 'Cả A và B đều đúng.',
        },
        "giai_thich": 'lidar_data có 5 phần tử nên [2:5] và [-3:] cùng lấy chỉ số 2,3,4 — ba giá trị cuối.',
        "tuan": 2,
    },
    {
        "so": 3,
        "de": '`config = {"mode": "auto", "speed": 20}`. Lệnh nào sau đây sẽ gây ra lỗi?',
        "lua_chon": {
            "A": '`config["speed"] = 30`',
            "B": '`config.update({"camera": "on"})`',
            "C": '`config.add("sensor", "lidar")`',
            "D": '`config["mode"] = "manual"`',
        },
        "giai_thich": 'dict không có phương thức add — thêm khoá mới dùng gán config[khoa] = gia_tri hoặc update.',
        "tuan": 2,
    },
    {
        "so": 4,
        "de": 'Kết quả của biểu thức `True and False or not False` là gì?',
        "lua_chon": {
            "A": '`True`',
            "B": '`False`',
            "C": '`None`',
            "D": 'Lỗi cú pháp (Syntax Error)',
        },
        "giai_thich": 'Thứ tự ưu tiên not > and > or: (True and False) or (not False) = False or True = True.',
        "tuan": 1,
    },
    {
        "so": 5,
        "de": 'Khối lệnh `finally` trong cấu trúc `try...except` hoạt động như thế nào?',
        "lua_chon": {
            "A": 'Chỉ chạy khi khối `try` có lỗi.',
            "B": 'Chỉ chạy khi khối `except` không bắt được lỗi.',
            "C": 'Luôn luôn chạy, bất kể có lỗi hay không.',
            "D": 'Chỉ chạy khi không có lỗi nào xảy ra.',
        },
        "giai_thich": 'finally chạy sau try/except trong mọi trường hợp, kể cả khi có lỗi không bắt được.',
        "tuan": 3,
    },
    {
        "so": 6,
        "de": 'Từ khóa nào dùng để bỏ qua lần đọc hiện tại và chuyển ngay sang lần lặp tiếp theo nếu dữ liệu bị nhiễu?',
        "lua_chon": {
            "A": '`break`',
            "B": '`pass`',
            "C": '`continue`',
            "D": '`return`',
        },
        "giai_thich": 'continue bỏ qua phần còn lại của lượt lặp hiện tại rồi quay về đầu vòng lặp, break thoát hẳn vòng lặp.',
        "tuan": 2,
    },
    {
        "so": 7,
        "de": 'Phát biểu nào đúng về tham số mặc định (default arguments)?',
        "lua_chon": {
            "A": 'Phải đặt trước các tham số không có giá trị mặc định.',
            "B": 'Phải đặt sau cùng trong danh sách tham số.',
            "C": 'Không thể thay đổi giá trị khi gọi hàm.',
            "D": 'Một hàm chỉ được phép có tối đa một tham số mặc định.',
        },
        "giai_thich": 'Python bắt buộc tham số có giá trị mặc định đứng sau tham số không có, nếu không sẽ báo SyntaxError.',
        "tuan": 2,
    },
    {
        "so": 8,
        "de": 'Tham số `self` trong các phương thức của một Class có ý nghĩa gì?',
        "lua_chon": {
            "A": 'Trỏ đến lớp cha.',
            "B": 'Từ khóa khai báo biến toàn cục.',
            "C": 'Trỏ đến chính đối tượng (instance) đang gọi phương thức.',
            "D": 'Đại diện cho `__init__`.',
        },
        "giai_thich": 'self là tham số đầu tiên của mọi phương thức, luôn trỏ vào chính object đang gọi nó.',
        "tuan": 3,
    },
    {
        "so": 9,
        "de": 'Để biến `__trang_thai_dong_co` trở thành private, nguyên lý nào của OOP đang được áp dụng?',
        "lua_chon": {
            "A": 'Kế thừa',
            "B": 'Đóng gói (Encapsulation)',
            "C": 'Đa hình',
            "D": 'Trừu tượng',
        },
        "giai_thich": 'Tiền tố __ giấu thuộc tính khỏi truy cập trực tiếp từ bên ngoài — đúng bản chất của đóng gói.',
        "tuan": 4,
    },
    {
        "so": 10,
        "de": 'Hàm `super().__init__()` dùng trong Lớp con nhằm mục đích gì?',
        "lua_chon": {
            "A": 'Khởi tạo lại toàn bộ phương thức của Lớp con.',
            "B": 'Gọi hàm khởi tạo của Lớp cha để kế thừa thuộc tính nền tảng.',
            "C": 'Xóa các thuộc tính của Lớp cha.',
            "D": 'Kiểm tra Lớp cha có tồn tại hay không.',
        },
        "giai_thich": 'super().__init__() gọi __init__ của lớp cha để các thuộc tính nền tảng được khởi tạo trước.',
        "tuan": 4,
    },
    {
        "so": 11,
        "de": '`Camera_Module` kế thừa từ `Sensor` và định nghĩa lại `read_data()`. Tính chất nào đang thể hiện?',
        "lua_chon": {
            "A": 'Ghi đè phương thức (Method Overriding) - biểu hiện của Đa hình.',
            "B": 'Đóng gói dữ liệu.',
            "C": 'Nạp chồng phương thức (Overloading).',
            "D": 'Biến tĩnh.',
        },
        "giai_thich": 'Lớp con viết lại một phương thức đã có ở lớp cha là ghi đè, một dạng của đa hình.',
        "tuan": 4,
    },
    {
        "so": 12,
        "de": 'Lập lịch tác vụ theo nguyên tắc "lệnh nào đến trước xử lý trước" — cấu trúc nào phù hợp?',
        "lua_chon": {
            "A": 'Stack',
            "B": 'Queue',
            "C": 'Set',
            "D": 'Graph',
        },
        "giai_thich": 'Vào trước ra trước (FIFO) là đúng nguyên lý của Queue.',
        "tuan": 4,
    },
    {
        "so": 13,
        "de": 'Ngăn xếp (Stack) hoạt động theo nguyên lý nào?',
        "lua_chon": {
            "A": 'FIFO',
            "B": 'LIFO',
            "C": 'Random Access',
            "D": 'Key-Value Pair',
        },
        "giai_thich": 'Stack là vào sau ra trước (LIFO): phần tử thêm cuối cùng bị lấy ra đầu tiên.',
        "tuan": 4,
    },
    {
        "so": 14,
        "de": 'Big O của Tìm kiếm nhị phân trên mảng đã sắp xếp là bao nhiêu?',
        "lua_chon": {
            "A": 'O(1)',
            "B": 'O(n)',
            "C": 'O(log n)',
            "D": 'O(n²)',
        },
        "giai_thich": 'Mỗi bước bỏ hẳn một nửa mảng còn lại, nên số bước tăng theo log2 của kích thước mảng.',
        "tuan": 5,
    },
    {
        "so": 15,
        "de": 'Điều kiện dừng (Base Case) trong Đệ quy có vai trò gì?',
        "lua_chon": {
            "A": 'Làm thuật toán chạy nhanh hơn.',
            "B": 'Tránh tràn bộ nhớ (Stack Overflow) do gọi vô hạn.',
            "C": 'Reset lại biến toàn cục.',
            "D": 'Trả về giá trị mặc định nếu đầu vào sai.',
        },
        "giai_thich": 'Không có điều kiện dừng, hàm đệ quy gọi chính nó mãi, chồng call stack đến khi tràn bộ nhớ.',
        "tuan": 5,
    },
    {
        "so": 16,
        "de": 'Xung đột (Collision) trong Bảng băm xảy ra khi nào?',
        "lua_chon": {
            "A": 'Bảng băm hết dung lượng.',
            "B": 'Hai khóa khác nhau bị hàm băm trả về cùng một chỉ mục.',
            "C": 'Xóa một phần tử không tồn tại.',
            "D": 'Cập nhật giá trị của một khóa đã có.',
        },
        "giai_thich": 'Collision là khi hàm băm ánh xạ hai khoá khác nhau vào cùng một ngăn (chỉ mục) trong bảng.',
        "tuan": 5,
    },
    {
        "so": 17,
        "de": 'Một Node trong Cây không có bất kỳ Node con nào thì gọi là gì?',
        "lua_chon": {
            "A": 'Gốc (Root)',
            "B": 'Nhánh (Branch)',
            "C": 'Cạnh (Edge)',
            "D": 'Lá (Leaf)',
        },
        "giai_thich": 'Node không có con nằm ở cuối một nhánh của cây — gọi là lá.',
        "tuan": 6,
    },
    {
        "so": 18,
        "de": 'Trong BST, quy tắc sắp xếp Node con so với Node cha là gì?',
        "lua_chon": {
            "A": 'Trái lớn hơn, phải nhỏ hơn.',
            "B": 'Cả hai đều lớn hơn.',
            "C": 'Trái nhỏ hơn, phải lớn hơn.',
            "D": 'Sắp xếp ngẫu nhiên.',
        },
        "giai_thich": 'Quy tắc BST: giá trị nhánh trái luôn nhỏ hơn node cha, nhánh phải luôn lớn hơn.',
        "tuan": 6,
    },
    {
        "so": 19,
        "de": 'Biểu diễn bản đồ Waypoint đã biết trước khoảng cách giữa các điểm nối — nên dùng cấu trúc nào?',
        "lua_chon": {
            "A": 'Đồ thị vô hướng không trọng số.',
            "B": 'Đồ thị có trọng số (Weighted Graph).',
            "C": 'Danh sách liên kết đơn.',
            "D": 'Bảng băm.',
        },
        "giai_thich": 'Khoảng cách giữa các điểm là một con số gắn trên mỗi cạnh — đúng định nghĩa đồ thị có trọng số.',
        "tuan": 6,
    },
    {
        "so": 20,
        "de": 'Kỹ thuật lưu kết quả bài toán con đã giải để không tính lại trong DP gọi là gì?',
        "lua_chon": {
            "A": 'Memoization',
            "B": 'Recursion',
            "C": 'Backtracking',
            "D": 'Linear Probing',
        },
        "giai_thich": 'Memoization là lưu lại kết quả bài toán con đã tính vào cache để lần sau tra thay vì tính lại.',
        "tuan": 6,
    },
]
