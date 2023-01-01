import pygame as pg
import math

class weapon:

    def __init__(self,x,y,damge,target_loc,img="source of img"):

        self.x = x
        self.y = y
        self.damge = damge
        self.speed = 10
        self.img = pg.image.load(img).convert()
        self.rect = pg.Rect(self.x,self.y,self.img.get_width(),self.img.get_height())
        self.dx,self.dy = 0 , 0
        self.img.set_colorkey((255,255,255))
        self.r = math.atan2(target_loc[1] - self.rect.center[1] ,target_loc[0] - self.rect.center[0])
        self.img_copy = pg.transform.rotate(self.img,math.degrees(self.r) * -1)
        
       
    def rotate_update(self,win,targtes,dt,targing=(0,0)):

        win.blit(self.img_copy,(self.rect.x - int(self.img_copy.get_width()/2),self.rect.y - int(self.img_copy.get_height()/2)))
        
        self.dx = math.cos(self.r) * self.speed 
        self.dy = math.sin(self.r) * self.speed
        
        self.rect.x += self.dx * dt
        self.rect.y += self.dy * dt

        hit = self.collied(targtes)
        return hit
    
    def collied(self,targets):
        
        for t in targets:
            if self.rect.colliderect(t.rect):
                t.health -= self.damge
                return True


