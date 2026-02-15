import random
import tkinter as tk


CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
INITIAL_SPEED_MS = 120


class SnakeGame:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("贪吃蛇")

        canvas_width = GRID_WIDTH * CELL_SIZE
        canvas_height = GRID_HEIGHT * CELL_SIZE

        self.canvas = tk.Canvas(
            root,
            width=canvas_width,
            height=canvas_height,
            bg="#111",
            highlightthickness=0,
        )
        self.canvas.pack(padx=10, pady=10)

        self.info_var = tk.StringVar()
        self.info_label = tk.Label(root, textvariable=self.info_var, font=("Arial", 12))
        self.info_label.pack(pady=(0, 10))

        self.root.bind("<Up>", lambda _: self.change_direction((0, -1)))
        self.root.bind("<Down>", lambda _: self.change_direction((0, 1)))
        self.root.bind("<Left>", lambda _: self.change_direction((-1, 0)))
        self.root.bind("<Right>", lambda _: self.change_direction((1, 0)))
        self.root.bind("<w>", lambda _: self.change_direction((0, -1)))
        self.root.bind("<s>", lambda _: self.change_direction((0, 1)))
        self.root.bind("<a>", lambda _: self.change_direction((-1, 0)))
        self.root.bind("<d>", lambda _: self.change_direction((1, 0)))
        self.root.bind("<space>", self.toggle_pause)
        self.root.bind("<r>", lambda _: self.restart())

        self.after_id: str | None = None
        self.restart()

    def restart(self) -> None:
        center_x = GRID_WIDTH // 2
        center_y = GRID_HEIGHT // 2
        self.snake = [
            (center_x, center_y),
            (center_x - 1, center_y),
            (center_x - 2, center_y),
        ]
        self.direction = (1, 0)
        self.pending_direction = self.direction
        self.score = 0
        self.speed_ms = INITIAL_SPEED_MS
        self.running = True
        self.paused = False

        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

        self.food = self.random_empty_cell()
        self.draw()
        self.game_loop()

    def toggle_pause(self, _: tk.Event) -> None:
        if not self.running:
            return
        self.paused = not self.paused
        if self.paused:
            self.info_var.set(f"分数: {self.score} ｜ 已暂停（空格继续）")
        else:
            self.game_loop()

    def change_direction(self, new_direction: tuple[int, int]) -> None:
        if not self.running or self.paused:
            return

        dx, dy = self.direction
        ndx, ndy = new_direction
        if (dx + ndx, dy + ndy) == (0, 0):
            return

        self.pending_direction = new_direction

    def random_empty_cell(self) -> tuple[int, int]:
        snake_set = set(self.snake)
        while True:
            pos = (random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))
            if pos not in snake_set:
                return pos

    def game_loop(self) -> None:
        if not self.running or self.paused:
            return

        self.direction = self.pending_direction

        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
            self.game_over()
            return

        body = self.snake[:-1]
        if new_head in body:
            self.game_over()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.speed_ms = max(60, INITIAL_SPEED_MS - self.score * 2)
            if len(self.snake) == GRID_WIDTH * GRID_HEIGHT:
                self.running = False
                self.info_var.set(f"你赢了！最终分数: {self.score}（按 R 重开）")
                self.draw()
                return
            self.food = self.random_empty_cell()
        else:
            self.snake.pop()

        self.draw()
        self.after_id = self.root.after(self.speed_ms, self.game_loop)

    def game_over(self) -> None:
        self.running = False
        self.draw()
        self.info_var.set(f"游戏结束！最终分数: {self.score}（按 R 重开）")

    def draw(self) -> None:
        self.canvas.delete("all")

        for x in range(0, GRID_WIDTH * CELL_SIZE, CELL_SIZE):
            self.canvas.create_line(x, 0, x, GRID_HEIGHT * CELL_SIZE, fill="#1c1c1c")
        for y in range(0, GRID_HEIGHT * CELL_SIZE, CELL_SIZE):
            self.canvas.create_line(0, y, GRID_WIDTH * CELL_SIZE, y, fill="#1c1c1c")

        fx, fy = self.food
        self.draw_cell(fx, fy, "#e74c3c")

        for index, (sx, sy) in enumerate(self.snake):
            color = "#2ecc71" if index == 0 else "#27ae60"
            self.draw_cell(sx, sy, color)

        if self.running and not self.paused:
            self.info_var.set(f"分数: {self.score} ｜ 方向键/WASD 控制 ｜ 空格暂停 ｜ R 重开")

    def draw_cell(self, x: int, y: int, color: str) -> None:
        x1 = x * CELL_SIZE + 1
        y1 = y * CELL_SIZE + 1
        x2 = x1 + CELL_SIZE - 2
        y2 = y1 + CELL_SIZE - 2
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=0)


def main() -> None:
    root = tk.Tk()
    SnakeGame(root)
    root.resizable(False, False)
    root.mainloop()


if __name__ == "__main__":
    main()
