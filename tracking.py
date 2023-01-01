import pygame,sys,math
pygame.init()

clock = pygame.time.Clock()
win = pygame.display.set_mode((800,600))
pygame.display.set_caption("Text Match")

x,y = 400,300
tx, ty = 0,0
dx,dy = 0,0
run = True
while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            tx,ty = pygame.mouse.get_pos()
   
            rad = math.atan2(ty - y, tx - x)
            dx,dy = math.cos(rad) * 15,math.sin(rad) * 15
    x += dx
    y += dy
    
    pygame.draw.circle(win,(255,255,255),(x,y),20)
    pygame.display.flip()
    win.fill((35,35,35))
    
pygame.quit()
