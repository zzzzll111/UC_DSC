import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Circle:
    def __init__(self, center, r):
        self.center = center  # center是一个Point对象
        self.r = r


def calculate_radius(center):
    return math.sqrt(center.x ** 2 + center.y ** 2)


def generate_tangent_circles_info(tangentpoint):
    # 计算半径，确保为整数
    r = int(calculate_radius(tangentpoint))

    # 确定两个圆心的坐标
    x1, y1 = tangentpoint.x + r, tangentpoint.y
    x2, y2 = tangentpoint.x - r, tangentpoint.y

    # 创建两个相切圆的对象，确保圆心和半径都是整数
    circle1 = Circle(Point(x1, y1), r)
    circle2 = Circle(Point(x2, y2), r)

    return circle1, circle2


# 示例用法
if __name__ == "__main__":
    # 指定切点坐标，确保是整数
    tangent_point = Point(3, 9)

    # 生成相切圆的信息
    circle1, circle2 = generate_tangent_circles_info(tangent_point)

    # 打印圆的信息
    print(f"Circle 1: Center ({circle1.center.x}, {circle1.center.y}), Radius {circle1.r}")
    print(f"Circle 2: Center ({circle2.center.x}, {circle2.center.y}), Radius {circle2.r}")
