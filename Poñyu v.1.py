import pygame
import random
pygame.init()

#GAME WINDOW
canvas_width = 800
canvas_height = 800
window = pygame.display.set_mode((canvas_height,canvas_width))
pygame.display.set_caption("Poñyu GAME♥")
bg = pygame.image.load('bg.png')

clock = pygame.time.Clock()

#MUSIC
bg_music = pygame.mixer.music.load('Music/bg_spooky_music.ogg')
pygame.mixer.music.play(-1)
slime_attack_sound = pygame.mixer.Sound('Music/slime_splash.wav')
cráneo_fuego_hit_sound = pygame.mixer.Sound('Music/hit.wav')
cráneo_fuego_defeated_sound = pygame.mixer.Sound('Music/hot_sizzling.wav')



class Player(object):
    #Indexes of Poñyu's sprites for walking
    char = pygame.image.load('Sprites/Ponyu Sprites/ponyu.png')
    walkRight = [pygame.image.load('Sprites/Ponyu Sprites/ponyu right 1.png'), pygame.image.load('Sprites/Ponyu Sprites/ponyu right 2.png'), pygame.image.load('Sprites/Ponyu Sprites/ponyu right 3.png')]
    walkLeft = [pygame.image.load('Sprites/Ponyu Sprites/ponyu left 1.png'),pygame.image.load('Sprites/Ponyu Sprites/ponyu left 2.png'), pygame.image.load('Sprites/Ponyu Sprites/ponyu left 3.png')]


    #Gives the player/Poñyu object properties like location, size, hitbox, and actions (is it going left or right, jumping, standing still, etc.)
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 10
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.idle = 0
        self.standing = True
        self.hitbox = (self.x + 25, self.y + 25, 75, 75)


    #Animates Poñyu walking left and right
    def draw(self, window):
        if self.walkCount + 1 >= 12:
            self.walkCount = 0
        if not(self.standing):
            if self.left:
                window.blit(self.walkLeft[self.walkCount//4], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                window.blit(self.walkRight[self.walkCount//4], (self.x,self.y))
                self.walkCount += 1
        else:
            if self.right:
                window.blit(self.walkRight[0], (self.x, self.y))
            else:
                window.blit(self.walkLeft[0], (self.x, self.y))
        #Draws its hidden hitbox
        self.hitbox = (self.x +25, self.y + 35, 50, 50)


    #Displays text when Poñyu gets hit by an enemy
    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 60
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('YoU HaVe FaLleN SLiME', 1, (225, 0, 0))
        window.blit(text, ((canvas_width / 2) - (text.get_width() / 2), (canvas_height / 2) - (text.get_height() / 2)))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()



class Projectile(object):
    #Sprites of Poñyu's slimeballs going left and right
    slimeball = pygame.image.load("Sprites/Ponyu Sprites/ponyu_slimeball_right.png")
    slimeball_reverse = pygame.image.load("Sprites/Ponyu Sprites/ponyu_slimeball_left.png")


    #Gives a slimeball object properties like location and speed
    def __init__(self, x, y, facing):
        self.x = x
        self.y = y
        self.facing = 0
        self.vel = 10 * facing


    #Animates the slimeball projectile moving left or right
    def draw(self, window):
        if facing == 1:
            window.blit(self.slimeball, (self.x,self.y))
        else:
            window.blit(self.slimeball_reverse, (self.x,self.y))



class Enemy(object):
    #Indexes of Cráneo Fuego's sprites
    walkRight = [pygame.image.load('Sprites/Cráneo Fuego Sprites/Cráneo Fuego right 1.png'), pygame.image.load('Sprites/Cráneo Fuego Sprites/Cráneo Fuego right 2.png'), pygame.image.load('Sprites/Cráneo Fuego Sprites/Cráneo Fuego right 3.png')]
    walkLeft = [pygame.image.load('Sprites/Cráneo Fuego Sprites/Cráneo Fuego left 1.png'),pygame.image.load('Sprites/Cráneo Fuego Sprites/Cráneo Fuego left 2.png'), pygame.image.load('Sprites/Cráneo Fuego Sprites/Cráneo Fuego left 3.png')]


    #Gives Cráneo Fuego object with properties like location, size, walking path, hitbox, speed, visibility, and health
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x , self.y, 100, 100)
        self.health = 10
        self.visible = True


    #Makes Cráneo Fuego move to its end point and back to its starting point
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0


    #Decreases Cráneo Fuego's health when hit by Poñyu's slime ball and activates noise when health is zero
    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            cráneo_fuego_defeated_sound .play()
            self.visible = False
        print("hit")


    #Animates Cráneo Fuego walking left and right
    def draw(self,window):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 18:
                self.walkCount = 0
            if self.vel > 0:
                window.blit(self.walkRight[self.walkCount//6], (self.x, self.y))
                self.walkCount += 1
            else:
                window.blit(self.walkLeft[self.walkCount//6], (self.x, self.y))
                self.walkCount += 1
            #Drawing its hidden hitbox
            pygame.draw.rect(window,(255,0,0),(self.hitbox[0],self.hitbox[1]-20, 50, 10))
            pygame.draw.rect(window,(0,169,0),(self.hitbox[0],self.hitbox[1]- 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 30, self.y + 20, 40, 50)



class Button:
    #Gives a button object properties like color, location, size, and text
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text


    #Draws an ellipse button
    def draw(self, window, outline = None):
        if outline:
            pygame.draw.ellipse(window, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        pygame.draw.ellipse(window, self.color, (self.x, self.y, self.width, self.height), 0)
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            window.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))


    #Takes note of mouse's position hovering over the button
    def isOver(self, mousePosition):
        if mousePosition[0] > self.x and mousePosition[0] < self.x + self.width:
            if mousePosition[1] > self.y and mousePosition[1] < self.y + self.height:
                return True
        return False



#Updates all sprites, text, and background on the game window
def redrawGameWindow():
    window.blit(bg, (0,0))
    ponyu.draw(window)
    cráneo_fuego.draw(window)
    cráneo_fuego_dos.draw(window)
    text = font.render("Cinnabon Delights: " + str(cinnabon_delights), 1, (255, 255, 0))
    window.blit(text,(0,10))
    for bullet in bullets:
        bullet.draw(window)
    pygame.display.update()




#mainloop
font = pygame.font.SysFont("comicsans", 30, True, True)
startButton = Button((50, 206, 245), canvas_width/3, canvas_height/2, 250, 100, 'START')
ponyu = Player(0, 600, 100, 100)
cráneo_fuego = Enemy(100, 610, 80, 80, 700)
cráneo_fuego_dos = Enemy(100, 560, 80, 80, 500)
shootloop = 0
run = True
start = True
bullets = []
cinnabon_delights = 0


#All game code is executed here while the game is running
while run:

    clock.tick(30)
    #Allows player to exit the game by clicking on the window's red X
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    #Displays the title screen with a start button
    while start:
        window.fill((255, 255, 255))
        startButton.draw(window, (0, 0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            mousePosition = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            #Changes title screen to game level
            if event.type == pygame.MOUSEBUTTONDOWN:
                if startButton.isOver(mousePosition):
                    print('clicked button')
                    start = False
            #Darkens the color of the button when the mouse hovers over the start button
            if event.type == pygame.MOUSEMOTION:
                if startButton.isOver(mousePosition):
                    startButton.color = (41, 126, 191)
            else:
                startButton.color = (33, 150, 243)


    #Deducts Cinnabon Delights (points) if Poñyu's hitbox touches an enemy's hitbox
    if cráneo_fuego.visible == True:
        if ponyu.hitbox[1] < cráneo_fuego.hitbox[1] + cráneo_fuego.hitbox[3] and ponyu.hitbox[1] + ponyu.hitbox[3] > cráneo_fuego.hitbox[1]:
                if ponyu.hitbox[0] + ponyu.hitbox[2] > cráneo_fuego.hitbox[0] and ponyu.hitbox[0] < cráneo_fuego.hitbox[0] + cráneo_fuego.hitbox[2]:
                    ponyu.hit()
                    cinnabon_delights -= 5


    #Deducts Cinnabon Delights (points) if Poñyu's hitbox touches the second enemy's hitbox
    if cráneo_fuego_dos.visible == True:
        if ponyu.hitbox[1] < cráneo_fuego_dos.hitbox[1] + cráneo_fuego_dos.hitbox[3] and ponyu.hitbox[1] + ponyu.hitbox[3] > cráneo_fuego_dos.hitbox[1]:
                if ponyu.hitbox[0] + ponyu.hitbox[2] > cráneo_fuego_dos.hitbox[0] and ponyu.hitbox[0] < cráneo_fuego_dos.hitbox[0] + cráneo_fuego_dos.hitbox[2]:
                    ponyu.hit()
                    cinnabon_delights -= 5


    #Limits the number of slimeballs Poñyu can shoot to three
    if shootloop > 0:
        shootloop += 1
    if shootloop > 3:
        shootloop = 0


    #Activates hit sound and adds point if a slimeball projectile hits an enemy's hitbox
    for bullet in bullets:
        if bullet.y - 40 < cráneo_fuego.hitbox[1] + cráneo_fuego.hitbox[3] and bullet.y + 40 > cráneo_fuego.hitbox[1] and cráneo_fuego.visible == True :
            if bullet.x + 40 > cráneo_fuego.hitbox[0] and bullet.x +10 < cráneo_fuego.hitbox[0] + cráneo_fuego.hitbox[2]:
                cráneo_fuego_hit_sound.play()
                cráneo_fuego.hit()
                cinnabon_delights += 1
                bullets.pop(bullets.index(bullet))
        #Limits slimeball's projectile range
        if bullet.x < canvas_width and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))


    #Activates hit sound and adds point if a slimeball projectile hits the second enemy's hitbox
    for bullet in bullets:
        if bullet.y - 40 < cráneo_fuego_dos.hitbox[1] + cráneo_fuego_dos.hitbox[3] and bullet.y + 40 > cráneo_fuego_dos.hitbox[1] and cráneo_fuego_dos.visible == True:
            if bullet.x + 40 > cráneo_fuego_dos.hitbox[0] and bullet.x +10 < cráneo_fuego_dos.hitbox[0] + cráneo_fuego_dos.hitbox[2]:
                cráneo_fuego_hit_sound.play()
                cráneo_fuego_dos.hit()
                cinnabon_delights += 1
                bullets.pop(bullets.index(bullet))
        #Limits slimeball's projectile range
        if bullet.x < canvas_width and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    #Allows only a portion of the screen to updated, instead of the entire area
    pygame.display.flip()

    #Arrow keys are assigned to Poñyu's movements (walking, jumping, and shooting)
    keys = pygame.key.get_pressed()
    #ARROW KEYS
    if keys[pygame.K_LEFT] and ponyu.x > ponyu.vel:
        ponyu.x -= ponyu.vel
        ponyu.left = True
        ponyu.right = False
        ponyu.standing = False
    elif keys[pygame.K_RIGHT] and ponyu.x < canvas_width - ponyu.width - ponyu.vel:
        ponyu.x += ponyu.vel
        ponyu.left = False
        ponyu.right = True
        ponyu.standing = False
    else:
        ponyu.standing = True
        ponyu.walkCount = 0
    #Fixes bug by putting Poñyu down to the groundfloor if placed above the enemy after getting hit
    if keys[pygame.K_DOWN]:
        ponyu.y = 600


    #SPACEBAR
    if keys[pygame.K_SPACE] and shootloop == 0:
        slime_attack_sound.play()
        if ponyu.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 3:
            bullets.append(Projectile(round(ponyu.x), round(ponyu.y),facing))
        shootloop = 1
    #Establishes how high Poñyu can jump
    if not(ponyu.isJump):
        if keys[pygame.K_UP]:
            ponyu.isJump = True
            ponyu.walkCount = 0
    else:
        if ponyu.jumpCount >= -10:
            neg = 1
            if ponyu.jumpCount < 0:
                neg = -1
            ponyu.y -= (ponyu.jumpCount ** 2) * 0.5 * neg
            ponyu.jumpCount -=1
        else:
            ponyu.isJump = False
            ponyu.jumpCount = 10


    #Once Poñyu scores 250 Cinnabon Delights (hits enemy 250x), the player is awarded to end screen
    if cinnabon_delights <= 250:
        if cráneo_fuego.visible == False and cráneo_fuego_dos.visible == False:
            cráneo_fuego.y = random.randint(500,600)
            cráneo_fuego.vel += 1
            cráneo_fuego.health = 5
            cráneo_fuego_dos.y =random.randint(450,550)
            cráneo_fuego_dos.vel += 1
            cráneo_fuego_dos.health = 5
            cráneo_fuego.visible = True
            cráneo_fuego_dos.visible = True
    elif cinnabon_delights > 250:
        cráneo_fuego.visible = False
        cráneo_fuego_dos.visable = False
        bg = pygame.image.load('win.jpg')
        window.blit(bg, (0,0))

    #Calls the function to update the graphics (sprites, background, etc.)
    redrawGameWindow()

