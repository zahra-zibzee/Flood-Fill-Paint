import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser

class PaintAndColor:
    def __init__(self, root):
        self.root = root
        self.root.title("Draw and Color")

        self.width = 800
        self.height = 600

        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="white")
        self.canvas.pack()

        self.grid_size = 20     # 20x20 grid
        self.cell_size = 20
        self.grid = []

        self.x_start = self.width // 2 - (self.cell_size * self.grid_size) // 2
        self.y_start = self.height // 2 - (self.cell_size * self.grid_size) // 2 - 50

        for row in range(self.grid_size):
            row_cells = []
            for col in range(self.grid_size):
                x1 = self.x_start + col * self.cell_size
                y1 = self.y_start + row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                cell = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
                row_cells.append(cell)
            self.grid.append(row_cells)

        self.canvas.bind("<Button-1>", self.change_color)   # left clicking on the grid will change its color
        self.canvas.bind("<B1-Motion>", self.change_color)  # dragging the mouse will change color of multiple cells
        
        # button to choose color
        self.color_button = ttk.Button(root, text="Paint Color", command=self.paint_color)
        self.color_button.place(x=self.x_start, y = self.y_start + self.grid_size * self.cell_size + 50)

        self.selected_color = "blue"  # default color

        # button to start coloring using flood fill algorithm
        self.fill_button = ttk.Button(root, text="Fill Color", command=self.activate_flood_fill)
        self.fill_button.place(x=self.x_start + (self.cell_size * self.grid_size) - 100, y = self.y_start + self.grid_size * self.cell_size + 50)

        self.flood_fill_mode = False

    def paint_color(self):
        self.flood_fill_mode = False
        color_code = colorchooser.askcolor(title="Choose color")
        if color_code:
            self.selected_color = color_code[1]
    
    def change_color(self, event):
        col = (event.x - self.x_start) // self.cell_size
        row = (event.y - self.y_start) // self.cell_size

        if col < self.grid_size and row < self.grid_size:   # Check if click is within grid
            if self.flood_fill_mode:
                self.flood_fill(row, col)
                self.flood_fill_mode = False
            else:
                cell = self.grid[row][col]
                self.canvas.itemconfig(cell, fill=self.selected_color)

    def activate_flood_fill(self):
        color_code = colorchooser.askcolor(title="Choose color")
        if color_code:
            self.selected_color = color_code[1]
            self.flood_fill_mode = True

    def flood_fill(self, row, col):
        target_color = self.canvas.itemcget(self.grid[row][col], "fill")
        if target_color == self.selected_color:
            return
        self.flood_fill_dfs(row, col, target_color)

    def flood_fill_dfs(self, row, col, target_color):
        if row < 0 or row >= self.grid_size or col < 0 or col >= self.grid_size:
            return
        cell = self.grid[row][col]
        current_color = self.canvas.itemcget(cell, "fill")
        if current_color != target_color:       # reaching a border
            return
        self.canvas.itemconfig(cell, fill=self.selected_color)
        self.flood_fill_dfs(row + 1, col, target_color)
        self.flood_fill_dfs(row - 1, col, target_color)
        self.flood_fill_dfs(row, col + 1, target_color)
        self.flood_fill_dfs(row, col - 1, target_color)
        

        

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintAndColor(root)
    root.mainloop()