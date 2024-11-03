import math
from booleanOperations.booleanGlyph import BooleanGlyph
from icecream import ic
from bezier import Curve
import numpy as np


def find_intersections(glyph: BooleanGlyph, line_start: tuple, line_end: tuple) -> list:
    intersections = []

    for contour in glyph.contours:
        pointPenPoints = contour._points
        lastCurvePoint = None
        for pointIdx, point in enumerate(pointPenPoints):
            segLength = None
            match point[0]:
                case "moveTo":
                    continue
                case "curve":
                    if pointIdx == 0:
                        lastCurvePoint = point
                        continue
                    elif not (len(pointPenPoints) - 1) - pointIdx:
                        points = [point[1], lastCurvePoint[1]]
                        intersection = calculate_intersection(
                            line_start, line_end, points
                        )
                        if intersection:
                            intersections.append(intersection)
                        continue
                    segLength = 4
                case "line":
                    if pointIdx == 0:
                        lastCurvePoint = point
                        continue
                    elif not (len(pointPenPoints) - 1) - pointIdx:
                        points = [pointPenPoints[pointIdx - 1][1], point[1]]
                        intersection = calculate_intersection(
                            line_start, line_end, points
                        )
                        if intersection:
                            intersections.append(intersection)
                        points = [point[1], lastCurvePoint[1]]
                        intersection = calculate_intersection(
                            line_start, line_end, points
                        )
                        if intersection:
                            intersections.append(intersection)
                        continue
                    segLength = 2
                case None:
                    if pointIdx != len(pointPenPoints) - 1:
                        continue
                    segLength = 3

            if not lastCurvePoint or (
                pointIdx != len(pointPenPoints) - 1 and point[0] is not None
            ):
                points = [
                    point[1]
                    for point in pointPenPoints[pointIdx + 1 - segLength : pointIdx + 1]
                ]
            else:
                points = [
                    point[1]
                    for point in pointPenPoints[pointIdx + 1 - segLength : pointIdx + 1]
                ] + [lastCurvePoint[1]]

            if points[0][0] == "line" and points[1][0] == "move":
                return

            intersection = calculate_intersection(line_start, line_end, points)
            if intersection:
                intersections.append(intersection)

    return intersections


def calculate_intersection(line1_start, line1_end, points):

    if len(points) == 2:
        # Handle line segment intersection
        return line_segment_intersection(line1_start, line1_end, points[0], points[1])
    elif len(points) == 4:
        # Handle curve intersection
        return curve_intersection(line1_start, line1_end, points)


def line_segment_intersection(line1_start, line1_end, line2_start, line2_end):
    x1, y1 = line1_start
    x2, y2 = line1_end
    x3, y3 = line2_start
    x4, y4 = line2_end

    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denom == 0:
        return None  # Lines are parallel

    intersect_x = (
        (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)
    ) / denom
    intersect_y = (
        (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)
    ) / denom

    if (
        min(x1, x2) <= intersect_x <= max(x1, x2)
        and min(y1, y2) <= intersect_y <= max(y1, y2)
        and min(x3, x4) <= intersect_x <= max(x3, x4)
        and min(y3, y4) <= intersect_y <= max(y3, y4)
    ):
        return (intersect_x, intersect_y)
    return None


def curve_intersection(line_start, line_end, curve_points):
    # Implement the curve intersection algorithm
    # This function should return the intersection point (x, y) if it exists, otherwise None
    # For simplicity, we can use a numerical method to find intersections

    nodes = np.asfortranarray(
        [
            [
                curve_points[0][0],
                curve_points[1][0],
                curve_points[2][0],
                curve_points[3][0],
            ],
            [
                curve_points[0][1],
                curve_points[1][1],
                curve_points[2][1],
                curve_points[3][1],
            ],
        ]
    )
    curve = Curve(nodes, degree=3)

    line_nodes = np.asfortranarray(
        [
            [line_start[0], line_end[0]],
            [line_start[1], line_end[1]],
        ]
    )
    line = Curve(line_nodes, degree=1)

    intersections = curve.intersect(line)
    if intersections.size > 0:
        x, y = curve.evaluate(intersections[0][0]).tolist()
        return x[0], y[0]

    return None


if __name__ == "__main__":
    from pathlib import Path
    from fontParts.world import OpenFont
    import time

    rfActive = False
    try:
        from mojo import tools  # type: ignore

        font = CurrentFont()  # type: ignore
        rfActive = True
    except:
        rootDir = Path(__file__).parent.parent
        testsDir = rootDir / "tests"
        UFOpath = testsDir / "_.ufo"
        font = OpenFont(UFOpath)

    rGlyph = font["test02"].copy()
    if "intersectionTest" in font:
        del font["intersectionTest"]

    font["intersectionTest"] = rGlyph

    rGlyph = font["intersectionTest"]

    glyph = BooleanGlyph(rGlyph)

    refLine = (-50, -100), (600, 60)

    # TIME COMPARISON

    start_time = time.time()
    intersections = find_intersections(glyph, *refLine)
    end_time = time.time()

    print(f"RB Execution time: {end_time - start_time} seconds")

    if rfActive:
        _glyph = font["intersectionTest"]
        start_time = time.time()
        intersections = tools.IntersectGlyphWithLine(
            _glyph,
            refLine,
        )
        end_time = time.time()

        print(f"RF Execution time: {end_time - start_time} seconds")

    pen = rGlyph.getPen()
    for idx, p in enumerate(intersections):
        if idx == 0:
            pen.moveTo(p)
            continue
        pen.lineTo(p)
    pen.endPath()
    # print(intersections)
# Example usage:
