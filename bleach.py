import pygame
import time

pygame.init()
# Screen setup
screen_width = 1200
screen_height = 600
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Bleach')
pygame.mixer.init()

# Load the image
hud_original = pygame.image.load('unnamed1.png').convert_alpha()

target_width = 430 
target_height = 150 

# 3. Scale it
hud_pannel = pygame.transform.smoothscale(hud_original, (target_width, target_height))
# Background
bg = pygame.transform.scale(pygame.image.load("bleach.jpeg"), (screen_width, screen_height))

# Music
pygame.mixer.music.load('on the precipice of death.mp3')
pygame.mixer.music.play(-1)
#0 for once, 1 for twice 2 for thrice,etc

attackOriginal= [pygame.image.load(f'nattack1{i}.png').convert_alpha() for i in range (0,6)]
# Sprites
#Player
walkRight = [pygame.image.load(f'run{i}.png') for i in range(1, 9)]
walkLeft = [pygame.transform.flip(img, True, False) for img in walkRight]
stanceRight = [pygame.image.load(f'stanced{i}.png') for i in range(4, 20)]
stanceLeft = [pygame.transform.flip(img, True, False) for img in stanceRight]
stanceFinalRight = [pygame.image.load(f'stanced1{i}.png') for i in range(7,10)]
stanceFinalLeft= [pygame.transform.flip(img, True, False) for img in stanceFinalRight]
jumpRight= [pygame.image.load(f'jump{i}.png') for i in range(0,10)]
jumpLeft= [pygame.transform.flip(img, True, False) for img in jumpRight]
dashRight=[ pygame.image.load(f'dash{i}.png') for i in range(1,4)]
dashLeft= [pygame.transform.flip(img, True, False) for img in dashRight]
attackRight= [pygame.image.load(f'nattack{i}.png') for i in range (0,6)]
attackLeft= [pygame.transform.flip(img, True, False) for img in attackRight]
getHitRight= [pygame.image.load(f'hit{i}.png') for i in range(0,10)]
getHitLeft= [pygame.transform.flip(img, True, False) for img in getHitRight]
hitRight= [pygame.image.load(f'hit{i}.png') for i in range(5,10)]
hitLeft=[pygame.transform.flip(img, True, False) for img in hitRight]
standUpRight= [pygame.image.load('stanced1.png'),
    pygame.image.load('stanced2.png'),pygame.image.load('jump1.png'), 
    pygame.image.load('jump2.png'),pygame.image.load('jump7.png'),
    pygame.image.load('jump8.png'),pygame.image.load('jump9.png')]
standUpLeft= [pygame.transform.flip(img, True, False) for img in standUpRight]
getsugatenshoRight =[pygame.image.load(f'getsugatensho{i}.png') for i in range(1,15)]
getsugatenshoLeft =[pygame.transform.flip(img, True, False) for img in getsugatenshoRight]

#Enemy
HwalkRight=[pygame.image.load(f'walk{i}.png') for i in range(2,10)]
HwalkLeft= [pygame.transform.flip(img, True, False) for img in HwalkRight]
HattackRight= [pygame.image.load(f'hattack{i}.png') for i in range(0,10)]
HattackLeft= [pygame.transform.flip(img, True, False) for img in HattackRight]
kickRight= [pygame.image.load(f'kick{i}.png') for i in range(0,3)]
kickLeft= [pygame.transform.flip(img, True, False) for img in kickRight]
attackSeenRight= [pygame.image.load(f'hattack{i}.png') for i in range(7,10)]
attackSeenLeft= [pygame.transform.flip(img, True, False) for img in attackSeenRight]
fallRight= [pygame.image.load(f'fall{i}.png') for i in range(1,5)]
fallLeft= [pygame.transform.flip(img, True, False) for img in fallRight]

# Player class
class Player:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.feet_y = y  # y-coordinate of the character's feet
        self.vel = 5
        self.walkCount = 0
        self.stanceCount = 0
        self.stanceFinal=0
        self.stancephase=0
        self.jumpCount = 11
        self.spjumpCount=0
        self.isJump = False
        self.right = False
        self.left = False
        self.standing = True
        self.dashing= False
        self.dashCount= 0
        self.facing= 1
        self.dashTimer= 10
        self.attacking= False
        self.attackCount= 0
        self.hitbox= pygame.Rect(self.x+10, self.feet_y-4,50, 52 )
        self.gotHit= False
        self.getHitCount=0
        self.stationaryPhase= False
        self.stationaryPhaseCount=0
        self.down= False
        self.downCount= 0
        self.health= 120
        self.signature= False
        self.signatureCount=0
        self.staminaGauge=100
        self.ultimateGauge=200

    def draw(self, win):
        # Select current sprite
        framesPerImg = 3
        limit=0
        sprite = jumpLeft[0]
        
        if not self.standing and not self.isJump and not self.attacking:
            self.stancephase=0
            if self.dashing:
                if self.facing==1:
                    limit= len(dashRight)*framesPerImg
                    sprite=dashRight[self.dashCount// framesPerImg]
                else:
                    limit = len(dashLeft) *framesPerImg
                    sprite = dashLeft[self.dashCount//framesPerImg]
                self.dashCount += 1
                if self.dashCount +1>= limit:
                    self.dashCount = 0
                
                self.dashTimer-=1
                if self.dashTimer<=0:
                    self.dashing= False
                    self.dashCount=0
                    self.dashTimer=10

            elif not self.down:
                if self.left:
                    limit = len(walkLeft) * framesPerImg
                    sprite = walkLeft[self.walkCount // framesPerImg]
                elif self.right:
                    limit = len(walkRight) * framesPerImg
                    sprite = walkRight[self.walkCount // framesPerImg]
                self.walkCount += 1
                if self.walkCount +1 >= limit:
                    self.walkCount = 0
            else:
                if self.facing==1:
                    limit= len(standUpRight)* framesPerImg
                    sprite= standUpRight[self.downCount// framesPerImg]
                else:
                    limit= len(standUpLeft)* framesPerImg
                    sprite= standUpLeft[self.downCount// framesPerImg]
                if self.downCount+1 >=limit:
                    self.downCount=0
                    self.down= False
                self.downCount+=1

        elif self.stationaryPhase: 
            # for the player to stay down for a while
            # just so player doesnt stand up right again like nthg happened
            if self.facing==-1:
                limit= len(hitLeft)*framesPerImg
                sprite= hitLeft[self.stationaryPhaseCount// framesPerImg]
            else:
                limit= len(hitRight)*framesPerImg
                sprite= hitRight[self.stationaryPhaseCount// framesPerImg]
            if self.stationaryPhaseCount+1>= limit:
                self.stationaryPhaseCount=0
                self.down= True
            self.stationaryPhaseCount+=1

        elif self.gotHit: #for the damage taking animation 
            draw_y= 500
            if self.facing==1:
                limit= len(getHitRight)*framesPerImg
                sprite= getHitRight[self.getHitCount//framesPerImg]
            else:
                limit= len(getHitLeft)*framesPerImg
                sprite= getHitLeft[self.getHitCount//framesPerImg]

            if self.getHitCount+1>=limit:
                self.getHitCount=0
                self.gotHit= False
                self.stationaryPhase= True
                self.down= True
                self.stationaryPhaseCount=0
            self.getHitCount+=1

        elif self.attacking:
            if not self.signature:
                self.x+= self.facing/2
                limit= len(attackRight)*framesPerImg
                if self.facing==1:
                    sprite= attackRight[self.attackCount// framesPerImg]
                else:
                    sprite= attackLeft[self.attackCount// framesPerImg]
                self.attackCount+=1
                if self.attackCount+1 >= limit:
                    self.attackCount=0
                    self.attacking=False
            else:
                limit= len(getsugatenshoRight)*framesPerImg
                if self.facing==1:
                    sprite= getsugatenshoRight[self.signatureCount// framesPerImg]
                else:
                    limit= len(getsugatenshoLeft)*framesPerImg
                    sprite= getsugatenshoLeft[self.signatureCount// framesPerImg]
                self.signatureCount+=1
                if self.signatureCount+1>=limit:
                    self.signatureCount=0
                    self.signature= False
                    self.attacking= False

        elif self.isJump:
            if self.facing==1:
                limit = len(jumpRight)* framesPerImg
                sprite= jumpRight[self.spjumpCount//framesPerImg]
            else:
                limit = len(jumpLeft)* framesPerImg
                sprite= jumpLeft[self.spjumpCount//framesPerImg]
            if self.spjumpCount +1>= limit:
                self.spjumpCount=0
            self.spjumpCount += 1
        else:
            if self.stancephase==0: 
                if self.facing==-1:
                    limit = len(stanceLeft) * framesPerImg
                    sprite = stanceLeft[self.stanceCount // framesPerImg]

                elif self.facing==1:
                    limit = len(stanceRight) * framesPerImg
                    sprite = stanceRight[self.stanceCount // framesPerImg]
                self.stanceCount += 1
                if self.stanceCount +1>= limit:
                    self.stanceCount=0
                    self.stancephase=1
            else:
                if self.facing==-1:
                    limit = len(stanceFinalLeft)* framesPerImg
                    sprite = stanceFinalLeft[self.stanceFinal // framesPerImg]
                else:
                    limit = len(stanceFinalRight)* framesPerImg
                    sprite = stanceFinalRight[self.stanceFinal // framesPerImg]
                self.stanceFinal+=1
                if self.stanceFinal+1>= limit:
                    self.stanceFinal=0
                    self.stanceCount=0

        # Draw sprite using feet position
        self.hitbox= pygame.Rect(self.x+10, self.feet_y-4,50, 52 )
        # pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        draw_x= self.x -sprite.get_width()+50
        # Get the width and height of the current frame
        sprite_height = sprite.get_height()
        #didnt work sadly for the x coordinate
        draw_y = self.feet_y - sprite_height+50
        win.blit(sprite, (draw_x, draw_y))

    def hit(self):
        if not self.stationaryPhase:
            self.gotHit=True
            self.attacking= False
            self.stationaryPhase= False
        
#Enemy Class
class Enemy:
    def __init__(self,width,height,x,y):#dunder - double underscore
        self.x= x
        self.feet= y
        self.width= width
        self.height= height
        self.vel=2
        self.facing=-1
        self.walkCount=0
        self.end= [self.width+30,screen_width-230]
        self.attackCount=0
        self.lastattackTimer= time.time()
        self.attacking= False
        self.body_hitbox= pygame.Rect(self.x+10, self.feet-100,70, 125 )
        self.attack_hitbox= pygame.Rect(self.x+10, self.feet-100, 50, 60)
        self.hit= False
        self.hitCount=0
        self.health=500
        self.fallCount= 0
        self.fall= False
        self.damage= False
    
    def draw(self,win):
        framesPerImg=4
        current= time.time()
        if not self.fall:
            if self.damage:
                pass
            if current- self.lastattackTimer > 3.0:
                self.attacking= True
                if not self.hit:
                    if self.facing==1:
                        limit= len(HattackRight)*framesPerImg
                        sprite= HattackRight[self.attackCount//framesPerImg]
                    elif self.facing==-1:
                        limit= len(HattackLeft)*framesPerImg
                        sprite= HattackLeft[self.attackCount//framesPerImg]
                    self.attackCount+=1
                    if self.attackCount+1>=limit:
                        self.attackCount=0 
                        self.attacking= False
                        self.lastattackTimer= time.time()
                
            else:       
                if self.facing==-1:
                    limit= len(HwalkLeft)* framesPerImg
                    sprite= HwalkLeft[self.walkCount//framesPerImg]
                elif self.facing==1:
                    limit= len(HwalkRight)*framesPerImg
                    sprite= HwalkRight[self.walkCount//framesPerImg]
                self.walkCount+=1
                if self.walkCount+1>= limit:
                    self.walkCount=0

            if not self.attacking:
                if self.facing==1:
                    self.body_hitbox= pygame.Rect(self.x+30, self.feet-100,70, 135 )
                    #Adding it here updates the self.hitbox when the character moves
            
                elif self.facing==-1:
                    self.body_hitbox= pygame.Rect(self.x+10, self.feet-100,70, 135 )
            else:
                if self.facing==1:
                    self.body_hitbox= pygame.Rect(self.x+10, self.feet-40,130, 60 )
                    self.attack_hitbox= pygame.Rect(self.x+100, self.feet-30,50, 60)
                else:
                    self.body_hitbox= pygame.Rect(self.x, self.feet-40,130, 60 )
                    self.attack_hitbox= pygame.Rect(self.x, self.feet-30,50, 60)
                #Enemy's attack hitbox
                #pygame.draw.rect(win, (0,255,0), self.attack_hitbox, 2)
            if self.hit:
                if self.facing==1:
                    limit= len(attackSeenRight)* framesPerImg
                    sprite= attackSeenRight[self.hitCount//framesPerImg]
                else:
                    limit= len(attackSeenLeft)* framesPerImg
                    sprite= attackSeenLeft[self.hitCount//framesPerImg]
                self.hitCount+=1
                if self.hitCount+1 >=limit:
                    self.hitCount=0
            #HP
            pygame.draw.rect(win,(255,0,0),(self.body_hitbox[0], self.body_hitbox[1]-20,70,10))
            pygame.draw.rect(win,(0,255,0),(self.body_hitbox[0], self.body_hitbox[1]-20,70-7*(500-self.health)/50,10))
                
        if self.health==0 and not self.fall:
                if self.facing==1:
                    limit= len(fallRight)*framesPerImg
                    sprite= fallRight[self.fallCount// framesPerImg]
                elif self.facing==-1:
                    limit= len(fallLeft)*framesPerImg
                    sprite= fallLeft[self.fallCount// framesPerImg]
                if self.fallCount+1>= limit:
                    self.fallCount=0
                    self.fall= True
                self.fallCount+=1
        elif self.fall:
                if self.facing==1:
                    sprite= fallRight[3]
                else:
                    sprite= fallLeft[3]

        #Enemy's hitbox
        # pygame.draw.rect(win, (255,0,0), self.body_hitbox,2)#2 is for border thickness
        sprite_height= sprite.get_height()
        draw_y= self.feet- sprite_height+50
        win.blit(sprite , (self.x, draw_y))
    
    def move(self):
        if not self.attacking and not self.health==0:
            if self.x==self.end[1]:
                self.facing=-1
            elif self.x==self.end[0]:
                self.facing=1
            self.x+= self.facing* self.vel
        self.draw(win)
    
    def gothit(self):
        self.health-=10
        print(self.health)
    
# Clock and player initialization
clock = pygame.time.Clock()
player = Player(64, 64, 10, 500)
enemy = Enemy(110, 149, 560, 500)
# Redraw function
def redrawwindow():
    win.blit(bg, (0, 0))
    hudPannel()
    enemy.move()
    player.draw(win)
    pygame.display.update()    

def hudPannel():
    pygame.draw.rect(win,(255,0,0),(212,59,212,23))
    pygame.draw.rect(win,(0,255,0),(212,59,212- 53*(120-player.health)/30,22 ))
    pygame.draw.rect(win,(255,255,0),(175,89,188-(100-player.staminaGauge)*1.88,14))
    pygame.draw.rect(win,(0,210,255),(239,116,(200-player.ultimateGauge)*1.8,18))
    win.blit(hud_pannel, (10,10))

def hit():
    player.health-=1
    print(player.health)

# Main game loop
def main():
    run = True
    while run:
        clock.tick(22)
        if player.staminaGauge<100:
            player.staminaGauge+=1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
         
            if event.type == pygame.KEYDOWN:
                if event.key== pygame.K_SPACE:
                    player.standing= False
                    player.attacking= True
                    player.stancephase=0
                
                elif event.key== pygame.K_LSHIFT:
                   if player.vel < player.x < screen_width - player.width - player.vel and player.staminaGauge>=20:
                        player.x+= player.facing*40
                        player.standing= False
                        player.dashing= True
                        player.dashCount=0
                        player.left= False
                        player.right= False
                        player.staminaGauge-=20
                
                elif event.key== pygame.K_z and player.staminaGauge>=80:
                    player.standing= False
                    player.signature= True
                    player.attacking= True
                    player.signatureCount=0
                    player.staminaGauge-=80
                    
        keys = pygame.key.get_pressed()
        # Left/right movement
        if not player.attacking:

            if keys[pygame.K_LEFT] and player.x > player.vel:
                player.x -= player.vel
                player.left = True
                player.right = False
                player.standing = False
                player.facing= -1

            elif keys[pygame.K_RIGHT] and player.x+ player.width+ player.vel < screen_width:
                player.x += player.vel
                player.left = False
                player.right = True
                player.standing = False
                player.facing= 1

            else:
                if not player.dashing:      
                    player.standing = True
                    player.dashCount=0
                player.walkCount = 0
               
        # Jump logic
        if not player.isJump:
            if keys[pygame.K_UP]:
                player.isJump = True
                player.right = False
                player.left = False
                player.standing = False
                player.walkCount=0
        else:
            if player.jumpCount >= -11:
                neg = 1
                if player.jumpCount < 0:
                    neg = -1
                # Update feet_y instead of y
                player.feet_y -= (player.jumpCount ** 2) * 0.5 * neg
                player.x+=player.facing*2
                player.jumpCount -= 1
            else:
                player.jumpCount = 11
                player.isJump = False
                player.feet_y=500
        
        if player.hitbox.colliderect(enemy.body_hitbox):
            if enemy.attacking and player.hitbox.colliderect(enemy.attack_hitbox):
                if enemy.attackCount>=21 and enemy.attackCount<24:
                    hit()
                    if not player.down:
                        enemy.hit= True
                        player.hit()
                #detects player enemy collision 
               
            # will be used for player health decrement
            elif player.attacking:
                if player.attackCount==0:
                    enemy.gothit()
            else:
                enemy.hit= False
                player.stationaryPhase= False
                player.gotHit=False
        else:
            enemy.hit= False
            player.stationaryPhase= False
            player.gotHit=False
        redrawwindow()
    pygame.quit()
main()
