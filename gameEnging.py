import pygame as pg
from settings import *
from Characters import player, Enimy
import random ,hb, Button, time
from weapons import weapon
pg.mixer.init()

"""
  / if you are programmer and reading this have some respect for yourself please
  stop read rihgt now it's heighly recommended, becuse it may be 
  a painfull exprince. i dont know what am doing so you are so please stop 
   
"""
class Game:

    def __init__(self):
        
        pg.init()
        self.click = True
        self.conter = 30
        self.fps = 60
        self.clock = pg.time.Clock()
        self.win = pg.display.set_mode((w,h))
        self.run = False
        self.main = True
        self.die = False
        self.FPS = 0
        pg.display.set_caption(str(self.FPS))
        self.enimys_list = []
        pg.mixer.music.load("sfx/Bm.mp3")
        self.s_cut = pg.mixer.Sound("sfx/wave_slight.wav")
        self.charging = pg.mixer.Sound("sfx/charging.wav")
        self.shot = pg.mixer.Sound("sfx/sht.wav")
        self.hit = pg.mixer.Sound("sfx/hit2.wav")
        self.hit_p = pg.mixer.Sound("sfx/hit.wav")
        self.pickup_c = pg.mixer.Sound("sfx/pickup.wav")
        self.pickup_h = pg.mixer.Sound("sfx/pickup_health.wav")
        self.sg = pg.mixer.Sound("sfx/sg.wav")
        self.font = pg.font.SysFont('Arial',20,True)
        self.timer = ""
        self.colletions = []
        self.camera_opj = []
        self.inventory = [0,0,0]
        self.inventory_rects = []
        self.shotgun_shot = []
        self.weapons = [pg.image.load("assets/weapons/shotgun.png").convert(),pg.image.load("assets/weapons/slight_wive.png").convert()]
        self.last_time = time.time()
        self.x,self.y = 0,0
        self.rect_invetory()
        self.oringe = (255,255,50)
        self.white = (255,255,255)
        self.curnt = self.white
        self.charge = []
        self.slighter = []
        self.erc = 5
        self.enimy_timer = 1
        self.characters = ["crippo","devil_crippo",
                           "crippo_007"]
        self.chars = [player(w/2-10,h/2 + 60,250) for c in self.characters]
        self.add_animation(self.characters,self.chars)
        self.char_id = 1
        self.muisc,self.sfx = True ,True
        if self.muisc:
            pg.mixer.music.play(-1)
       
        self.fire = 1
        self.fire2 = 1
    def rect_invetory(self):
        x = 2
        for i in self.inventory:

            self.inventory_rects.append(self.get_rect(x,2,60,40))
            x += 62
            
    
    def get_rect(self,x,y,w,h):
        return pg.Rect(x,y,w,h)
    
    def timer_c(self,curnt_time):
            
    
        counting_m = str(curnt_time//60000).zfill(2)
        counting_s = str((curnt_time%60000)//1000).zfill(2)
    
        self.timer = "%s:%s"%(counting_m,counting_s)
        return self.timer 
    
    def text_render(self,text,pos,color=(255,255,255)):
        
        text = self.font.render(text,1,color)
        tr = text.get_rect()
        tr.topright = pos
        self.win.blit(text,tr.center)
        
    def update(self,player,dt):

        
        for i in self.inventory_rects:# rendering inventory
            
            # render weapons
            if self.inventory[self.inventory_rects.index(i)] == 1:
                r = self.weapons[self.inventory_rects.index(i)].get_rect().topleft
                r = ( i.midleft[0] + 10,i.midleft[1] - 10)
                self.weapons[self.inventory_rects.index(i)].set_colorkey((255,255,255))
                self.win.blit(self.weapons[self.inventory_rects.index(i)],r)
                self.curnt = self.oringe
                pg.draw.rect(self.win,self.curnt,(i),2)
                self.curnt = self.white

            if (pg.time.get_ticks()//60000) > 1:
                
                if self.fire >= (60 * 25): # wave chock timer
                    
                    # charger & update and adding it
                    self.charging.play()
                    self.charge.clear()
                    self.x,self.y = player.rect.x,player.rect.y
                    self.charge.append(charge(self.win,10,self.x,self.y,dt))
                    # after charging & we set slighter waves in " self.slighter "
                        
                    self.fire = 0
                    self.charge[0].ch = True
                    self.fire = 0
                    
        
            self.fire += 1
            if (pg.time.get_ticks()//60000) > 1:            
                if self.fire2 >= (60*15):
                    for i in range(4):
                        
                        try:
                            for s in range(random.randint(4,6)):

                                self.shotgun_shot.append(weapon(player.rect.x,player.rect.y,15,(self.enimys_list[s].rect.x,self.enimys_list[s].rect.y),img="assets/weapons/bullit.png"))
                            
                        except:
                            pass
                        self.sg.play()
                    self.fire2 = 0
            
            self.fire2 += 1
     
        self.inventory[0] = 1
        self.inventory[1] = 1
        pg.display.update()
        self.win.fill((45,45,35))
        pg.mixer.music.set_volume(0.05)
  
        
    def Run(self):
        
        self.main_screen()
        p = player(w/2,h/2,250)
        p.frame_database['run'] = p.l_frames('assets/character/'+self.characters[self.char_id]+'/run',[7,7])
        p.frame_database['std'] = p.l_frames('assets/character/'+self.characters[self.char_id]+'/std',[int(self.fps/2),int(self.fps/2)])
      
        while self.run:
            # FPS Clock
            dt = time.time() - self.last_time
            dt *= 60
            self.last_time = time.time()
            
            self.respown_enimy(self.erc)
            self.clock.tick(self.fps)
            curnt_time = pg.time.get_ticks()
            
            self.text_render(self.timer_c(curnt_time),(w/2,0))
            pg.display.set_caption("CRRIPO Bata v0.3.0 |"+str(int(self.clock.get_fps()))+" FPS" +  " | gen: " + str(len(self.enimys_list)))
            
            # Chack The Events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.x,self.y = pg.mouse.get_pos()

                    

            if len(self.charge):
                self.charge[0].charge_render(p.rect.x,p.rect.y,dt)
    
                if self.charge[0].full:
                    
                    try:
                        for s in range(random.randint(4,6)):

                            self.slighter.append(weapon(p.rect.x,p.rect.y,20,
                                (self.enimys_list[s].rect.x,self.enimys_list[s].rect.y),img="assets/weapons/slight_wave.png"))
                    except:
                        pass
                    self.charge[0].full = False
                for s in self.slighter:
                    s.rotate_update(self.win,self.enimys_list,dt)
                    if (pg.time.get_ticks()%60000)//1000 == 15:
                    
                        self.slighter.pop(self.slighter.index(s))
                    
                    
            if p.health_b.amount <= 0:
                self.die = True
                self.died_screen()
            # rendering the inventory
            
            if len(self.shotgun_shot):
                
                for s in self.shotgun_shot:
                    s.rotate_update(self.win,(self.enimys_list),dt)
                    if (pg.time.get_ticks()%60000)//1000 == 15:
                        self.shotgun_shot.pop(self.shotgun_shot.index(s))
                        
            # add opject in one list for the camera update the same list every frame

            if len(self.camera_opj) == 2: # here we chake if or list are not emty so we clear ir
                self.camera_opj.remove(self.camera_opj[1])
                self.camera_opj.remove(self.camera_opj[0])
                # updating the list
            self.camera_opj.append(self.enimys_list)
            self.camera_opj.append(self.colletions)
            self.camera(p,self.camera_opj,0,dt)
            self.update(p,dt)
            # ghost.animat(self.fps,self.win,ghost.frame_database[ghost.action],(p.rect.x,p.rect.y))
            p.animat(self.fps,self.win,p.frame_database[p.action],self.enimys_list,self.shot,dt)
            
            
            for e in self.enimys_list:
                # enimy colliding Handling  and moving
                tl = self.enimys_list.copy()
                tl.pop(tl.index(e))
                e.collide_e(tl)
                try:
                    
                    e.animat(self.fps,self.win,e.frame_database[e.action],(p.rect.x,p.rect.y),dt)
                except:
                    pass
          
                if e.health <= 0:
                    self.enimys_list.pop(self.enimys_list.index(e))
                    self.hit.play()
                    # when enimy die respown coin or enirgy ----------------->
                    if random.randint(0,10):
                        self.colletions.append(hb.Item(e.rect.x,e.rect.y,"coin",img="assets/collection/coin.png"))
                        
                    else:
                        self.colletions.append(hb.Item(e.rect.x,e.rect.y,"health",img="assets/collection/enrige.png"))
                        
                if p.collide(e):
                    self.hit_p.play()
                    p.health_b.damege_r(2)
                    #print(p.health_b.amount)
                    
                        # self.rander_animation()
                        
            self.collecton_c(self.colletions,p)
            targeting = random.choice(self.enimys_list)
            p.shoting(self.fps,(targeting.rect.x,targeting.rect.y),50,(w,h))
            
            
        pg.quit()
    def shougun(self,targ,p):
        shots = []
        t1,t2 = targ
        for i in range(4):
            shots.append(weapon(p.rect.x,p.rect.x,25,(t1+i*i,t2+i*i),img="assets/weapons/bullit.png"))
        return shots
                         
    def respown_enimy(self,en_num):

        
        if (pg.time.get_ticks()%60000)//1000 > 58:
            self.FPS += 1
            
            if self.FPS >= 19 and len(self.enimys_list) < 120:
                self.erc += 2
                self.FPS = 0
             
        if len(self.enimys_list) <= random.randint(1,2):
            
            self.enimys_list.clear()
            l_loc = random.choice([[random.randint(-10,w + 10),0],[-10,random.randint(0,h)],[w + 10,random.randint(-10,h + 10)],[random.randint(-10,w),h+ 10]])
            for e in range(en_num):
                
                self.enimys_list.append(Enimy(l_loc[0],l_loc[1],'ghost',(20,24)))
                self.enimys_list[e].frame_database['ghost'] = self.enimys_list[e].l_frames('assets/ghost',[7,7])

            # respow new kinde of enimys ------------>
            if int(pg.time.get_ticks()//60000) >= 3:
                if self.enimy_timer >= 6000:
                    for e in range(0,int(pg.time.get_ticks()//60000) * 2):
                        l_loc = random.choice([[random.randint(-10,w + 10),0],[-10,random.randint(0,h)],[w + 10,random.randint(-10,h + 10)],[random.randint(-10,w),h+ 10]])
                        self.enimys_list.append(Enimy(l_loc[0],l_loc[1],"bghost",(39,62),health=500,vel=2))
                        self.enimys_list[-1].frame_database['bghost'] = self.enimys_list[-1].l_frames('assets/ghost/bghost',[7,7])

                self.enimy_timer = 1
            
            
            if int(pg.time.get_ticks()//60000) >= 200:
                if self.enimy_timer >= 6000:
                    for e in range(0,int(pg.time.get_ticks()//60000) * 2):
                        l_loc = random.choice([[random.randint(-10,w + 10),0],[-10,random.randint(0,h)],[w + 10,random.randint(-10,h + 10)],[random.randint(-10,w),h+ 10]])
                        self.enimys_list.append(Enimy(l_loc[0],l_loc[1],"greenghost",(40,60),health=500,vel=3))
                        self.enimys_list[-1].frame_database['greenghost'] = self.enimys_list[-1].l_frames('assets/ghost/Gg',[7,7,7])
                        
                self.enimy_timer = 0
            # End ---------->
        self.enimy_timer += 1
            
            
    def rander_animation(self,target_loc):

        for enimy in self.enimys_list:           
            enimy.animat(self.fps,self.win,enimy.frame_database[enimy.action],target_loc)
          
    def collecton_c(self,collections,opj):
        if len(collections):
            # see if there are collition
            for c in collections:
                if c.rect.colliderect(opj.rect):
                    self.colletions.pop(self.colletions.index(c))
                    if c.item_name == "health":
                        opj.health_b.re_health(20)
                        self.pickup_h.play()
                    if c.item_name == "coin":
                        self.pickup_c.play()
                # make itme viench after a monante of time
                if c.timer > int(3600 / 2) and c in  self.colletions: # 30 sec neraly
                    
                     self.colletions.pop(self.colletions.index(c))
                # self.camera(p,self.colletions)
                c.render_item(self.win) # rendering collections
                
    def died_screen(self):
        
        home = pg.image.load("assets/buttons/home_0.png").convert()
        home_rect = pg.Rect(0,0,50,50)
        home.set_colorkey((255,255,255))
        
        
        while self.die:
            self.clock.tick(30)
            #self.win.fill((255,191,128))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.main = False
                    pg.exit()
                    break
                tx,ty = pg.mouse.get_pos()
                if home_rect.collidepoint(tx,ty):
                    pg.draw.rect(self.win,(155,155,100),home_rect)
                if event.type == pg.MOUSEBUTTONDOWN:
                    
                    if home_rect.collidepoint(tx,ty):
                        self.run = False
                        self.main = True
                        
                        # inintlaize things for new game
                        self.FPS = 0
                        self.enimys_list.clear()
                        self.timer = ""
                        self.colletions.clear()
                        self.camera_opj.clear()
                        self.inventory = [0,0,0]
                        self.inventory_rects.clear()
                        self.shotgun_shot.clear()
                        self.x,self.y = 0,0
                        self.rect_invetory()
                        self.oringe = (255,255,50)
                        self.white = (255,255,255)
                        self.curnt = self.white
                        self.charge.clear()
                        self.slighter.clear()
                        self.erc = 5
                        self.enimy_timer = 1
                        self.die = False
                        self.Run()
                    else:
                        
                        # inintlaize things for new game
                        self.FPS = 0
                        self.enimys_list.clear()
                        self.timer = ""
                        self.colletions.clear()
                        self.camera_opj.clear()
                        self.inventory = [0,0,0]
                        self.inventory_rects.clear()
                        self.shotgun_shot.clear()
                        self.x,self.y = 0,0
                        self.rect_invetory()
                        self.oringe = (255,255,50)
                        self.white = (255,255,255)
                        self.curnt = self.white
                        self.charge.clear()
                        self.slighter.clear()
                        self.erc = 5
                        self.enimy_timer = 1
                        self.die = False
                        self.run = True
                        self.Run()                        
                        

            text = self.font.render("Click To Play",1,(255,255,240))
            tr = text.get_rect()
            tr.topright = (w/2 ,h/2 + 100)
            self.win.blit(text,tr.center)
            self.win.blit(home,(10,10))
            pg.display.flip()
            self.win.fill((50,50,40))
            
    def camera(self,p,opjlist_big,s,dt):
        # clearing list

        if p.rect.x >= w/2 + p.rect.width * 10:
            for opjlist in opjlist_big:
                for o in opjlist:
                    if o.rect.x >= p.rect.x:
                         o.rect.x -= p.vel * dt
                             
                         o.dx = 0
                    elif o.rect.x <= p.rect.x:
                         o.rect.x -= p.vel * dt
                         o.dx = 0
                
            p.rect.x -= p.vel - 3 * dt
              
        if p.rect.x < w/2 - p.rect.width * 10:
            for opjlist in opjlist_big:
                for o in opjlist:
                    if o.rect.x <= p.rect.x:
                        o.rect.x += p.vel * dt
                        o.dx = 0
                    elif o.rect.x >= p.rect.x:
                         o.rect.x += p.vel * dt
                         o.dx = 0
            p.rect.x += p.vel * dt
            
        if p.rect.y > w/2 + p.rect.height * 10:
            for opjlist in opjlist_big:
                for o in opjlist:
                    if o.rect.y >= p.rect.y:
                        o.rect.y -= p.vel * dt
                        o.dy = 0
                    elif o.rect.y <= p.rect.y:
                        o.rect.y -= p.vel * dt
                        o.dy = 0
            p.rect.y -= (p.vel - 3) * dt
            
        if p.rect.y < w/2 - p.rect.height * 10:
            for opjlist in opjlist_big:
                for o in opjlist:
                    if o.rect.y <= p.rect.y:
                        o.rect.y += p.vel * dt
                        o.dy = 0
                    elif o.rect.y >= p.rect.y:
                        o.rect.y += p.vel * dt
                        o.dy = 0
            p.rect.y += p.vel * dt

    def main_screen(self):

        # player character side ------------------- >
 
        rect_start = pg.Rect(w/2,h/4,80,30)
        rs,ls = pg.Rect(w/2 - 160,h/2 + 50,80,30),pg.Rect(w/2 + 80,h/2 + 50,80,30) # ra > right side , ls > left side
        rect_start.center = (w/2,h/2 + 200)
        start_b = pg.image.load("assets/buttons/start.png").convert()
        icon = start_b
        icon2 = start_b
        coin = pg.image.load("assets/collection/coin.png").convert()
        coin.set_colorkey((255,255,255))
        start_b.set_colorkey((255,242,0))
        color = (255,242,0)
        # widget panel -------------->
        settings = Button.But(w-80,h-30,self.win,text="settings",w=80)
        inventory = Button.But(w-180,h-30,self.win,text="inventory")
        shop = Button.But(w-280,h-30,self.win,text="shop")
        
        # setting_icon.set_colorkey((255,255,255))
        coin.set_colorkey((255,255,255))
        while self.main:
            self.clock.tick(30)
            self.win.fill((20,25,25))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.main = False
                    break
                tx,ty = pg.mouse.get_pos()
                # start button ---------------------------------------------- >
                if rect_start.collidepoint(tx,ty):
                    color = (255,245,91)
                    if event.type == pg.MOUSEBUTTONDOWN:
                        self.main = False
                        self.run = True

                else:
                    color = (255,242,0)

                # Charcter side ---------------------------------------------- >
                if rs.collidepoint(tx,ty):
                    icon = pg.transform.scale(start_b,(20,23))
                    if event.type == pg.MOUSEBUTTONDOWN:
                        # do somthing
                        if self.char_id < 0 :
                            self.char_id = len(self.characters) - 1
                        else:
                            self.char_id -= 1
               
                elif ls.collidepoint(tx,ty):
                    icon2 = pg.transform.scale(start_b,(20,23))
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if self.char_id > len(self.characters) - 2:
                            self.char_id = 0
                            
                        else:
                            self.char_id += 1
                            
                else:
                    icon = start_b
                    icon2 = start_b
                
            # widget display ---------------------- >
            shop.draw((shop.xp,shop.yp),color=(255,120,40))
            inventory.draw((inventory.xp,inventory.yp),color=(255,120,40))
            settings.draw((settings.xp,settings.yp),color=(255,120,40))
            # widget funcs -------->
            if settings.click():
                
                # open settings ----- lazy to write a comment
                self.settings(1)
            self.chars[self.char_id].just_animat(self.fps,self.win,self.chars[self.char_id].frame_database[self.chars[self.char_id].action])
            # start ---------------- > 
            pg.draw.rect(self.win,color,rect_start)
            img_pos = start_b.get_rect()
        
            r = start_b.get_rect()
            r.center = rect_start.center
            li = icon.get_rect()
            ri = icon.get_rect()
            li.center = ls.center
            ri.center = rs.center
            # Charcter side ---------------------------------------------- >
            self.win.blit(pg.transform.flip(icon,True,False),ri)
            self.win.blit(icon2,li)
          
            self.win.blit(start_b,r)
            pg.display.flip()

    def settings(self,var):
        
        draw = False
        draw2 = False
        check = pg.image.load("assets/buttons/check.png").convert()
        check.set_colorkey((0,0,0))
        check = pg.transform.scale(check,(25,25))
        self.rect = pg.Rect(w/2 - 120, h/2 + 20, 18,18)
        self.rect2 = pg.Rect(w/2 - 120, h/2 + 60, 18,18)
        self.rect3 = pg.Rect(w/2 + 100, h/2 + 35, 6,18)
        self.r = pg.Rect(w/2 + 20,h/2 + 41, 100,4)
        while var:
            self.clock.tick(30)
            self.win.fill((20,25,25))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    var = 0
                    break
                x,y = pg.mouse.get_pos()
                if self.rect.collidepoint(x,y):
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if draw:
                            draw = False
                            self.muisc = False
                            pg.mixer.music.stop()
                        else:
                            draw = True
                            self.muisc = True
                            pg.mixer.music.play(-1)
                        
                if self.rect2.collidepoint(x,y):
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if draw2 :
                            draw2 = False
                            self.sfx = False
                        else:
                            self.sfx = True
                            draw2 = True
                            
                if self.r.collidepoint(x,y) and self.muisc:
                    
                    if event.type == pg.MOUSEBUTTONDOWN:
                         # get new pos to comper
                        self.rect3.x = x
                        pg.mixer.music.set_volume((self.rect3.x - self.r.x)/2000)
                        print((x - self.rect3.x),(self.r.x - self.rect3.x)/10000)
            
            self.text_render("music",(w/2 - 150,h/2),color=(255,255,255))
            pg.draw.rect(self.win,(255,120,40),self.rect,2)
            pg.draw.rect(self.win,(255,120,40),self.rect2,2)
            pg.draw.rect(self.win,(255,255,255),self.r)
            pg.draw.rect(self.win, (255,255,255),self.rect3)
            if draw or self.muisc:
                x,y = self.rect.topleft
                
                self.win.blit(check,(x,y - 6))
            if draw2 or self.sfx:
                x,y = self.rect2.topleft
                self.win.blit(check,(x,y - 6))
            
            self.text_render("sfx",(w/2 - 150,h/2 + 40),color=(255,255,255))
            pg.display.flip()
                
    def add_animation(self,animation,opjs):
        for a in animation:
            opjs[animation.index(a)].frame_database['run'] = opjs[animation.index(a)].l_frames('assets/character/'+a+'/run',[7,7])
            opjs[animation.index(a)].frame_database['std'] = opjs[animation.index(a)].l_frames('assets/character/'+a+'/std',[int(self.fps/2),int(self.fps/2)])
            
class market: # market class
    def __init__(self,loc):
        pass

class charge:
    
    def __init__(self,win,w,x,y,color=(255,55,50)):
        self.win = win
        self.w = w
        self.r = 5
        self.r_c = 0
        self.cs = 8
        self.rs = 1
        self.x = x
        self.y = y
        self.ch = False
        self.color = color
        self.full = False
        
    def charge_render(self,x,y,dt):
        
        if self.ch:
            pg.draw.circle(self.win,(255,255,255),(x,y),self.w,self.r)
            self.w += self.cs
            self.r_c += .2 * dt
            
        if self.r_c >= 2:
            self.r -= self.rs
            self.r_c = 0
        if self.r == 0:
            self.r = 5
        if self.w >= 300:
            self.cs = 10
            self.cs *= -1
            self.rs *- -1
            
        if self.w < -20 and self.ch:
            self.w = 20
            self.r = 5
            self.cs = 8
            self.r_c = 0
            self.rs = 1
            self.full = True
            self.ch = False
                
