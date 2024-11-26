# maze_solver.py
import math
from simpleai.search import SearchProblem

# Chi phí di chuyển theo các hướng
COSTS = {
    "up": 1.0,      # Lên
    "down": 1.0,    # Xuống
    "left": 1.0,    # Trái
    "right": 1.0,   # Phải
    # "up left": 1.7,  # Lên trái (đã tắt)
    # "up right": 1.7, # Lên phải (đã tắt)
    # "down left": 1.7, # Xuống trái (đã tắt)
    # "down right": 1.7 # Xuống phải (đã tắt)
}

class MazeSolver(SearchProblem):
    def __init__(self, board):
        self.board = board
        self.goal = (0, 0)
        # Xác định điểm bắt đầu và điểm kết thúc trong mê cung
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x].lower() == "o":
                    self.initial = (x, y)  # Điểm bắt đầu
                elif self.board[y][x].lower() == "x":
                    self.goal = (x, y)     # Điểm kết thúc
        super(MazeSolver, self).__init__(initial_state=self.initial)

    # Xác định các hành động hợp lệ từ một trạng thái (vị trí) nhất định
    def actions(self, state):
        actions = []
        for action in COSTS.keys():
            newx, newy = self.result(state, action)
            # Kiểm tra nếu vị trí mới nằm trong biên của mê cung và không phải là tường
            if 0 <= newy < len(self.board) and 0 <= newx < len(self.board[0]) and self.board[newy][newx] != "#":
                actions.append(action)
        return actions

    # Tính toán vị trí mới sau khi thực hiện một hành động
    def result(self, state, action):
        x, y = state
        if action.count("up"):
            y -= 1
        if action.count("down"):
            y += 1
        if action.count("left"):
            x -= 1
        if action.count("right"):
            x += 1
        return (x, y)

    # Kiểm tra nếu trạng thái hiện tại là mục tiêu (điểm kết thúc)
    def is_goal(self, state):
        return state == self.goal

    # Chi phí di chuyển từ một trạng thái qua một hành động tới trạng thái mới
    def cost(self, state, action, state2):
        return COSTS[action]

    # Hàm heuristic ước lượng khoảng cách từ trạng thái hiện tại đến mục tiêu
    def heuristic(self, state):
        x, y = state
        gx, gy = self.goal
        return math.sqrt((x - gx) ** 2 + (y - gy) ** 2)  # Khoảng cách Euclid
