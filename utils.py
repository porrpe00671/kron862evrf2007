import math

# Example:
# n = [(54.5, 17.041667, 31.993),
#          (54.5, 17.083333, 31.911),
#          (54.458333, 17.041667, 31.945),
#          (54.458333, 17.083333, 31.866),
#     ]
# bilinear_interpolation(54.4786674627, 17.0470721369, n)
# 31.95798688313631


def bilinear_interpolation(x, y, points):
    points = sorted(points)
    (x1, y1, q11), (_x1, y2, q12), (x2, _y1, q21), (_x2, _y2, q22) = points

    if not x1 <= x <= x2 or not y1 <= y <= y2:
        raise ValueError('(x, y) not within the rectangle')

    return (q11 * (x2 - x) * (y2 - y) +
            q21 * (x - x1) * (y2 - y) +
            q12 * (x2 - x) * (y - y1) +
            q22 * (x - x1) * (y - y1)
            ) / ((x2 - x1) * (y2 - y1) + 0.0)


def find_rectangle_coordinates(points, x, y):

    left_bottom_points = [p for p in points if x - p[0] >= 0 and y - p[1] >= 0]
    right_bottom_points = [
        p for p in points if p[0] - x >= 0 and y - p[1] >= 0]

    left_top_points = [p for p in points if x - p[0] >= 0 and p[1] - y >= 0]
    right_top_points = [
        p for p in points if p[0] - x >= 0 and p[1] - y >= 0]

    left_bottom_points_closest = min(
        left_bottom_points, key=lambda p: math.sqrt((p[0]-x)**2 + (p[1]-y)**2))
    right_bottom_points_closest = min(
        right_bottom_points, key=lambda p: math.sqrt((p[0]-x)**2 + (p[1]-y)**2))

    left_top_points_closest = min(
        left_top_points, key=lambda p: math.sqrt((p[0]-x)**2 + (p[1]-y)**2))
    right_top_points_closest = min(
        right_top_points, key=lambda p: math.sqrt((p[0]-x)**2 + (p[1]-y)**2))

    return [tuple(left_bottom_points_closest), tuple(right_bottom_points_closest), tuple(left_top_points_closest), tuple(right_top_points_closest)]
