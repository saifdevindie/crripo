import pygame as pg
import math
from hb import HB
from settings import *
from weapons import weapon

        
class player:

    def __init__(self,x,y,health):

        # img >> The path of a animations file
        self.x = x
        self.y = y
        self.health = health
        self.action = 'std'
        self.frame_data = {} # saving name of animation and load a pic of it
        self.frame_database = {} # saveing the dorations of the animations
        self.frame = 0
        self.flip = False
        self.vel = 3
        self.shoting_d = 0
        self.rect = pg.Rect(self.x,self.y,20,20)
        self.health_b = HB(self.rect.topleft[0],self.rect.topleft[1] - 10,(0,0,225),self.health)
        self.shots = []
        
    def l_frames(self,path,frame_doretions):
        
        animation_name = path.split("/")[-1]
        animation_data = []
        n = 0
        for frame in frame_doretions:

            frame_id = animation_name + "_" + str(n)
            image_loc = path + "/" + frame_id + ".png"
            animation_img = pg.image.load(image_loc).convert()
            animation_img.set_colorkey((255,255,255))
            self.frame_data[frame_id] = animation_img
            
            for f in range(frame):
                animation_data.append(frame_id)
            n += 1
            
        return animation_data
            
    def animat(self,fps,win,l_frames,targets,sound,dt):

        key = pg.key.get_pressed()
        pos_old = (self.rect.x,self.rect.y) # set a copy from the old pos
        if key[pg.K_UP]:
            self.rect.y -= self.vel * dt
            self.change_action(self.action,"run")
            
        if key[pg.K_DOWN]:
            self.change_action(self.action,"run")
            self.rect.y += self.vel * dt
            
            
        if key[pg.K_LEFT]: # move left with " <-- "arrow
                
            self.flip = True
            self.change_action(self.action,"run")
            self.rect.x -= self.vel * dt
            
        if key[pg.K_RIGHT]:# move right with " --> " arrow 
    
            self.change_action(self.action,"run")
            self.rect.x += self.vel * dt
            
        if pos_old == (self.rect.x,self.rect.y):
            self.change_action(self.action,"std")
            
        if self.frame >= len(l_frames) - 1:
            self.frame = 0
        self.frame += 1
        

        # animateion handling and updates
        self.health_b.update(win,self.rect.topleft) # update health
        self.img = self.frame_database[self.action][self.frame]
        win.blit(pg.transform.flip(self.frame_data[self.img],self.flip,False),(self.rect.x,self.rect.y))
        # weapons updating
        for shot in self.shots:

            hit = shot.rotate_update(win,targets,dt)
            if hit:
                sound.play()
                self.shots.pop(self.shots.index(shot))
           
    def just_animat(self,fps,win,l_frames):
        self.img = self.frame_database[self.action][self.frame]
        if self.frame >= len(l_frames) - 1:
            self.frame = 0
        self.frame += 1
        self.img = self.frame_database[self.action][self.frame]
        win.blit(pg.transform.flip(self.frame_data[self.img],self.flip,False),(self.rect.x,self.rect.y))
        
    def change_action(self,c_action,new_action):
        if c_action != new_action:
            self.action = new_action
            self.frame = 0

        
    def collide(self,opj):

        if self.rect.colliderect(opj.rect):
            return True

    def shoting(self,fps,target,damege,win_size):
        
        if self.shoting_d > fps/2 + 10:
            
            if target[0] in [x for x in range(10,win_size[0])]:
                if target[1] in [x for x in range(10,win_size[1])]:
                    self.shots.append(weapon(self.rect.x,self.rect.y,damege,target,img="assets/weapons/f1.png"))
                    self.shoting_d = 0
            
        self.shoting_d += 1
        


        
class Enimy:

    def __init__(self,x,y,action,size,health=200,vel=2.5,attack_delay=1):
        
        # img >> The path of a animations file
        self.x = x
        self.y = y
        self.health = health
        self.action = action
        self.frame_data = {} # saving name of animation and load a pic of it
        self.frame_database = {} # saveing the dorations of the animations
        self.r,self.l = False,True
        self.frame = 0
        self.flip = False
        self.vel = vel
        self.dx,self.dy = 0,0
        self.distance = 0
        self.rect = pg.Rect(self.x,self.y,size[0],size[1])
        self.attack_d = 0
        self.attack_delay = attack_delay
        
    def l_frames(self,path,frame_doretions):
        
        animation_name = path.split("/")[-1]
        animation_data = []
        n = 0
        for frame in frame_doretions:

            frame_id = animation_name + "_" + str(n)
            image_loc = path + "/" + frame_id + ".png"
            animation_img = pg.image.load(image_loc).convert()
            animation_img.set_colorkey((255,255,255))
            self.frame_data[frame_id] = animation_img
            
            for f in range(frame):
                animation_data.append(frame_id)
            n += 1
            
            
        return animation_data
            
    def animat(self,fps,win,l_frames,target_loc,dt):

    
        if self.dx < 0: # move left with " <-- "arrow
                
            self.flip = True
            
        if self.dx > 1:# move right with " --> " arrow 
    
            self.flip = False
            

        if self.frame >= len(l_frames) - 1:
            
            self.frame = 0
            rad = math.atan2(target_loc[1] - self.rect.y, target_loc[0] - self.rect.x)
            self.dx,self.dy = math.cos(rad) * self.vel,math.sin(rad) * self.vel
            dectine = math.hypot(target_loc[1] - self.rect.y, target_loc[0] - self.rect.x)
            
        self.frame += 1 # update frame rate
        self.attack_d += 1 # damege duration time for every attack
        
        self.img = self.frame_database[self.action][self.frame]
        win.blit(pg.transform.flip(self.frame_data[self.img],self.flip,False),(self.rect.x,self.rect.y))
        # Updating damege rate or delay ------------>
        if (pg.time.get_ticks()%60000)//1000 > self.attack_delay:
            self.attack_d = self.attack_d
            
        else:
            self.attack_d = 0
            
    def change_action(self,c_action,new_action):
        if c_action != new_action:
            self.action = new_action
            self.frame = 0
            
    def collide_list(self,rects):
        collide_l = []
        
        for re in rects:
            if self.rect.colliderect(re.rect):
                collide_l.append(re.rect)

        return collide_l
    
    def collide_e(self,rects):

        collide = {"top":False,"bottom":False,"right":False,"left":False}
        self.rect.x += self.dx
        
        cl = self.collide_list(rects)
        for c in cl:
            if self.dx > 0:
                self.rect.right = c.left
                collide["right"]
                
            elif self.dx < 0:
                self.rect.left = c.right
                collide["left"] = True

        
        cl = self.collide_list(rects)
        self.rect.y += self.dy
        for c in cl:
            if self.dy > 0:
                self.rect.bottom = c.top
                collide["bottom"] = True
            
            elif self.dy < 0:
                self.rect.top = c.bottom
                collide["top"] = True
