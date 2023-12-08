import pygame as pg
from pygame.locals import *

pg.init()
#____[This was seperate but kept getting wierd errors after a few runs]____
#___[Class pulls img from spritesheet and makes the background transparent]__
class Spritesheet:
    def __init__(self,image):
        self.sheet = image

    def get_image(self,frame,width,height,scale,color):
        image = pg.Surface((width,height)).convert_alpha()
#____[blit img from sheet , start at top left corner (0,0)]______
        image.blit(self.sheet,(2,0),((frame*width),0,width,height))
        image = pg.transform.scale(image,(width*scale,height*scale))
        image.set_colorkey(color)
        return image


BLACK =(0,0,0)
win = pg.display.set_mode((500,500))
pg.display.set_caption("Game")
#_____[load images from spritesheet and call method spritesheet-cuts them out]
walk=pg.image.load("sprites\left_right_walk.png").convert_alpha()
sheet = Spritesheet(walk)
#____[put images into a list for easier access later]__________
walk_list = []
for x in range(11):
    walk_list.append(sheet.get_image(x,30,24,3,BLACK))

tu = pg.image.load("turtle.png").convert_alpha()
tus = Spritesheet(tu)
#tui = tus.get_image(0,32,32,2,BLACK)
t_left = []
t_right = []
t_shell = []
for x in range(4):
    t_left.append(tus.get_image(x,30,31,2,BLACK))
for n in range(4,8):
    t_right.append(tus.get_image(n,30,31,2,BLACK))
t_shell.append(tus.get_image(8,30,31,2,BLACK))
t_shell.append(tus.get_image(9,30,31,2,BLACK))

#____[could prob do this better, but wanted to seperate left from right walk img
walk_left = [walk_list[2],walk_list[3],walk_list[4],walk_list[5]]
walk_right = [walk_list[7],walk_list[8],walk_list[9],walk_list[10]]
#___[this is the regular luigi standing
luigi= walk_list[6]
jumping = pg.image.load("sprites\jumping.png").convert_alpha()
jumping.set_colorkey(BLACK)
left_jump = pg.image.load("left_jump.png").convert_alpha()
left_jump.set_colorkey(BLACK)
#______[set all vars to init values]_____
bg = pg.image.load('new_bg.png')
clock= pg.time.Clock()
x = 50
y = 400
width= 64
height =64
vel =5
is_jump = False
jump_count =10
left = False
right = False
walk_count = 0
#____[player class can be model, but need to seperate the draw method for view]
class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.is_jump = False
        self.left = False
        self.right = False
        self.walk_count = 0
        self.jump_count = 0
        self.standing = True
        self.image = walk_list[0]
        self.rect = self.image.get_rect()
#____[hitbox doesnt work yet for player, seemed like it would be a good idea
#____for collision detection but only works on baddie right now]_______
        self.hitbox = (self.x+20,self.y+5,40,60)
        
#___[draws the appropriate image depending on walkcount and direction]___        
    def draw(self,win):
        if self.walk_count + 1 >= 27:
            self.walk_count =0
        if not(self.standing):
            if self.left:
                win.blit(walk_left[self.walk_count//3],(self.x,self.y))
                self.walk_count += 1
            elif self.right:
                win.blit(walk_right[self.walk_count//3],(self.x,self.y))
                self.walk_count += 1
        else:
            if self.right:
                win.blit(walk_right[0],(self.x,self.y))
            else:
                win.blit(walk_left[0],(self.x,self.y))

            self.hitbox = (self.x+20,self.y+5,40,60)
            pg.draw.rect(win,(255,0,0),self.hitbox,2)

        

#______________________[need to adjust jumping, pic left if left + jump]_____________
#_____[if is_jump and left: win.blit(jump left[walkcount//3,(self.x,self.y))

def redrawGameWindow():
    global walk_count
    #win.blit(bg,(0,0))
    if walk_count +1 >=27:
        walk_count = 0
    if left:
        win.blit(walk_left[walk_count//3],(x,y))
        walk_count += 1
        if walk_count > len(walk_left):
            walk_count=0
            
    elif right:

        win.blit(walk_right[walk_count//3],(x,y))
        walk_count +=1
        if walk_count > len(walk_right):
            walk_count = 0
    elif is_jump:
        win.blit(jumping,(x,y))
    else:
        win.blit(luigi,(x,y))
    pg.display.update()
    
class baddie(object):
    def __init__(self,x,y,width,height,end):
        self.t_right = t_right
        self.t_left = t_left
        self.x = x
        self.y = y
        self.walk_count =0
        self.path = [x,end]
        self.vel =3
#____[hitbox shows up but size needs to be adjusted. ]________
        self.hitbox = (self.x +23,self.y+5,32,32)
    def draw(self,win):
        self.move()
#___[4 of each left,right img]_____[upper bound = 12]______
#_______________[showing each img for 3 frames]_____________ 
        if self.walk_count + 1 >= 12:
            self.walk_count =0
  
#____________________[if vel >0 , sprite is walking right. display t_right]______
        if self.vel >0:
            win.blit(self.t_right[self.walk_count //3],(self.x,self.y))
            self.walk_count +=1
 
        else:
#____________________________________________[else display left images]__________
            win.blit(self.t_left[self.walk_count //3],(self.x,self.y))
            self.walk_count +=1
        self.hitbox = (self.x+23,self.y+5,32,32)
        pg.draw.rect(win,(255,0,0),self.hitbox,2)
        
    def move(self):
#__________________________[if moving right]__________________________________
        if self.vel >0:
#___________________________________[if haven't reached furthest right on path]_______
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
                
#___________________________________[change dir , move back other way]_________
            else:
                self.vel =self.vel * -1
                self.x += self.vel
                self.walk_count =0
#______________________________[if moving left]__________________________________
        else:
            if self.x > self.path[0] - self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel *-1
                self.x +=self.vel
                self.walk_count = 0
p1 = player(x,y,width,height)
b1 = baddie(100,410,64,64,300)


run = True
while run:
    clock.tick(27)
    win.fill(BLACK)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
#____[Cant decide if key presses go to controller or event handler file?]___
#____[Need to see if they can be seperated somehow]_______
    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT] and x >vel:
        x -= vel
        left = True
        right = False
    elif keys[pg.K_RIGHT] and x < 500- width- vel:
        x += vel
        right = True
        left = False
    else:
        right = False
        left = False
        walk_count = 0
    if not(is_jump):
        if keys[pg.K_SPACE]:
            is_jump = True
            right = False
            left = False
            walk_count= 0
    else:
        if jump_count >= -10:
            neg = 1
            if jump_count <0:
                neg = -1
                
            y -= (jump_count**2)*0.5*neg
            jump_count -=1
      
        else:
            is_jump = False
            jump_count = 10
    
        


    win.blit(bg,(0,0))
    b1.draw(win)
    redrawGameWindow()

    
    
    pg.display.update()
    
pg.quit()
    

    


