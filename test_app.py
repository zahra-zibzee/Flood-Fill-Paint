import unittest
import tkinter as tk
from app import PaintAndColor

class TestPaintAndColor(unittest.TestCase):

    def setUp(self):
        """
            Setting up the application adn testing the existence of the canvas
        """
        self.root = tk.Tk()
        self.app = PaintAndColor(self.root)
        self.assertIsNotNone(self.app.canvas)

    def tearDown(self):
        """
            Destroying the window after each test
        """
        self.root.destroy()
        
    def test_button_existence(self):
        """
            Testing the existence of the color and fill buttons
        """
        self.assertIsNotNone(self.app.color_button)
        self.assertIsNotNone(self.app.fill_button)

    def test_change_color(self):
        """
            Testing the change of color of the cell with simulated mouse click
        """
        event = tk.Event()
        event.x, event.y = self.app.x_start + 10, self.app.y_start + 10  # a defined grid cell
        initial_color = self.app.canvas.itemcget(self.app.grid[0][0], "fill")

        self.app.change_color(event)  # event of clicking
        new_color = self.app.canvas.itemcget(self.app.grid[0][0], "fill")

        self.assertNotEqual(initial_color, new_color)  # color should change

    def test_flood_fill_entire_grid(self):
        """
            Coloring the entire grid with green when no barriers exist
        """
        self.app.selected_color = "#00FF00"  # green
        self.app.flood_fill(0, 0)  # starting to fill from the top-left corner

        # checking if all cells are green
        for row in range(self.app.grid_size):
            for col in range(self.app.grid_size):
                self.assertEqual(self.app.canvas.itemcget(self.app.grid[row][col], "fill"), "#00FF00")

    def test_flood_fill_inside_square(self):
        """
            Testing flood fill inside a blue-bordered square.
                1- Filling inside of the square with red.
                2- Testing if the boundary cells remain blue.
                3- Testing if the interior cells are red.
        """

        boundary_color = "#0000FF"  # blue
        fill_color = "#FF0000"  # red
        start_row, start_col = 5, 5
        end_row, end_col = 14, 14

        for row in range(start_row, end_row + 1):
            self.app.canvas.itemconfig(self.app.grid[row][start_col], fill=boundary_color)  # left 
            self.app.canvas.itemconfig(self.app.grid[row][end_col], fill=boundary_color)  # right 
        for col in range(start_col, end_col + 1):
            self.app.canvas.itemconfig(self.app.grid[start_row][col], fill=boundary_color)  # top 
            self.app.canvas.itemconfig(self.app.grid[end_row][col], fill=boundary_color)  # bottom 

        self.app.selected_color = fill_color
        self.app.flood_fill(start_row + 1, start_col + 1)  # flood fill inside the square

        # testing if the interior cells are red
        for row in range(start_row + 1, end_row):
            for col in range(start_col + 1, end_col):
                self.assertEqual(self.app.canvas.itemcget(self.app.grid[row][col], "fill"), fill_color)

        # testing if the boundary cells remain blue
        for row in range(start_row, end_row + 1):
            self.assertEqual(self.app.canvas.itemcget(self.app.grid[row][start_col], "fill"), boundary_color)  # left
            self.assertEqual(self.app.canvas.itemcget(self.app.grid[row][end_col], "fill"), boundary_color)  # right
        for col in range(start_col, end_col + 1):
            self.assertEqual(self.app.canvas.itemcget(self.app.grid[start_row][col], "fill"), boundary_color)  # top
            self.assertEqual(self.app.canvas.itemcget(self.app.grid[end_row][col], "fill"), boundary_color)  # bottom



if __name__ == "__main__":
    unittest.main()
