from random import randint
import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter.colorchooser import askcolor

from PIL import Image, ImageTk

import square_diagonals


# create window

window = tkinter.Tk()
window.title('boxGen v0.0.0')
window.geometry('1000x800')


# initialize box

square_type = square_diagonals.SquareTypes.DIAGONAL
box_width = 3
box_height = 2
box = [[0] * box_height for i in range(box_width)]
box_highlight = None
background_color = square_diagonals.DEFAULT_BACKGROUND_COLOR
draw_color = square_diagonals.DEFAULT_DRAW_COLOR

def generate_images():
    global box_image, generated_image, resized, converted_box_img, converted_gen_img
    # generate images
    box_image = square_diagonals.generate_image(
        box_width,
        box_height,
        square_diagonals.box_to_lambda(box, square_type=square_type, highlighted=box_highlight),
        square_size=30,
        thickness=7,
        background_color=background_color,
        draw_color=draw_color
    )
    generated_image = square_diagonals.generate_image(
        30,
        20,
        square_diagonals.box_to_lambda(box, square_type=square_type, highlighted=box_highlight),
        square_size=50,
        thickness=10,
        background_color=background_color,
        draw_color=draw_color
    )
    resized = generated_image.crop((0,0,950,570))
    converted_box_img = ImageTk.PhotoImage(box_image)
    converted_gen_img = ImageTk.PhotoImage(resized)

generate_images()

# add the box image to the window
box_label = tkinter.Label(image = converted_box_img)
box_label.image = converted_box_img
box_label.place(x=200, y=0)

# add the large image to the window
image_label = tkinter.Label(image = converted_gen_img)
image_label.image = converted_gen_img
image_label.place(x=0, y=200)


# function that checks whether the two indices are within the box dimensions
def in_bounds(i, j):
    return i < box_width and j < box_height

# updates all images to match the current content of the box
def refresh():
    generate_images()

    # update gui
    box_label.configure(image = converted_box_img)
    box_label.image = converted_box_img
    image_label.configure(image = converted_gen_img)
    image_label.image = converted_gen_img


# add event handling for the box (hovering/clicking)

def box_click_handler(event):
    i = event.x // 30
    j = event.y // 30
    if in_bounds(i, j):
        box[i][j] = (box[i][j] + 1) % square_diagonals.number_of_tiles(square_type)
        refresh()
def box_motion_handler(event):
    global box_highlight
    i = event.x // 30
    j = event.y // 30
    if in_bounds(i, j) and not (box_highlight == (i,j)):
        box_highlight = (i,j)
        refresh()
def box_leave_handler(event):
    global box_highlight
    box_highlight = None
    refresh()
box_label.bind("<Button-1>", box_click_handler)
box_label.bind("<Motion>", box_motion_handler)
box_label.bind("<Leave>", box_leave_handler)


# add buttons for changing box size

def inc_box_width():
    global box_width
    box.append([0] * box_height)
    box_width = box_width + 1
    refresh()
def inc_box_height():
    global box_height
    for i in range(box_width):
        box[i].append(0)
    box_height = box_height + 1
    refresh()
def dec_box_width():
    global box_width
    if box_width == 1:
        return
    del box[-1]
    box_width = box_width - 1
    refresh()
def dec_box_height(): # BUG: when changing from 1x2 to 1x1, there is a list index out of range IndexError
    global box_height
    if box_height == 1:
        return
    for i in range(box_height):
        del box[i][-1]
    box_height = box_height - 1
    refresh()

inc_width_button = Button(window, text="Width++", width=10, height=1, command=inc_box_width)
dec_width_button = Button(window, text="Width--", width=10, height=1, command=dec_box_width)
inc_height_button = Button(window, text="Height++", width=10, height=1, command=inc_box_height)
dec_height_button = Button(window, text="Height--", width=10, height=1, command=dec_box_height)
inc_width_button.place(x=0, y=0)
dec_width_button.place(x=0, y=30)
inc_height_button.place(x=100, y=0)
dec_height_button.place(x=100, y=30)


# add button to switch to dual pattern

def invert_box():
    for i in range(box_width):
        for j in range(box_height):
            box[i][j] = 1 - box[i][j]
    refresh()

dual_button = Button(window, text="Dual pattern", width=24, height=1, command=invert_box)
dual_button.place(x=0, y=60)


