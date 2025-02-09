import tkinter as tk
from functools import partial

def find_zero_blocks(a, m, n):
    rows, cols = len(a), len(a[0])
    result = []

    # 生成两种可能的尺寸
    possible_shapes = [(m, n), (n, m)]

    # 遍历每一个起始点 (x0, y0)
    for x0 in range(rows):
        for y0 in range(cols):
            # 遍历两种可能的尺寸
            for dx, dy in possible_shapes:
                x1, y1 = x0 + dx - 1, y0 + dy - 1  # 计算结束点

                # 检查矩形是否越界
                if x1 >= rows or y1 >= cols:
                    continue

                # 检查该区域是否所有元素都为0
                is_valid = True
                for x in range(x0, x1 + 1):
                    for y in range(y0, y1 + 1):
                        if a[x][y] != 0:
                            is_valid = False
                            break
                    if not is_valid:
                        break

                # 如果满足条件，记录结果
                if is_valid:
                    result.append(((x0, y0), (x1, y1)))

    return result

def place_blocks_recursively(a, blocks, block_index=0, placement=[]):
    if block_index == len(blocks):
        if all(all(cell == 1 for cell in row) for row in a):
            return placement  # 返回放置方案
        return None

    block_name, (m, n) = blocks[block_index]
    positions = find_zero_blocks(a, m, n)

    for (x0, y0), (x1, y1) in positions:
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                a[x][y] = 1

        result = place_blocks_recursively(a, blocks, block_index + 1, placement + [(block_name, (x0, y0), (x1, y1))])
        if result:
            return result

        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                a[x][y] = 0

    return None

class PuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Puzzle Solver")
        self.grid_size = 8
        self.button_size = 50
        self.a = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.selected_positions = []
        self.buttons = []
        self.solve_btn = None
        self.reset_btn = None
        self.blocks_to_validate = [(1, 3), (1, 2), (1, 1)]  # 先大后小排序
        self.blocks = [
            ("Red1", (4, 2)),
            ("Red2", (3, 2)),
            ("Yellow1", (4, 3)),
            ("Yellow2", (5, 2)),
            ("White1", (3, 3)),
            ("White2", (2, 2)),
            ("Blue1", (5, 1)),
            ("Blue2", (4, 1))
        ]
        self.create_ui()

    def create_ui(self):
        # 创建按钮网格
        for i in range(self.grid_size):
            row_buttons = []
            for j in range(self.grid_size):
                btn = tk.Button(self.root, width=self.button_size // 10, height=self.button_size // 20,
                                bg="white", command=partial(self.set_initial_position, i, j))
                btn.grid(row=i, column=j, padx=1, pady=1)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        # Solve 按钮
        self.solve_btn = tk.Button(self.root, text="Solve", bg="lightblue", state="disabled", command=self.solve)
        self.solve_btn.grid(row=self.grid_size, column=0, columnspan=4)

        # Reset 按钮
        self.reset_btn = tk.Button(self.root, text="Reset", bg="orange", command=self.reset)
        self.reset_btn.grid(row=self.grid_size, column=4, columnspan=4)

    def set_initial_position(self, x, y):
        if len(self.selected_positions) < 6 and self.a[x][y] == 0:
            self.a[x][y] = 1
            self.selected_positions.append((x, y))
            self.buttons[x][y].config(bg="black")
            if len(self.selected_positions) == 6:
                if not self.validate_initial_positions():
                    tk.messagebox.showerror("Error", "Initial positions must form blocks of size 1x1, 1x2, and 1x3.")
                    self.reset()
                else:
                    self.solve_btn.config(state="normal")

    def validate_initial_positions(self):
        pos = set(self.selected_positions)
        for size in self.blocks_to_validate:
            found = False
            for x, y in list(pos):
                # 检查水平
                if all((x, y + i) in pos for i in range(size[1])):
                    for i in range(size[1]):
                        pos.remove((x, y + i))
                    found = True
                    break
                # 检查垂直
                if all((x + i, y) in pos for i in range(size[1])):
                    for i in range(size[1]):
                        pos.remove((x + i, y))
                    found = True
                    break
            if not found:
                return False
        return True

    def solve(self):
        # 开始求解
        solution = place_blocks_recursively(self.a, self.blocks)
        if solution:
            print("找到解决方案：")
            for block_name, (x0, y0), (x1, y1) in solution:
                color = self.get_block_color(block_name)
                for x in range(x0, x1 + 1):
                    for y in range(y0, y1 + 1):
                        self.buttons[x][y].config(bg=color)
        else:
            print("未找到解决方案")

    def reset(self):
        # 清理所有方块
        self.a = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.selected_positions = []
        self.solve_btn.config(state="disabled")
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.buttons[i][j].config(bg="white")

    def get_block_color(self, block_name):
        colors = {
            "Red1": "red",
            "Red2": "darkred",
            "Yellow1": "yellow",
            "Yellow2": "gold",
            "White1": "white",
            "White2": "lightgray",
            "Blue1": "blue",
            "Blue2": "lightblue"
        }
        return colors.get(block_name, "black")

def main():
    root = tk.Tk()
    app = PuzzleApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
