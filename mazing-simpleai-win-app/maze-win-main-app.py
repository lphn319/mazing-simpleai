import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk
import time
from simpleai.search import astar, breadth_first, depth_first
from maze_solver import MazeSolver
from maps import MAP, generate_map_image

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.dem = 0
        self.is_displaying_path = False  # Trạng thái hiển thị đường đi
        self.title('Tìm đường trong mê cung')
        self.cvs_me_cung = tk.Canvas(self, width=len(MAP[0]) * 21, height=len(MAP) * 21, relief=tk.SUNKEN, border=1)

        # Tải và hiển thị hình ảnh ban đầu của mê cung
        self.image_tk = ImageTk.PhotoImage(generate_map_image())
        self.cvs_me_cung.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
        self.cvs_me_cung.bind("<Button-1>", self.xu_ly_mouse)

        # Các nút điều khiển
        lbl_frm_menu = tk.LabelFrame(self)
        btn_start = tk.Button(lbl_frm_menu, text='Start', width=7, command=self.btn_start_click)
        btn_reset = tk.Button(lbl_frm_menu, text='Reset', width=7, command=self.btn_reset_click)
        
        # Lựa chọn thuật toán với hàm theo dõi để phát hiện thay đổi
        self.algorithm = tk.StringVar(value="astar")
        self.algorithm.trace("w", self.on_algorithm_change)
        tk.Radiobutton(lbl_frm_menu, text="A*", variable=self.algorithm, value="astar").grid(row=2, column=0, sticky=tk.W)
        tk.Radiobutton(lbl_frm_menu, text="BFS", variable=self.algorithm, value="breadth_first").grid(row=3, column=0, sticky=tk.W)
        tk.Radiobutton(lbl_frm_menu, text="DFS", variable=self.algorithm, value="depth_first").grid(row=4, column=0, sticky=tk.W)

        # Bố trí
        btn_start.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N)
        btn_reset.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N)
        self.cvs_me_cung.grid(row=0, column=0, padx=5, pady=5)
        lbl_frm_menu.grid(row=0, column=1, padx=5, pady=7, sticky=tk.NW)

    def xu_ly_mouse(self, event):
        px = event.x
        py = event.y
        x = px // 21
        y = py // 21

        # Kiểm tra nếu nhấn vào tường thì không ghi nhận
        if MAP[y][x] == '#':
            return  # Bỏ qua nếu là tường

        if self.dem == 0:
            MAP[y][x] = 'o'
            self.cvs_me_cung.create_oval(x * 21 + 2, y * 21 + 2, (x + 1) * 21 - 2, (y + 1) * 21 - 2, outline='#00FF00', fill='#00FF00')  # Màu xanh lá cây cho điểm bắt đầu
            self.dem = 1
        elif self.dem == 1:
            MAP[y][x] = 'x'
            self.cvs_me_cung.create_rectangle(x * 21 + 2, y * 21 + 2, (x + 1) * 21 - 2, (y + 1) * 21 - 2, outline='#FF0000', fill='#FF0000')  # Màu đỏ cho điểm kết thúc
            self.dem = 2

    def btn_start_click(self):
        self.find_and_draw_path()

    def find_and_draw_path(self):
        # Kiểm tra nếu điểm bắt đầu và điểm kết thúc đã được chọn
        start_point = any('o' in row for row in MAP)
        goal_point = any('x' in row for row in MAP)
        
        # Thông báo lỗi nếu chưa chọn điểm bắt đầu hoặc kết thúc
        if not start_point:
            messagebox.showerror("Lỗi", "Chưa chọn điểm bắt đầu. Hãy chọn điểm bắt đầu trước khi bắt đầu tìm kiếm.")
            return
        if not goal_point:
            messagebox.showerror("Lỗi", "Chưa chọn điểm kết thúc. Hãy chọn điểm kết thúc trước khi bắt đầu tìm kiếm.")
            return

        # Khởi tạo bài toán và chọn thuật toán tìm đường
        problem = MazeSolver(MAP)
        algorithm = self.algorithm.get()
        if algorithm == "astar":
            result = astar(problem, graph_search=True)
        elif algorithm == "breadth_first":
            result = breadth_first(problem, graph_search=True)
        elif algorithm == "depth_first":
            result = depth_first(problem, graph_search=True)
        else:
            return

        path = [x[1] for x in result.path()]

        # Đặt trạng thái đang hiển thị đường đi
        self.is_displaying_path = True

        # Vẽ đường đi
        for i in range(1, len(path)):
            x, y = path[i]
            self.cvs_me_cung.create_rectangle(x * 21 + 2, y * 21 + 2, (x + 1) * 21 - 2, (y + 1) * 21 - 2, outline='#FF0000', fill='#FF0000')
            self.update()
            time.sleep(0.1)

        # Đặt trạng thái đã hoàn thành hiển thị đường đi
        self.is_displaying_path = False

    def on_algorithm_change(self, *args):
        """Hàm gọi khi thuật toán được thay đổi."""
        # Xóa đường đi cũ
        self.clear_path()
        # Tìm và vẽ đường đi mới sử dụng thuật toán đã chọn
        self.find_and_draw_path()

    def clear_path(self):
        """Xóa đường đi đã vẽ mà không đặt lại điểm bắt đầu và kết thúc."""
        # Xóa canvas và hiển thị lại mê cung với các điểm bắt đầu/kết thúc
        self.cvs_me_cung.delete(tk.ALL)
        self.image_tk = ImageTk.PhotoImage(generate_map_image())
        self.cvs_me_cung.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

        # Vẽ lại điểm bắt đầu và kết thúc nếu tồn tại
        for y, row in enumerate(MAP):
            for x, cell in enumerate(row):
                if cell == 'o':  # Điểm bắt đầu
                    self.cvs_me_cung.create_oval(x * 21 + 2, y * 21 + 2, (x + 1) * 21 - 2, (y + 1) * 21 - 2, outline='#00FF00', fill='#00FF00')  # Màu xanh lá
                elif cell == 'x':  # Điểm kết thúc
                    self.cvs_me_cung.create_rectangle(x * 21 + 2, y * 21 + 2, (x + 1) * 21 - 2, (y + 1) * 21 - 2, outline='#FF0000', fill='#FF0000')  # Màu đỏ

    def btn_reset_click(self):
        # Kiểm tra nếu đường đi đang được hiển thị
        if self.is_displaying_path:
            messagebox.showerror("Lỗi", "Không thể làm mới khi đường đi đang hiển thị. Vui lòng đợi đến khi hoàn thành.")
            return

        # Đặt lại canvas và bản đồ
        self.cvs_me_cung.delete(tk.ALL)
        self.image_tk = ImageTk.PhotoImage(generate_map_image())
        self.cvs_me_cung.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
        self.dem = 0
        for x in range(len(MAP)):
            for y in range(len(MAP[x])):
                if MAP[x][y] == 'o' or MAP[x][y] == 'x':
                    MAP[x][y] = ' '

if __name__ == "__main__":
    app = App()
    app.mainloop()
