from pygame import display, draw
from math import sqrt
from listmath import dot, minus
try:
    from twodpt import mathfoo as to_2d
except ImportError:
    from twodpt import altmath as to_2d

class ZView(object):
    def __init__(self):
        self.screen = display.get_surface()
        self.w, self.h = self.screen.get_size()
        self.horizon = [self.w / 2.0, self.h / 2.0, 500.0]
        self.camera = [self.w / 2.0, self.h / 2.0, -100.0]
        self.zoom = self.set_zoom()
        
    def set_zoom(self):
        max_x = max([abs(i - self.camera[0]) for i in 0, self.w])
        max_y = max([abs(j - self.camera[1]) for j in 0, self.h])
        return sqrt(max_x**2 + max_y**2 + abs(self.camera[2]**2)) * 1.618039887
    
    def to_2d_pt(self, cam, xyz):
        result = xyz[:-1]
        if xyz[2] > cam[2]:
            d = xyz[2] - cam[2]
            for i in range(2):
                result[i] = ((result[i] - cam[i]) / d * self.zoom) + cam[i]
        return result
        
    def to_2d_rect(self, rect, z):
        tl = self.to_2d_pt(rect.topleft + (z,))
        br = self.to_2d_pt(rect.bottomright + (z, ))
        return tl[0], tl[1], br[0] - tl[0], br[1] - tl[1]
        
    def to_rect_ptlist(self, rect):
        return rect.topleft, rect.topright, rect.bottomright, rect.bottomleft
        
    def z_color(self, color, z):
        d = 1.0 / ((z - self.camera[2]) / self.zoom)
        return color if d > 1 else [int(max(0, c * d)) for c in color]
        
    def draw_zrect(self, rect, z):
        draw.rect(self.screen, 
                    self.z_color((222, 55, 55), z), 
                    self.to_2d_rect(rect, z),
                    1)
                        
    def draw_zshape(self, zshape):
        for line in zshape.lines:
            if line[0][2] > self.camera[2] and line[1][2] > self.camera[2]:
                draw.line(self.screen,
                        self.z_color(zshape.color, line[1][2]),
                        to_2d.simple_pt(self.camera, line[0], self.zoom),
                        to_2d.simple_pt(self.camera, line[1], self.zoom),
                        1)
                        
    def draw_zline(self, pt1, pt2, color=(60, 60, 180), width=1):
        if pt1[2] > self.camera[2] and pt2[2] > self.camera[2]:
            draw.line(self.screen,
                self.z_color(color, pt2[2]),
                to_2d.simple_pt(self.camera, pt1, self.zoom),
                to_2d.simple_pt(self.camera, pt2, self.zoom),
                width)
                
    def draw_zcirc(self, pt, radius=3, color=(120, 60, 60)):
        if pt[2] > self.camera[2] and pt[2] > self.camera[2]:
            int_pt = [int(x) for x in to_2d.simple_pt(self.camera, pt, self.zoom)]
            draw.circle(self.screen,
                self.z_color(color, pt[2]),
                int_pt,
                radius
            )
    def cull_draw(self, qs):
        self.screen.lock()
        for q in qs:
            for zshape in sorted(q, key=lambda x: x.center[2], reverse=True):
                #for line in zshape.lines:
                for face in zshape.faces:
                    to_cam = minus(face.order[0], self.camera)
                    if dot(to_cam, face.get_norm()) < 0:
                    #if face.get_norm()[-1] < 0:
                        for line in face.lines:
                            self.draw_zline(line[0], line[1], face.color, 1)
                    #if line[0][2] > self.camera[2] and line[1][2] > self.camera[2]:
                    #    draw.line(self.screen,
                    #        self.z_color(zshape.color, line[1][2]),
                    #        to_2d.simple_pt(self.camera, line[0], self.zoom),
                    #        to_2d.simple_pt(self.camera, line[1], self.zoom),
                    #        1)
        self.screen.unlock()
        
    def zdraw(self, qs):
        self.screen.lock()
        for q in qs:
            for zshape in sorted(q, key=lambda x: x.center[2], reverse=True):
                for line in zshape.lines:
                    if line[0][2] > self.camera[2] and line[1][2] > self.camera[2]:
                        draw.line(self.screen,
                            self.z_color(zshape.color, line[1][2]),
                            to_2d.simple_pt(self.camera, line[0], self.zoom),
                            to_2d.simple_pt(self.camera, line[1], self.zoom),
                            1)
        self.screen.unlock()
