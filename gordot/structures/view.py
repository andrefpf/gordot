from dataclasses import dataclass

from gordot.structures import Vector
from gordot.utils import Transform

@dataclass
class View:
    '''
    p0 ------ p1 
    |          |
    |          |
    |          |
    p2 ------ p3 
    '''
    p0: Vector
    p1: Vector
    p2: Vector
    p3: Vector
    
    def normalized(self):
        w = self.width()
        h = self.height()
        v = Vector(-w/2, -h/2)

        ppc = View(
            Vector(0, h),
            Vector(w, h),
            Vector(0, 0), 
            Vector(w, 0)
        )

        ppc.move(v)
        return ppc

    def width(self):
        return (self.p1 - self.p0).size()

    def height(self):
        return (self.p0 - self.p2).size()
    
    def min(self):
        return self.p2
    
    def max(self):
        return self.p1
    
    def center(self):
        return (self.p0 + self.p1 + self.p2 + self.p3) / 4
    
    def up_vector(self):
        return self.p0 - self.p2
    
    def move(self, delta):
        a = self.up_vector().angle(Vector(0,1,0))
        delta.rotate(-a)
        
        matrix = Transform.translate(delta)
        print('pré trans')
        print([
            self.p0,
            self.p1,
            self.p2,
            self.p3,
        ])
        self.p0 @= matrix
        self.p1 @= matrix
        self.p2 @= matrix
        self.p3 @= matrix
        print('pós trans')
        print([
            self.p0,
            self.p1,
            self.p2,
            self.p3,
        ])
        
    def zoom(self, amount, around=None):
        around = self.center()
        
        matrix = Transform.translate(- around) @ Transform.scale(Vector(amount, amount)) @ Transform.translate(around)

        self.p0 @= matrix
        self.p1 @= matrix
        self.p2 @= matrix
        self.p3 @= matrix

    def rotate(self, angle):
        around = self.center()
        matrix = Transform.translate(-around) @ Transform.rotate(angle) @ Transform.translate(around)

        self.p0 @= matrix
        self.p1 @= matrix
        self.p2 @= matrix
        self.p3 @= matrix
    
    def __str__(self) -> str:
        return f"""View(
            [{self.xmin} {self.ymin}],
            [{self.xmax} {self.ymax}],
        )"""
