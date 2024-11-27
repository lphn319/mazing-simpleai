from PIL import Image, ImageDraw
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from maze_solver import MazeSolver
from map_utils import load_map, is_valid_point, is_valid_path
from simpleai.search import astar, breadth_first, depth_first

# Kích thước mỗi ô trong lưới
W = 21
click_size = 15
st.title('Tìm đường trong mê cung')

# Mô tả bản đồ mê cung dưới dạng chuỗi
MAP_STR = """
##############################
#         #              #   #
# ####    ########       #   #
#    #    #              #   #
#    ###     #####  ######   #
#      #   ###   #           #
#      #     #   #  #  #   ###
#     #####    #    #  #     #
#              #       #     #
##############################
"""

# Tải bản đồ mê cung từ chuỗi
MAP = load_map(MAP_STR)

# Mở ảnh nền mê cung
bg_image = Image.open("maze.bmp")

# Lưu ảnh nền vào session_state nếu chưa tồn tại
if 'canvas_image' not in st.session_state:
    st.session_state['canvas_image'] = bg_image
    st.session_state['start_point'] = None
    st.session_state['end_point'] = None
    st.session_state['points'] = []  # Danh sách các điểm đã chọn

# Hiển thị ảnh nền ban đầu
frame = st.session_state['canvas_image'].copy()
draw = ImageDraw.Draw(frame)

