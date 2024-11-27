import math
from simpleai.search import SearchProblem

COSTS = {
    "up": 1.0,
    "down": 1.0,
    "left": 1.0,
    "right": 1.0,
    # "up left": 1.7,
    # "up right": 1.7,
    # "down left": 1.7,
    # "down right": 1.7,
}

class MazeSolver(SearchProblem):
    def __init__(self, board):
        """
        Hàm khởi tạo cho MazeSolver, kế thừa từ SearchProblem.
        - board: Bản đồ mê cung được biểu diễn dưới dạng ma trận 2D.
        - Khởi tạo điểm bắt đầu (initial) và điểm kết thúc (goal) từ kí tự 'o' và 'x'.
        """
        self.board = board
        self.goal = (0, 0)

        # Tìm điểm bắt đầu (o) và điểm kết thúc (x) trên bản đồ
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x].lower() == "o":
                    self.initial = (x, y)
                elif self.board[y][x].lower() == "x":
                    self.goal = (x, y)

        # Gọi hàm khởi tạo của lớp cha với trạng thái ban đầu
        super(MazeSolver, self).__init__(initial_state=self.initial)

    def actions(self, state):
        """
        Hàm xác định các hành động có thể thực hiện từ trạng thái hiện tại.
        - state: Trạng thái hiện tại là một tuple (x, y).
        - Trả về danh sách các hành động có thể di chuyển từ vị trí hiện tại.
        """
        actions = []
        for action in COSTS.keys():
            newx, newy = self.result(state, action)
            # Kiểm tra xem điểm mới có phải là tường (#) hay không
            if self.board[newy][newx] != "#":
                actions.append(action)
        return actions

    def result(self, state, action):
        """
        Hàm tính toán trạng thái mới sau khi thực hiện một hành động từ trạng thái hiện tại.
        - state: Trạng thái hiện tại là một tuple (x, y).
        - action: Hành động cần thực hiện (up, down, left, right).
        - Trả về trạng thái mới sau khi thực hiện hành động.
        """
        x, y = state
        if "up" in action:
            y -= 1
        if "down" in action:
            y += 1
        if "left" in action:
            x -= 1
        if "right" in action:
            x += 1
        return (x, y)

    def is_goal(self, state):
        """
        Hàm kiểm tra xem trạng thái hiện tại có phải là trạng thái đích hay không.
        - state: Trạng thái hiện tại là một tuple (x, y).
        - Trả về True nếu trạng thái hiện tại là đích, ngược lại trả về False.
        """
        return state == self.goal

    def cost(self, state, action, state2):
        """
        Hàm tính toán chi phí để di chuyển từ trạng thái hiện tại đến trạng thái tiếp theo.
        - state: Trạng thái hiện tại.
        - action: Hành động thực hiện.
        - state2: Trạng thái tiếp theo sau khi thực hiện hành động.
        - Trả về chi phí di chuyển, được xác định từ COSTS.
        """
        return COSTS[action]

    def heuristic(self, state):
        """
        Hàm heuristic để ước lượng chi phí từ trạng thái hiện tại đến trạng thái đích.
        - state: Trạng thái hiện tại là một tuple (x, y).
        - Sử dụng khoảng cách Euclidean để tính toán heuristic.
        - Công thức: sqrt((x - gx)^2 + (y - gy)^2), với (gx, gy) là tọa độ của trạng thái đích.
        """
        x, y = state
        gx, gy = self.goal
        return math.sqrt((x - gx) ** 2 + (y - gy) ** 2)
