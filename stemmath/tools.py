import math
from booleanOperations.booleanGlyph import BooleanGlyph
from icecream import ic


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
                        points = [point, lastCurvePoint]
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
                        points = [pointPenPoints[pointIdx - 1], point]
                        intersection = calculate_intersection(
                            line_start, line_end, points
                        )
                        if intersection:
                            intersections.append(intersection)
                        points = [point, lastCurvePoint]
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
                points = pointPenPoints[pointIdx + 1 - segLength : pointIdx + 1]
            else:
                points = pointPenPoints[pointIdx + 1 - segLength : pointIdx + 1] + [
                    lastCurvePoint
                ]

            if points[0][0] == "line" and points[1][0] == "move":
                return

            intersection = calculate_intersection(line_start, line_end, points)
            if intersection:
                intersections.append(intersection)

    return intersections


def calculate_intersection(line1_start, line1_end, points):
    ic(points)
    if len(points) == 2:
        # Handle line segment intersection
        return line_segment_intersection(
            line1_start, line1_end, points[0][1:], points[1][1:]
        )
    elif len(points) == 4:
        # Handle curve intersection
        return curve_intersection(line1_start, line1_end, points)


def line_segment_intersection(line1_start, line1_end, line2_start, line2_end):
    # Implement the line segment intersection algorithm
    # This function should return the intersection point (x, y) if it exists, otherwise None
    pass


def curve_intersection(line_start, line_end, curve_points):
    # Implement the curve intersection algorithm
    # This function should return the intersection point (x, y) if it exists, otherwise None
    pass


if __name__ == "__main__":
    from pathlib import Path
    from fontParts.world import OpenFont

    rootDir = Path(__file__).parent.parent
    testsDir = rootDir / "tests"
    UFOpath = testsDir / "_.ufo"
    font = OpenFont(UFOpath)
    glyph = font["test02"]

    glyph = BooleanGlyph(glyph)

    intersections = find_intersections(glyph, (0, 0), (10, 10))
    print(intersections)
# Example usage:
