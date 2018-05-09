import drawSvg as draw
import datetime
from rdp import rdp

strokeArray = [[30, -40], [0, 0], [-80, -40], [30, -60]]
drawingArray = [
    [[8, 2], [9, 2], [10, 1], [11, 1], [12, 1], [13, 0], [15, 0], [16, -1], [17, -2], [18, -2], [19, -3], [19, -4], [20, -4], [20, -4], [20, -5], [20, -5], [20, -5], [20, -5], [20, -5], [20, -5], [20, -5], [19, -5], [19, -4], [19, -4], [18, -4], [18, -4]],
    [[10, -6], [9, -5], [9, -5], [8, -5], [8, -5], [7, -5], [6, -5], [5, -4], [4, -4], [3, -4], [2, -3], [0, -3], [-1, -2], [-3, -2], [-5, -1], [-7, 0], [-8, 0], [-10, 1], [-12, 2], [-13, 3], [-15, 4], [-16, 5], [-17, 6], [-18, 7], [-19, 7], [-19, 8], [-19, 8], [-19, 8], [-19, 8], [-19, 8], [-18, 7], [-17, 7], [-16, 6], [-15, 5], [-13, 4], [-11, 3], [-10, 2], [-8, 1], [-7, 0], [-6, 0], [-5, -1], [-5, -2], [-5, -2], [-5, -2]],
    [[3, -6], [2, -6], [2, -6], [1, -5], [0, -5], [-1, -4], [-2, -3], [-3, -2], [-5, -2], [-7, -1], [-9, -1], [-10, 0], [-12, 0], [-13, 1], [-15, 1], [-16, 1], [-17, 2], [-17, 2], [-17, 2], [-17, 2], [-17, 1], [-17, 1], [-17, 1]],
    [[-5, 4], [-5, 4], [-5, 4], [-5, 4], [-5, 4], [-5, 4], [-6, 4], [-6, 4]]
]

characterArray2 = [
    [[-6, 2], [-6, 2], [-6, 2], [-5, 2], [-5, 2], [-5, 1], [-5, 1], [-5, 1], [-5, 1], [-5, 1], [-5, 1], [-5, 1], [-5, 1], [-5, 1], [-5, 1], [-5, 1], [-5, 1], [-5, 1], [-5, 1], [-5, 1], [-5, 1], [-5, 1], [-5, 1], [-5, 1], [-4, 1], [-4, 1], [-4, 1], [-4, 1], [-3, 1], [-3, 0], [-3, 0], [-2, 0], [-2, 0], [-2, -1], [-2, -1], [-2, -1], [-2, -1]],
    [[6, 38], [7, 37], [7, 33], [7, 30], [8, 28], [8, 24], [9, 21], [10, 18], [11, 16], [14, 17], [16, 17], [17, 16], [16, 15], [16, 14], [15, 13], [15, 13], [15, 13], [17, 16], [18, 16]],
    [[7, 32], [6, 31], [6, 30], [4, 30], [3, 30], [1, 30], [-2, 25], [-4, 24], [-7, 25], [-9, 24], [-12, 24], [-14, 24], [-16, 24], [-18, 25], [-21, 26], [-22, 27], [-23, 27], [-24, 29]]
]

drawingArray2 = [[[-39, -27], [-39, -27], [-39, -27], [-39, -27], [-39, -27], [-39, -27], [-39, -27], [-39, -27], [-39, -27], [-39, -27], [-38, -26], [-38, -26], [-37, -25], [-37, -25], [-37, -25], [-36, -24], [-36, -24], [-36, -23], [-35, -23], [-35, -22], [-35, -21], [-34, -21], [-34, -20], [-34, -19], [-33, -18], [-33, -17], [-33, -16], [-32, -15], [-32, -14], [-31, -12], [-31, -11], [-30, -9], [-29, -7], [-28, -6], [-27, -4], [-26, -2], [-25, 0], [-24, 2], [-23, 4], [-21, 6], [-20, 8], [-18, 10], [-16, 12], [-15, 14], [-13, 16], [-12, 18], [-10, 20], [-9, 21], [-8, 23], [-7, 25], [-6, 26], [-5, 28], [-4, 29], [-4, 30], [-4, 31], [-3, 32], [-3, 32]]]

#print(characterArray1)


