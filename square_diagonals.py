from PIL import Image, ImageDraw
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
def invert_color(c):
    return (255-c[0], 255-c[1], 255-c[2])

DEFAULT_BACKGROUND_COLOR = BLACK
DEFAULT_DRAW_COLOR = (0, 57, 204)

# generates a new image consisting of a grid of size width * height.
# each square contains a diagonal line, whose direction is determined by f : (i, j) -> bool
def generate_image(
    width,
    height,
    f,
    square_size = 50,
    thickness=10,
    highlights=lambda i,j: False,
    background_color=DEFAULT_BACKGROUND_COLOR,
    draw_color=DEFAULT_DRAW_COLOR
):
    img = Image.new('RGB', (width * square_size, height * square_size), background_color)
    draw = ImageDraw.Draw(img)
    
    for i in range(0, width):
        for j in range(0, height):
            if highlights(i,j):
                selected_thickness = int(thickness * 1.2)
                selected_color = invert_color(draw_color)
            else:
                selected_thickness = thickness
                selected_color = draw_color
            if f(i, j):
                draw.line([(i * square_size, j * square_size), ((i+1) * square_size, (j+1) * square_size)], fill=selected_color, width=selected_thickness)
            else:
                draw.line([((i+1) * square_size, j * square_size), (i * square_size, (j+1) * square_size)], fill=selected_color, width=selected_thickness)

    return img

def dual(params):
    return (params[0], params[1], lambda i,j: not params[2](i,j))

def gen_img(p):
    return generate_image(p[0], p[1], p[2])

def box_to_lambda(box):
    box_width = len(box)
    box_height = len(box[0])
    return lambda i,j: box[i % box_width][j % box_height]
def box_highlighter(box, i, j):
    box_width = len(box)
    box_height = len(box[0])
    return lambda i2,j2: (i2 % box_width == i) and (j2 % box_height == j)

def main():
    # f = lambda i,j: (i*j) % 2
    # f = lambda i,j: (i % 2) + ((j-i) % 3)
    # f = lambda i,j: random.randint(0,1)
    # f = box_to_lambda([[0,0], [0,0], [0,1]])
    f = box_to_lambda([[0,1], [0,1], [1,0], [1,0]])

    parameters = (30, 20, lambda i,j: f(i,j) == 0)
    # parameters = (30, 20, lambda i,j: f(i,j) % 2 == 0)
    gen_img(parameters).show()
    # gen_img(dual(parameters)).show()

if __name__ == "__main__":
    main()