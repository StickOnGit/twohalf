import pygame
import sys
    
from hitdetector import HitDetector
from zshape import ZShape
from zline import ZLine
from zcube import ZCube
from ztetra import ZTetra
from zocta import ZOcta
from zview import ZView
    
def main():
    from random import randint, choice
    from math import sqrt
    
    # init pygame, game objects
    pygame.init()
    Screen = pygame.display.set_mode((640, 480))
    ZScreen = ZView() 
    FPS = 30
    Timer = pygame.time.Clock()
    Seeker = HitDetector()
    
    # init player object
    player_select = [ZCube, ZTetra, ZOcta]
    player_is = 0
    player_stats = (0, 0, 0, 25)
    PlayerObj = player_select[player_is](*player_stats)
    PlayerObj.color = [255, 255, 255]
    
    # queues for objects to live in
    # eventually become pygame sprite Groups?
    bg_q = []
    player_q = [PlayerObj]
    star_q = []
    
    # populate star_q
    for i in xrange(15):
        x = randint(0, ZScreen.w)
        y = randint(0, ZScreen.h)
        z = randint(0, 1200)
        ab = [[x, y, z], [x, y, z + 50]]
        star_class = choice([ZLine, ZCube, ZTetra])
        
        # I KNOW I KNOW
        # THIS IS TEMPORARY
        if star_class == ZLine:
            star = star_class(ab)
        else:
            star = star_class(x, y, z, 35)
        star.color = [randint(140, 180) for i in range(3)]
        star.direction[2] = -40
        star_q.append(star)
    bg_q.extend(star_q)
    allq = (bg_q, player_q)
    while True:
        PlayerObj = player_q[0]
        Screen.fill((0, 0, 0))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            elif e.type == pygame.MOUSEMOTION:
                PlayerObj.move_to_center(e.pos + (None,))
            elif e.type == pygame.MOUSEBUTTONDOWN:
                ZScreen.camera = [e.pos[0], e.pos[1], ZScreen.camera[2]]
                ZScreen.zoom = ZScreen.set_zoom()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_w:
                    PlayerObj.direction[2] += 10
                elif e.key == pygame.K_s:
                    PlayerObj.direction[2] -= 10
                elif e.key == pygame.K_a:
                    ZScreen.camera[2] += 100
                elif e.key == pygame.K_d:
                    ZScreen.camera[2] -= 100
                elif e.key == pygame.K_g:
                    xyz = PlayerObj.center
                    player_is += 1
                    PlayerObj = player_select[player_is % len(player_select)](*player_stats)
                    PlayerObj.move_to_center(xyz)
                    player_q[0] = PlayerObj
        #PlayerObj.rotate(.1, "x")
        PlayerObj.move()
        
        for s in star_q:
            #s.move()
            if s.center[2] < ZScreen.camera[2]:
                c, d = ZScreen.camera[2] + 1600, ZScreen.camera[2] + 1800
                s.move_to_center([randint(a, b) for a, b in zip((0, 0, c), (640, 480, d))])
            
            if Seeker.hitcube_collide(PlayerObj, s):
                # proof that it's looking
                ZScreen.draw_zline(PlayerObj.center, s.center)
                front = min([PlayerObj.center, s.center], key=lambda x: x[2])
                ZScreen.draw_zcirc(front, 6, [55, 55, 230])
                if Seeker.find_collision(PlayerObj, s):
                    # simple way to note they bonked
                    s.color = choice(([200, 55, 55], [55, 200, 55], [55, 55, 200]))
                    
        ZScreen.zdraw(allq)
        pygame.display.flip()
        Timer.tick(FPS)

if __name__ == '__main__':
    main()
    sys.exit(pygame.quit())
    