def main(drawingArray):
    d = draw.Drawing(200, 200, origin='center')

    #print (datetime.datetime.now())
    print(strokeArray)
    strokeCount = len(drawingArray)
    print("no of strokes", strokeCount)
    #receive strokes

    for i in range(strokeCount):
        draw_stroke(drawingArray[i], d)
        draw_stroke_min(drawingArray[i], d)
        #draw_minimize(drawingArray[i], d)

    #draw_stroke([[-39, -27], [0, 0], [-3, 32]], d)
    #draw_minimize([[-37, -27], [0, 0], [-5, 32]], d)

    #draw_stroke([[-39, -27], [-39, -27], [-39, -27], [-39, -27], [-39, -27], [-39, -27], [-39, -27], [-39, -27], [-39, -27], [-39, -27], [-38, -26], [-38, -26], [-37, -25], [-37, -25], [-37, -25], [-36, -24], [-36, -24], [-36, -23], [-35, -23], [-35, -22], [-35, -21], [-34, -21], [-34, -20], [-34, -19], [-33, -18], [-33, -17], [-33, -16], [-32, -15], [-32, -14], [-31, -12], [-31, -11], [-30, -9], [-29, -7], [-28, -6], [-27, -4], [-26, -2], [-25, 0], [-24, 2], [-23, 4], [-21, 6], [-20, 8], [-18, 10], [-16, 12], [-15, 14], [-13, 16], [-12, 18], [-10, 20], [-9, 21], [-8, 23], [-7, 25], [-6, 26], [-5, 28], [-4, 29], [-4, 30], [-4, 31], [-3, 32], [-3, 32]], d)
    #draw_stroke_black([[-39, -27], [-36, -24], [-36, -23], [-35, -23], [-35, -21], [-34, -21], [-34, -19], [-33, -18], [-33, -16], [-32, -15], [-32, -14], [-31, -12], [-31, -11], [-29, -7], [-28, -6], [-23, 4], [-21, 6], [-20, 8], [-16, 12], [-15, 14], [-13, 16], [-12, 18], [-9, 21], [-7, 25], [-6, 26], [-5, 28], [-4, 29], [-4, 31], [-3, 32]], d)

    d.setPixelScale(2)  # Set number of pixels per geometry unit
    #d.setRenderSize(400,200)  # Alternative to setPixelScale
    timeString = str(datetime.datetime.now())
    filename = timeString[:19]
    d.saveSvg('character/test' + filename + '.svg')
    d.savePng('character/test' + filename + '.png')
    d.rasterize()  # Display as PNG
    d  # Display as SVG


# draw strokes from raw x y data
def draw_stroke(strokeArray, d):

    r = draw.Path(stroke_width=0.5, stroke='red',
              fill='none', fill_opacity=0.5)
    lineCount = len(strokeArray)

    print("original", strokeArray)
    print("no of orig lines", lineCount)

    for i in range(lineCount):
        if i == 0:
            draw_path(strokeArray[i][0], strokeArray[i][1], r, "start")

        else:
            draw_path(strokeArray[i][0], strokeArray[i][1], r, "point")

    end_stroke(d, r)


# minimize stroke count using rdp
def draw_stroke_min(strokeArray, d):

    r = draw.Path(stroke_width=0.5, stroke='black',
              fill='none', fill_opacity=0.5)
    strokeArray = rdp_stroke(strokeArray)
    lineCount = len(strokeArray)

    print("min", strokeArray)
    print("no of min lines", lineCount)

    for i in range(lineCount):
        if i == 0:
            draw_path(strokeArray[i][0], strokeArray[i][1], r, "start")

        else:
            draw_path(strokeArray[i][0], strokeArray[i][1], r, "point")

    end_stroke(d, r)


def rdp_stroke(strokeArray):

    return rdp(strokeArray, algo="rec", epsilon=1.5)


def draw_path(x, y, multipath, state):
    if state == "start":
        return multipath.M(x,y)
    elif state == "point":
        return multipath.L(x,y)


def end_stroke(drawing, path):
    drawing.append(path)


# not used
def draw_line(x1, y1, x2, y2):
    return draw.Lines(x1, y1, x2, y2, close=False, fill='none', stroke='red')


if __name__ == '__main__':
    main(drawingArray)

