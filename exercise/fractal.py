from json import load
from PIL import Image, ImageDraw
from random import uniform
import sys
from math import cos, sin, radians, log, sqrt
import numpy as np

def process_file(r, transformations, width, height, iterations=1, outputfile='out.png'):

    N = len(transformations)
    D = log(N) / log(1/r)
    print(f'Hausdorff Dimension (D): {D:.4f}')


    probability_join = sum(t[0] for t in transformations)

    points = set([(0,0)])

    for i in range(iterations):
        new_points = set()

        for point in points:
            rnd = uniform(0, probability_join)
            p_sum = 0
            for probability, function in transformations:
                p_sum += probability
                if rnd <= p_sum:
                    new_points.add(function(*point))
                    break

        points.update(new_points)

    min_x = min(points, key=lambda p:p[0])[0]
    max_x = max(points, key=lambda p:p[0])[0]
    min_y = min(points, key=lambda p:p[1])[1]
    max_y = max(points, key=lambda p:p[1])[1]
    p_width = max_x - min_x
    p_height = max_y - min_y

    width_scale = (width/p_width)
    height_scale = (height/p_height)
    scale = min(width_scale, height_scale)

    image = Image.new( 'RGB', (width, height))
    draw = ImageDraw.Draw(image)

    for point in points:
        x = (point[0] - min_x) * scale
        y = height - (point[1] - min_y) * scale
        draw.point((x,y))

    image.save( outputfile, "PNG" )
    # image.show()

def parse(filename):
    with open(filename) as f:
        definition = load(f)

    if "width" not in definition: raise ValueError('"width" parameter missing')
    if "height" not in definition: raise ValueError('"height" parameter missing')
    if "iterations" not in definition: raise ValueError('"iterations" parameter missing')
    if "transformations" not in definition: raise ValueError('"transformations" parameter missing')
    if "r" not in definition: raise ValueError('"r" parameter missing')
    if "theta" not in definition: raise ValueError('"theta" parameter missing')

    r = definition['r']
    theta = radians(definition['theta'])

    def make_t_function(expression):
        return lambda x,y: eval(expression, {'x': x, 'y': y, 'cos': cos, 'sin': sin, 'r':r, 'theta':theta, 'sqrt':sqrt})

    definition['transformations'] = [(float(probability), make_t_function(expression) ) for
                                     probability, expression in definition['transformations']]

    return definition, r

if __name__ == "__main__":

    if len(sys.argv) > 1 and sys.argv[1] != '-':
        for filename in sys.argv[1:]:
            result, r = parse(filename.split(".")[0]+".json")
            process_file(r, result['transformations'], result['width'],
                         result['height'], result['iterations'],
                         filename.split('.')[0] + '.png')