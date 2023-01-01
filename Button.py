import pygame

white = (255,255,255)
# 123
class But:

    def __init__(self,x,y,win,text="button",w=100,h=30):

        self.xp = x
        self.yp = y
        self.win = win
        self.heihgt = h
        self.width = w
        self.rect = pygame.Rect(self.xp,self.yp,self.width,self.heihgt)
        self.text = text

    def mouse(self):
        self.xx,self.xy = pygame.mouse.get_pos()

        self.rt = pygame.Rect(self.xx,self.xy,10,18)
        return self.rt

    def click(self): # chack for mouse click
        '''
            when you click on button 
                This func will 
               return True value
        '''
        for event in pygame.event.get():
            x,y = pygame.mouse.get_pos()
            if self.rect.collidepoint(x,y):
                if event.type == pygame.MOUSEBUTTONDOWN:
                   
                    return True



    ''' 
    display button on the
    screen 
    '''

    def draw(self,pos,size=20,color=(255,255,255),widget=1):

        if widget:
            pygame.draw.rect(self.win,color,self.rect,2)
        else:
            pygame.draw.rect(self.win,color,self.rect)
            
        font = pygame.font.SysFont('Arial',size,True)
        text = font.render(self.text,1,white)
        r = text.get_rect(center=self.rect.center)
        self.win.blit(text,r)