# Vẽ điểm bắt đầu và kết thúc nếu đã có
if st.session_state['start_point']:
    x, y = st.session_state['start_point']
    draw.ellipse(
        [(x * W + (W - click_size) // 2, y * W + (W - click_size) // 2),
         (x * W + (W + click_size) // 2, y * W + (W + click_size) // 2)],
        fill="green"  # Chấm xanh cho điểm bắt đầu
    )

if st.session_state['end_point']:
    x, y = st.session_state['end_point']
    draw.ellipse(
        [(x * W + (W - click_size) // 2, y * W + (W - click_size) // 2),
         (x * W + (W + click_size) // 2, y * W + (W + click_size) // 2)],
        fill="red"  # Chấm đỏ cho điểm kết thúc
    )

# Cập nhật lại ảnh nền trong session_state
st.session_state['canvas_image'] = frame

# Khởi tạo canvas trong Streamlit để người dùng có thể chọn điểm
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.2)",  # Màu nền cho canvas
    stroke_width=5,
    stroke_color="",  # Mặc định là trong suốt
    background_image=st.session_state['canvas_image'],  # Sử dụng ảnh nền từ session_state
    height=210,
    width=630,
    drawing_mode="point"  # Chế độ chọn điểm
)

# Tùy chọn lựa chọn thuật toán
algorithm = st.selectbox(
    "Chọn thuật toán tìm đường",
    ["astar", "breadth_first", "depth_first"],
    index=0
)

# Xử lý khi người dùng chọn điểm trên canvas
if canvas_result.json_data is not None:
    for obj in canvas_result.json_data["objects"]:
        # Lấy tọa độ điểm từ canvas
        px = obj['left'] + 3
        py = obj['top'] + 3
        
        # Chuyển đổi tọa độ điểm từ pixel sang ô lưới
        x = int(px) // W
        y = int(py) // W
        
        # Kiểm tra nếu điểm hợp lệ và chưa đủ 2 điểm
        if is_valid_point(MAP, x, y) and len(st.session_state['points']) < 2:
            # Nếu hợp lệ, thêm vào danh sách
            st.session_state['points'].append((x, y))

            # Cập nhật điểm bắt đầu hoặc kết thúc nếu chưa có
            if len(st.session_state['points']) == 1:
                st.session_state['start_point'] = st.session_state['points'][0]
            elif len(st.session_state['points']) == 2:
                st.session_state['end_point'] = st.session_state['points'][1]

            # Tạo bản sao của ảnh để vẽ lên các điểm hợp lệ
            frame = st.session_state['canvas_image'].copy()
            draw = ImageDraw.Draw(frame)
            
            # Vẽ điểm bắt đầu (màu xanh) hoặc điểm kết thúc (màu đỏ)
            for i, (px, py) in enumerate(st.session_state['points']):
                color = "green" if i == 0 else "red"
                draw.ellipse(
                    [(px * W + (W - click_size) // 2, py * W + (W - click_size) // 2),
                     (px * W + (W + click_size) // 2, py * W + (W + click_size) // 2)],
                    fill=color
                )

            # Cập nhật lại ảnh nền trong session_state
            st.session_state['canvas_image'] = frame

            # Hiển thị lại canvas với ảnh nền cập nhật
            canvas_result = st_canvas(
                fill_color="rgba(255, 165, 0, 0.2)",
                stroke_width=5,
                stroke_color="black",  # Đặt màu đen nếu điểm hợp lệ
                background_image=st.session_state['canvas_image'],
                height=210,
                width=630,
                drawing_mode="point"
            )

# Nút Run để tìm đường đi sau khi chọn xong điểm
if st.button('Run'):
    # Kiểm tra nếu điểm đầu và điểm kết thúc có hợp lệ không
    if st.session_state['start_point'] and st.session_state['end_point']:
        x1, y1 = st.session_state['start_point']
        x2, y2 = st.session_state['end_point']
        
        if is_valid_path(x1, y1, x2, y2):
            st.write(f'Điểm bắt đầu: ({x1}, {y1}), Điểm kết thúc: ({x2}, {y2})')
            MAP[y1][x1] = 'o'  # Đánh dấu điểm bắt đầu trên bản đồ
            MAP[y2][x2] = 'x'  # Đánh dấu điểm kết thúc trên bản đồ

            # Khởi tạo bài toán tìm đường
            problem = MazeSolver(MAP)
            if algorithm == "astar":
                result = astar(problem, graph_search=True)
            elif algorithm == "breadth_first":
                result = breadth_first(problem, graph_search=True)
            elif algorithm == "depth_first":
                result = depth_first(problem, graph_search=True)

            path = [x[1] for x in result.path()]  # Lấy đường đi từ kết quả tìm kiếm

            # Vẽ đường đi lên ảnh
            frame = st.session_state['canvas_image'].copy()
            draw = ImageDraw.Draw(frame)
            frames = []

            # Vẽ đường đi trên từng khung hình
            for (px, py) in path:
                draw.ellipse(
                    [(px * W + (W - click_size) // 2, py * W + (W - click_size) // 2),
                     (px * W + (W + click_size) // 2, py * W + (W + click_size) // 2)],
                    fill="red"  # Đường đi màu đỏ
                )
                frames.append(frame.copy())  # Thêm khung hình vào GIF

            # Lưu GIF và hiển thị
            gif_path = "solution.gif"
            frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=300, loop=0)

            st.image(gif_path)  # Hiển thị GIF đường đi
            st.success('Tìm đường đi thành công!')
        else:
            st.error('Điểm bắt đầu và điểm kết thúc không hợp lệ hoặc trùng nhau. Vui lòng chọn lại')
    else:
        st.error('Vui lòng chọn điểm bắt đầu và điểm kết thúc.')

# Nút Reset để quay lại trạng thái ban đầu
if st.button('Reset'):
    # Đặt lại các biến về trạng thái ban đầu
    st.session_state['start_point'] = None
    st.session_state['end_point'] = None
    st.session_state['points'] = []
    st.session_state['canvas_image'] = bg_image.copy()
    # Cập nhật lại canvas sau khi reset
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.2)",  # Màu nền cho canvas
        stroke_width=5,
        stroke_color="",  # Mặc định là trong suốt
        background_image=st.session_state['canvas_image'],  # Sử dụng ảnh nền từ session_state
        height=210,
        width=630,
        drawing_mode="point"  # Chế độ chọn điểm
    )
