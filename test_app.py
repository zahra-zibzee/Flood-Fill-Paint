import pytest
import tkinter as tk
from app import PaintAndColor


@pytest.fixture
def app():
    """
        Setting up the application adn testing the existence of the canvas
    """
    root = tk.Tk()
    application = PaintAndColor(root)
    yield application
    root.destroy()


def test_button_existence(app):
    """
        Testing the existence of the color and fill buttons
    """
    assert app.color_button is not None
    assert app.fill_button is not None


def test_change_color(app):
    """
        Testing the change of color of the cell with simulated mouse click
    """
    event = tk.Event()
    event.x, event.y = app.x_start + 10, app.y_start + 10  # a defined grid cell
    initial_color = app.canvas.itemcget(app.grid[0][0], "fill")

    app.change_color(event)  # event of clicking
    new_color = app.canvas.itemcget(app.grid[0][0], "fill")

    assert initial_color != new_color  # color should change


def test_flood_fill_entire_grid(app):
    """
        Coloring the entire grid with green when no barriers exist
    """
    app.selected_color = "#00FF00"  # green
    app.flood_fill(0, 0)  # starting to fill from the top-left corner

    # checking if all cells are green
    for row in range(app.grid_size):
        for col in range(app.grid_size):
            assert app.canvas.itemcget(app.grid[row][col], "fill") == "#00FF00"


def test_flood_fill_inside_square(app):
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
        app.canvas.itemconfig(app.grid[row][start_col], fill=boundary_color)  # left 
        app.canvas.itemconfig(app.grid[row][end_col], fill=boundary_color)  # right 
    for col in range(start_col, end_col + 1):
        app.canvas.itemconfig(app.grid[start_row][col], fill=boundary_color)  # top 
        app.canvas.itemconfig(app.grid[end_row][col], fill=boundary_color)  # bottom 

    app.selected_color = fill_color
    app.flood_fill(start_row + 1, start_col + 1)  # flood fill inside the square

    # testing if the interior cells are red
    for row in range(start_row + 1, end_row):
        for col in range(start_col + 1, end_col):
            assert app.canvas.itemcget(app.grid[row][col], "fill") == fill_color

    # testing if the boundary cells remain blue
    for row in range(start_row, end_row + 1):
        assert app.canvas.itemcget(app.grid[row][start_col], "fill") == boundary_color  # left
        assert app.canvas.itemcget(app.grid[row][end_col], "fill") == boundary_color  # right
    for col in range(start_col, end_col + 1):
        assert app.canvas.itemcget(app.grid[start_row][col], "fill") == boundary_color  # top
        assert app.canvas.itemcget(app.grid[end_row][col], "fill") == boundary_color  # bottom
