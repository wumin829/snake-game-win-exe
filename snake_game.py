"""
贪吃蛇游戏 - Windows版
使用Python标准库tkinter，无需安装额外依赖
"""
import tkinter as tk
import random

class SnakeGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("贪吃蛇 🐍")
        self.window.geometry("400x420")
        self.window.resizable(False, False)
        
        # 游戏区域大小
        self.CANVAS_SIZE = 400
        self.GRID_SIZE = 20
        self.GRID_COUNT = self.CANVAS_SIZE // self.GRID_SIZE
        
        # 画布
        self.canvas = tk.Canvas(self.window, width=self.CANVAS_SIZE, height=self.CANVAS_SIZE, bg="#2d2d2d")
        self.canvas.pack()
        
        # 分数显示
        self.score_label = tk.Label(self.window, text="分数: 0", font=("Arial", 14), bg="#1a1a1a", fg="white")
        self.score_label.pack(fill=tk.X, pady=5)
        
        # 游戏状态
        self.snake = [(10, 10), (9, 10), (8, 10)]  # 蛇身列表
        self.direction = "Right"  # 初始方向
        self.food = None
        self.score = 0
        self.game_running = False
        self.speed = 100  # 毫秒
        
        # 绑定键盘
        self.window.bind("<KeyPress>", self.on_key_press)
        
        # 绘制初始画面
        self.draw_border()
        self.spawn_food()
        self.draw_snake()
        self.draw_food()
        
        # 开始按钮
        self.start_btn = tk.Button(self.window, text="开始游戏", command=self.start_game, 
                                   font=("Arial", 12), bg="#4CAF50", fg="white", width=15)
        self.start_btn.pack(pady=5)
        
        self.window.mainloop()
    
    def draw_border(self):
        """绘制边框"""
        self.canvas.create_rectangle(2, 2, self.CANVAS_SIZE-2, self.CANVAS_SIZE-2, 
                                     outline="#555555", width=2)
    
    def spawn_food(self):
        """生成食物"""
        while True:
            x = random.randint(0, self.GRID_COUNT - 1)
            y = random.randint(0, self.GRID_COUNT - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break
    
    def draw_snake(self):
        """绘制蛇"""
        self.canvas.delete("snake")
        for i, (x, y) in enumerate(self.snake):
            color = "#00FF00" if i == 0 else "#32CD32"  # 头部亮一点
            x1 = x * self.GRID_SIZE
            y1 = y * self.GRID_SIZE
            x2 = x1 + self.GRID_SIZE
            y2 = y1 + self.GRID_SIZE
            self.canvas.create_rectangle(x1+2, y1+2, x2-2, y2-2, 
                                        fill=color, outline="#228B22", tags="snake")
    
    def draw_food(self):
        """绘制食物"""
        self.canvas.delete("food")
        if self.food:
            x, y = self.food
            x1 = x * self.GRID_SIZE
            y1 = y * self.GRID_SIZE
            x2 = x1 + self.GRID_SIZE
            y2 = y1 + self.GRID_SIZE
            self.canvas.create_oval(x1+3, y1+3, x2-3, y2-3, 
                                    fill="#FF6B6B", outline="#FF4500", tags="food")
    
    def on_key_press(self, event):
        """键盘控制"""
        key = event.keysym
        directions = {
            "Up": "Down",
            "Down": "Up", 
            "Left": "Right",
            "Right": "Left"
        }
        if key in directions and self.direction != directions[key]:
            self.direction = key
    
    def start_game(self):
        """开始游戏"""
        if not self.game_running:
            self.game_running = True
            self.start_btn.config(text="游戏中...", state=tk.DISABLED)
            self.game_loop()
    
    def move(self):
        """移动蛇"""
        head_x, head_y = self.snake[0]
        
        if self.direction == "Up":
            new_head = (head_x, head_y - 1)
        elif self.direction == "Down":
            new_head = (head_x, head_y + 1)
        elif self.direction == "Left":
            new_head = (head_x - 1, head_y)
        else:
            new_head = (head_x + 1, head_y)
        
        # 检查撞墙
        if (new_head[0] < 0 or new_head[0] >= self.GRID_COUNT or
            new_head[1] < 0 or new_head[1] >= self.GRID_COUNT):
            self.game_over()
            return
        
        # 检查撞自己
        if new_head in self.snake:
            self.game_over()
            return
        
        # 移动
        self.snake.insert(0, new_head)
        
        # 吃食物
        if new_head == self.food:
            self.score += 10
            self.score_label.config(text=f"分数: {self.score}")
            self.spawn_food()
            self.draw_food()
            
            # 每50分加速
            if self.score % 50 == 0 and self.speed > 50:
                self.speed -= 5
        else:
            self.snake.pop()
        
        self.draw_snake()
    
    def game_loop(self):
        """游戏循环"""
        if self.game_running:
            self.move()
            if self.game_running:
                self.window.after(self.speed, self.game_loop)
    
    def game_over(self):
        """游戏结束"""
        self.game_running = False
        self.canvas.create_text(self.CANVAS_SIZE/2, self.CANVAS_SIZE/2, 
                               text=f"游戏结束!\n最终得分: {self.score}", 
                               fill="white", font=("Arial", 20, "bold"))
        self.start_btn.config(text="重新开始", state=tk.NORMAL)
        
        # 重置游戏
        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.direction = "Right"
        self.score = 0
        self.speed = 100
        self.score_label.config(text="分数: 0")
        self.spawn_food()
        self.draw_snake()
        self.draw_food()

if __name__ == "__main__":
    SnakeGame()
