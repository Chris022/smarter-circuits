from typing import Type

class Point():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
    def __str__(self) -> None:
        return '({x},{y})'.format(x=self.x,y=self.y)
    def __repr__(self):
        return str(self)
    def __eq__(self, obj):
        return self.x == obj.x and self.y == obj.y
class Feature(Point):
    pass
class EndPoint(Feature):
    pass
class Intersection(Feature):
    pass
class Center(Feature):
    pass
#define new Typealias
point = Type[Point]

#---------------------------------------------------------------

class Rect():
    def __init__(self,center: point,radius: int) -> None:
        self.center = center
        self.radius = radius
    def __str__(self) -> None:
        return 'Rect(center: {center},radius: {radius})'.format(center=self.center,radius=self.radius)
    def __repr__(self):
        return str(self)

#define new Typealias
rect = Type[Rect]