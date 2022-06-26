from PIL import Image, ImageDraw
import random
from enum import Enum, auto

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
def invert_color(c):
    return (255-c[0], 255-c[1], 255-c[2])

DEFAULT_BACKGROUND_COLOR = BLACK
DEFAULT_DRAW_COLOR = (0, 57, 204)

class SquareTypes(Enum):
    DIAGONAL = auto()
    AXIS_PARALLEL = auto()
    QUARTER_CIRCLE = auto()
    SEMI_CIRCLE = auto()

# generates a new image consisting of a grid of size width * height.
# the function f should, given a tuple
#     (draw, square_size, thickness, draw_color, i, j),
# use the given draw object to fill in the (i,j)-th square.
def generate_image(
    width,
    height,
    f,
    square_size=50,
    thickness=10,
    background_color=DEFAULT_BACKGROUND_COLOR,
    draw_color=DEFAULT_DRAW_COLOR
):
    img = Image.new('RGB', (width * square_size, height * square_size), background_color)
    draw = ImageDraw.Draw(img)
    
    for i in range(0, width):
        for j in range(0, height):
            f(draw, square_size, thickness, draw_color, i, j)
    return img

def dual(box): # TODO: generalize for different shape types
    return [[1 - box[i][j] for j in range(len(box[0]))] for i in range(len(box))]

def gen_img(p):
    return generate_image(p[0], p[1], p[2])

def center(p1, p2):
    mean = lambda x,y: (x+y)/2
    return (mean(p1[0], p2[0]), mean(p1[1], p2[1]))

def box_to_lambda(box, square_type=SquareTypes.DIAGONAL, highlighted=None):
    box_width = len(box)
    box_height = len(box[0])
    def f(draw, square_size, thickness, draw_color, i, j):
        box_i = i % box_width
        box_j = j % box_height
        square_content = box[box_i][box_j]
        if highlighted == (box_i, box_j):
            selected_thickness = int(thickness * 1.2)
            selected_color = invert_color(draw_color)
        else:
            selected_thickness = thickness
            selected_color = draw_color

        corners = [[(i1 * square_size, i2 * square_size) for i1 in [i, i+1]] for i2 in [j, j+1]]
        horizontal_edge_centers = [center(corners[i][0], corners[i][1]) for i in [0,1]]
        vertical_edge_centers = [center(corners[0][j], corners[1][j]) for j in [0,1]]
        midpoint = center(corners[0][0], corners[1][1])
        
        # check the mode in which the squares should be filled # TODO: add possibility to leave a square blank in each type
        if square_type is SquareTypes.DIAGONAL:
            if square_content == 0:
                draw.line([corners[0][0], corners[1][1]], fill=selected_color, width=selected_thickness)
            elif square_content == 1:
                draw.line([corners[1][0], corners[0][1]], fill=selected_color, width=selected_thickness)
        elif square_type is SquareTypes.AXIS_PARALLEL:
            if square_content == 0:
                draw.line([horizontal_edge_centers[0], horizontal_edge_centers[1]], fill=selected_color, width=selected_thickness)
            elif square_content == 1:
                draw.line([vertical_edge_centers[0], vertical_edge_centers[1]], fill=selected_color, width=selected_thickness)
        elif square_type is SquareTypes.QUARTER_CIRCLE: # TODO
            pass
        elif square_type is SquareTypes.SEMI_CIRCLE: # TODO
            pass
    return f

def main():
    # TODO: fill in some examples
    pass

if __name__ == "__main__":
    main()