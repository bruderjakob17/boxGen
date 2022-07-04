from PIL import Image, ImageDraw
import random
from enum import Enum, auto

from numpy import square

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
    ANY = auto()
def number_of_tiles(square_type):
    if square_type is SquareTypes.DIAGONAL:
        return 2
    if square_type is SquareTypes.AXIS_PARALLEL:
        return 2
    if square_type is SquareTypes.QUARTER_CIRCLE:
        return 4
    if square_type is SquareTypes.SEMI_CIRCLE:
        return 4
    if square_type is SquareTypes.ANY:
        return 12

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

# applies the function f componentwise to the two pairs x and y
def pointwise(f, x, y):
    return (f(x[0], y[0]), f(x[1], y[1]))
def center(p1, p2):
    mean = lambda x,y: (x+y)/2
    return pointwise(mean, p1, p2)
def mirror(point, center):
    mirror_l = lambda x,y: x + 2*(y-x)
    return pointwise(mirror_l, point, center)
def bounding_box(*points):
    min_x = None
    min_y = None
    max_x = None
    max_y = None
    for (x,y) in points:
        if min_x is None or x < min_x:
            min_x = x
        if min_y is None or y < min_y:
            min_y = y
        if max_x is None or x > max_x:
            max_x = x
        if max_y is None or y > max_y:
            max_y = y
    return ((min_x, min_y), (max_x, max_y))

def box_to_lambda(box, square_type=SquareTypes.DIAGONAL, highlighted=None):
    box_width = len(box)
    box_height = len(box[0])
    def f(draw, square_size, thickness, draw_color, i, j):
        box_i = i % box_width
        box_j = j % box_height
        square_content = box[box_i][box_j]
        square_type2 = None
        if square_type is SquareTypes.ANY: # TODO: improve code
            if square_content in [0,1]:
                square_type2 = SquareTypes.DIAGONAL
                square_content = square_content
            elif square_content in [2,3]:
                square_type2 = SquareTypes.AXIS_PARALLEL
                square_content = square_content - 2
            elif square_content in [4,5,6,7]:
                square_type2 = SquareTypes.QUARTER_CIRCLE
                square_content = square_content - 4
            elif square_content in [8,9,10,11]:
                square_type2 = SquareTypes.SEMI_CIRCLE
                square_content = square_content - 8
        else:
            square_type2 = square_type
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
        if square_type2 is SquareTypes.DIAGONAL:
            if square_content == 0:
                draw.line([corners[0][0], corners[1][1]], fill=selected_color, width=selected_thickness)
            elif square_content == 1:
                draw.line([corners[1][0], corners[0][1]], fill=selected_color, width=selected_thickness)
        elif square_type2 is SquareTypes.AXIS_PARALLEL:
            if square_content == 0:
                draw.line([horizontal_edge_centers[0], horizontal_edge_centers[1]], fill=selected_color, width=selected_thickness)
            elif square_content == 1:
                draw.line([vertical_edge_centers[0], vertical_edge_centers[1]], fill=selected_color, width=selected_thickness)
        elif square_type2 is SquareTypes.QUARTER_CIRCLE:
            if square_content == 0:
                draw.arc([mirror(corners[1][1], corners[0][0]), corners[1][1]], start=0, end=90, fill=selected_color, width=selected_thickness)
            elif square_content == 1:
                draw.arc(bounding_box(mirror(corners[1][0], corners[0][1]), corners[1][0]), start=90, end=180, fill=selected_color, width=selected_thickness)
            elif square_content == 2:
                draw.arc([corners[0][0], mirror(corners[0][0], corners[1][1])], start=180, end=270, fill=selected_color, width=selected_thickness)
            elif square_content == 3:
                draw.arc(bounding_box(mirror(corners[0][1], corners[1][0]), corners[0][1]), start=270, end=0, fill=selected_color, width=selected_thickness)
        elif square_type2 is SquareTypes.SEMI_CIRCLE:
            if square_content == 0:
                draw.arc([mirror(vertical_edge_centers[0], corners[0][0]), vertical_edge_centers[1]], start=0, end=180, fill=selected_color, width=selected_thickness)
            elif square_content == 1:
                draw.arc([horizontal_edge_centers[0], mirror(horizontal_edge_centers[1], corners[1][1])], start=90, end=270, fill=selected_color, width=selected_thickness)
            elif square_content == 2:
                draw.arc([vertical_edge_centers[0], mirror(vertical_edge_centers[1], corners[1][1])], start=180, end=0, fill=selected_color, width=selected_thickness)
            elif square_content == 3:
                draw.arc([mirror(horizontal_edge_centers[0], corners[0][0]), horizontal_edge_centers[1]], start=270, end=90, fill=selected_color, width=selected_thickness)
    return f

def main():
    # TODO: fill in some examples
    pass

if __name__ == "__main__":
    main()