# add button to fill pattern randomly
def random_box():
    for i in range(box_width):
        for j in range(box_height):
            box[i][j] = randint(0,square_diagonals.number_of_tiles(square_type)-1)
    refresh()

random_button = Button(window, text="Random", width=24, height=1, command=random_box)
random_button.place(x=0, y=90)

# add button to clear all box entries (the box size delibaretely stays the same)
def reset_box():
    global box
    box = [[0] * box_height for i in range(box_width)]
    refresh()

reset_button = Button(window, text="Reset", width=24, height=1, command=reset_box)
reset_button.place(x=0, y=120)


# color settings

def change_background_color():
    global background_color
    rgb = askcolor(color=background_color)[0]
    if rgb is None:
        return
    background_color = rgb
    refresh()
change_background_color_button = Button(window, text="Change background color", width=20, height=1, command=change_background_color)
change_background_color_button.place(x=350, y=0)
def change_draw_color():
    global draw_color
    rgb = askcolor(color=draw_color)[0]
    if rgb is None:
        return
    draw_color = rgb
    refresh()
change_draw_color_button = Button(window, text="Change line color", width=20, height=1, command=change_draw_color)
change_draw_color_button.place(x=350, y=30)


# add the menu

# main menu bar
menubar = Menu(window)
window.config(menu=menubar)
# File > ...
file_menu = Menu(menubar, tearoff=False)
# File > Image export
def image_export():
    filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG-Image", ".png")])
    if filename is None:
        return
    generated_image.save(filename)
file_menu.add_command(
    label='Export Image...',
    command=image_export,
)
# File > Save pattern
def save_pattern():
    file = filedialog.asksaveasfile(defaultextension=".bgp", filetypes=[("boxGen pattern", ".bgp")])
    if file is None:
        return
    for column in box:
        file.write(','.join(map(str, column)) + '\n')
    file.close()
file_menu.add_command(
    label='Save pattern...',
    command=save_pattern,
)
# File > Open pattern
def open_pattern():
    filename = filedialog.askopenfilename(defaultextension=".bgp", filetypes=[("boxGen pattern", ".bgp")])
    if filename is None:
        return
    with open(filename, "r") as file:
        global box, box_width, box_height
        # reset box
        box = []
        for line in file.readlines():
            column = list(map(lambda x: int(x), line.split(',')))
            box.append(column)
        box_width = len(box)
        box_height = len(box[0])
        refresh()
file_menu.add_command(
    label='Open pattern...',
    command=open_pattern,
)
# add File menu to menubar
menubar.add_cascade(
    label='File',
    menu=file_menu,
)

# Mode > ...
mode_menu = Menu(menubar, tearoff=False)
# Mode > Diagonal
def set_mode_squares_diagonal():
    global square_type
    square_type = square_diagonals.SquareTypes.DIAGONAL
    refresh()
mode_menu.add_command(
    label='Squares (Diagonal)',
    command=set_mode_squares_diagonal,
)
# Mode > Axis parallel
def set_mode_squares_axis_parallel():
    global square_type
    square_type = square_diagonals.SquareTypes.AXIS_PARALLEL
    refresh()
mode_menu.add_command(
    label='Squares (Axis parallel)',
    command=set_mode_squares_axis_parallel,
)
# Mode > Semi circles
def set_mode_squares_semi_circle():
    global square_type
    square_type = square_diagonals.SquareTypes.SEMI_CIRCLE
    refresh()
mode_menu.add_command(
    label='Squares (Semi circle)',
    command=set_mode_squares_semi_circle,
)
# Mode > Quarter circles
def set_mode_squares_quarter_circle():
    global square_type
    square_type = square_diagonals.SquareTypes.QUARTER_CIRCLE
    refresh()
mode_menu.add_command(
    label='Squares (Quarter circle)',
    command=set_mode_squares_quarter_circle,
)
# Mode > Any Squares
def set_mode_squares_any():
    global square_type
    square_type = square_diagonals.SquareTypes.ANY
    refresh()
mode_menu.add_command(
    label='Squares (Any)',
    command=set_mode_squares_any,
)
# add Mode menu to menubar
menubar.add_cascade(
    label='Mode',
    menu=mode_menu,
)


# everything is ready now.

window.mainloop()