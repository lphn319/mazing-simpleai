def load_map(map_str):
    """
    Hàm load_map để chuyển đổi một chuỗi mô tả bản đồ thành ma trận 2D.
    - map_str: Chuỗi mô tả bản đồ, với mỗi hàng được phân tách bằng ký tự xuống dòng.
    - Trả về: Danh sách hai chiều (ma trận) biểu diễn bản đồ.
    """
    return [list(row) for row in map_str.split("\n") if row]

def is_valid_point(map_data, x, y):
    """
    Hàm is_valid_point để kiểm tra xem một điểm (x, y) có phải là vị trí hợp lệ trên bản đồ không.
    - map_data: Bản đồ mê cung dưới dạng ma trận 2D.
    - x, y: Tọa độ cần kiểm tra.
    - Trả về: True nếu điểm không phải là tường (#), ngược lại trả về False.
    """
    return map_data[y][x] != '#'

def is_valid_path(x1, y1, x2, y2):
    """
    Hàm is_valid_path để kiểm tra xem điểm bắt đầu và điểm kết thúc có hợp lệ hay không.
    - x1, y1: Tọa độ điểm bắt đầu.
    - x2, y2: Tọa độ điểm kết thúc.
    - Trả về: True nếu điểm bắt đầu và kết thúc không trùng nhau, ngược lại trả về False.
    """
    return (x1, y1) != (x2, y2)