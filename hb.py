import pygame as pg

class HB:
    # HB ----> Health Bar

    def __init__(self,x,y,color,amount,lenth=20,h=2):

        
        self.x = x
        self.y = y
        self.color = color
        self.amount = amount
        self.copy_amount = self.amount
        self.lenth = lenth
        self.reh = False
        self.h = h
        self.rect = pg.Rect(self.x,self.y,self.lenth,self.h)
        self.bordx,self.bordy = 0,0
        self.dt = 0
        
    def render_h(self,win):

        self.bordx, self.bordy = self.rect.x-2,self.rect.y - 2
        pg.draw.rect(win,(235,235,235),(self.bordx ,self.bordy,self.lenth + 4 ,self.rect.height + 4))
        pg.draw.rect(win,(self.color),self.rect)

    def damege_r(self,attack_point=0): # attak_p how many precient damege rudiuse
        if self.dt < 1:
            self.dt += ((attack_point/ self.copy_amount) * 100 ) / 100 * self.rect.width
        if self.dt > 1:
         
        #print(((attack_point/ self.copy_amount) * 100 ) / 100 * self.rect.width)
            self.rect.width -= self.dt
            self.dt = 0
        # convert to presint or 100% scale > num/fullnum * 100
        
        if self.amount:
            self.amount -= attack_point
        
    def re_health(self,item):
        if self.dt < 1:
            self.dt += ((item / self.copy_amount) * 100 ) / 100 * self.rect.width
        if self.dt > 1 and self.amount <= self.copy_amount:
         
        #print(((attack_point/ self.copy_amount) * 100 ) / 100 * self.rect.width)
            self.rect.width += self.dt
            self.dt = 0
        # convert to presint or 100% scale > num/fullnum * 100
        if self.amount <= self.copy_amount:
            
            self.amount += item
        
    def update(self,win,c_rect,attack_point=0):

        self.render_h(win)
        self.damege_r(attack_point)
        self.rect.x,self.rect.y = c_rect[0] ,c_rect[1] - 10
        

class Item:

    def __init__(self,x,y,item_name,img="path"):

        self.img = pg.image.load(img).convert()
        self.rect = pg.Rect(x,y,self.img.get_width(),self.img.get_height())
        self.img.set_colorkey((255,255,255))
        self.item_name = item_name
        self.timer = 0
        
    def render_item(self,win):
        win.blit(pg.transform.scale(self.img,(self.img.get_width()/1.2,self.img.get_height()/1.2)),(self.rect.x,self.rect.y))
        self.timer += 1
        
        
