from random import randint
import tkinter
from tkinter import *
from tkinter import filedialog

from PIL import Image, ImageTk

import square_diagonals


# create window

window = tkinter.Tk()
window.title('boxGen v0.0.0')
window.geometry('1000x800')


# initialize box

box_width = 3
box_height = 2

box = [[0] * box_height for i in range(box_width)]
box_highlight = (lambda i,j: False)
currently_highlighted = None

# generate the box image
box_image = square_diagonals.generate_image(box_width, box_height, square_diagonals.box_to_lambda(box), highlights=box_highlight, square_size=30, thickness=7)

# generate the large image
generated_image = square_diagonals.generate_image(30, 20, square_diagonals.box_to_lambda(box), highlights=box_highlight, square_size=50)
resized = generated_image.crop((0,0,950,570))

# add the box image to the window
converted_box_img = ImageTk.PhotoImage(box_image)
box_label = tkinter.Label(image = converted_box_img)
box_label.image = converted_box_img
box_label.place(x=200, y=0)

# add the large image to the window
converted_gen_img = ImageTk.PhotoImage(resized)
image_label = tkinter.Label(image = converted_gen_img)
image_label.image = converted_gen_img
image_label.place(x=0, y=200)


# function that checks whether the two indices are within the box dimensions
def in_bounds(i, j):
    return i < box_width and j < box_height

# updates all images to match the current content of the box
def refresh():
    global box_image, generated_image, resized, converted_box_img, converted_gen_img
    # generate images
    box_image = square_diagonals.generate_image(box_width, box_height, square_diagonals.box_to_lambda(box), highlights=box_highlight, square_size=30, thickness=7)
    generated_image = square_diagonals.generate_image(30, 20, square_diagonals.box_to_lambda(box), highlights=box_highlight, square_size=50)
    resized = generated_image.crop((0,0,950,570))
    converted_box_img = ImageTk.PhotoImage(box_image)
    converted_gen_img = ImageTk.PhotoImage(resized)

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
        box[i][j] = 1 - box[i][j]
        refresh()
def box_motion_handler(event):
    global box_highlight, currently_highlighted
    i = event.x // 30
    j = event.y // 30
    if in_bounds(i, j) and not (currently_highlighted == (i,j)):
        box_highlight = square_diagonals.box_highlighter(box, i, j)
        currently_highlighted = (i,j)
        refresh()
def box_leave_handler(event):
    global box_highlight, currently_highlighted
    box_highlight = (lambda i,j: False)
    currently_highlighted = None
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
            box[i][j] = randint(0,1)
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


# everything is ready now.

window.mainloop()