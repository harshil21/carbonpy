from carbonpy import Element
from ..graphical import forces

from math import cos, sin


class GraphElement(Element):
    def __init__(self, value, comp, x, y):
        super().__init__(value, comp)
        self.x = x
        self.y = y

    def get_coords(self):
        return self.x, self.y

    def calc_attractive_f_mag(self, other):
        dist = forces.calc_dist(other, self)
        return 50 * (dist - 65)

    def calc_attractive_f(self, other):
        force_mag = self.calc_attractive_f_mag(other)
        force_angle = forces.calc_angle(other, self)

        force_x = cos(force_angle) * force_mag
        force_y = sin(force_angle) * force_mag
        return force_x, force_y

    def calc_repulsive_f_mag(self, other):
        dist = forces.calc_dist(other, self)
        if dist < 100:
            dist = 100
        return 10000 * (10 ** 10) / (dist ** dist)

    def calc_repulsive_f(self, other):
        force_mag = self.calc_repulsive_f_mag(other)
        force_angle = forces.calc_angle(other, self)

        force_x = cos(force_angle) * force_mag
        force_y = sin(force_angle) * force_mag
        return force_x, force_y
