import pygame
import random
pygame.init()

#GAME WINDOW
canvas_width = 800
canvas_height = 800
window = pygame.display.set_mode((canvas_height, canvas_width))
pygame.display.set_caption("Poñyu GAME♥")
bg = pygame.image.load('bg.png')
bg_x = 0
bg_x2 = bg.get_width()

clock = pygame.time.Clock()

#MUSIC
bg_music = pygame.mixer.music.load('Music/8bit_Jojo.mp3')
pygame.mixer.music.play(-1)
slime_attack_sound = pygame.mixer.Sound('Music/slime_splash.wav')
cráneo_fuego_hit_sound = pygame.mixer.Sound('Music/hit.wav')
cráneo_fuego_defeated_sound = pygame.mixer.Sound('Music/hot_sizzling.wav')





class Player(object):
    #Indexes of Poñyu's sprites for walking
    char = pygame.image.load('Sprites/Ponyu Sprites/ponyu.png')
    walk_right = [pygame.image.load('Sprites/Ponyu Sprites/ponyu right 1.png'), pygame.image.load('Sprites/Ponyu Sprites/ponyu right 2.png'), pygame.image.load('Sprites/Ponyu Sprites/ponyu right 3.png')]
    walk_left = [pygame.image.load('Sprites/Ponyu Sprites/ponyu left 1.png'),pygame.image.load('Sprites/Ponyu Sprites/ponyu left 2.png'), pygame.image.load('Sprites/Ponyu Sprites/ponyu left 3.png')]

    #Gives the player/Poñyu object properties like location, size, hitbox, and actions (is it going left or right, jumping, standing still, etc.)
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 10
        self.is_jump = False
        self.jump_count = 10
        self.left = False
        self.right = False
        self.walk_count = 0
        self.idle = 0
        self.standing = True
        self.hitbox = (self.x + 25, self.y + 25, 75, 75)

    #Animates Poñyu walking left and right
    def draw(self, window):
        if self.walk_count + 1 >= 12:
            self.walk_count = 0
        if not(self.standing):
            if self.left:
                window.blit(self.walk_left[self.walk_count//4], (self.x,self.y))
                self.walk_count += 1
            elif self.right:
                window.blit(self.walk_right[self.walk_count//4], (self.x,self.y))
                self.walk_count += 1
        else:
            if self.right:
                window.blit(self.walk_right[0], (self.x, self.y))
            else:
                window.blit(self.walk_left[0], (self.x, self.y))
        #Draws its hidden hitbox
        self.hitbox = (self.x +25, self.y + 35, 50, 50)

    #Displays text when Poñyu gets hit by an enemy
    def hit(self):
        self.is_jump = False
        self.jump_count = 10
        self.x = 60
        self.y = 410
        self.walk_count = 0
        font_death = pygame.font.SysFont('Comic Sans MS', 50)
        text_death = font_death.render('YoU HaVe FaLleN SLiME', 1, (0, 0, 0))
        text_back = font_death.render('YoU HaVe FaLleN SLiME', 1, (225, 0, 0))
        window.blit(text_death, ((canvas_width / 2) - (text_death.get_width() / 2), (canvas_height / 2) - (text_death.get_height() / 2)))
        window.blit(text_back, ((canvas_width / 2) - (text_death.get_width() / 2), (canvas_height / 2) - 40))
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
    walk_right = [pygame.image.load('Sprites/Cráneo Fuego Sprites/Cráneo Fuego right 1.png'), pygame.image.load('Sprites/Cráneo Fuego Sprites/Cráneo Fuego right 2.png'), pygame.image.load('Sprites/Cráneo Fuego Sprites/Cráneo Fuego right 3.png')]
    walk_left = [pygame.image.load('Sprites/Cráneo Fuego Sprites/Cráneo Fuego left 1.png'),pygame.image.load('Sprites/Cráneo Fuego Sprites/Cráneo Fuego left 2.png'), pygame.image.load('Sprites/Cráneo Fuego Sprites/Cráneo Fuego left 3.png')]

    #Gives Cráneo Fuego object with properties like location, size, walking path, hitbox, speed, visibility, and health
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walk_count = 0
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
                self.walk_count = 0

    #Decreases Cráneo Fuego's health when hit by Poñyu's slime ball and activates noise when health is zero
    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            cráneo_fuego_defeated_sound .play()
            self.visible = False

    #Animates Cráneo Fuego walking left and right
    def draw(self,window):
        self.move()
        if self.visible:
            if self.walk_count + 1 >= 18:
                self.walk_count = 0
            if self.vel > 0:
                window.blit(self.walk_right[self.walk_count//6], (self.x, self.y))
                self.walk_count += 1
            else:
                window.blit(self.walk_left[self.walk_count//6], (self.x, self.y))
                self.walk_count += 1
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
            font_button = pygame.font.SysFont('Comic Sans MS', 40)
            text = font_button.render(self.text, 1, (0, 0, 0))
            window.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    #Takes note of mouse's position hovering over the button
    def isOver(self, mousePosition):
        if mousePosition[0] > self.x and mousePosition[0] < self.x + self.width:
            if mousePosition[1] > self.y and mousePosition[1] < self.y + self.height:
                return True
        return False



#This class's purpose is to only display pre-made speech bubbles to represent dialogue
class Dialogue(object):
    #Gives a Dialogue object properties like location and which image to display
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.visible = True

    #Displays the speech bubble image for a fixed amount of time and then hides it
    def appear(self):
        window.blit(self.image, (self.x, self.y))
        pygame.display.update()
        pygame.time.delay(3800)
        self.visible = False
        pygame.display.update()



#Updates all sprites, text, and background on the game window
def redrawGameWindow():
    window.blit(bg, (bg_x, 0))
    window.blit(bg, (bg_x2, 0))
    ponyu.draw(window)
    cráneo_fuego.draw(window)
    cráneo_fuego_dos.draw(window)
    cinnabon_delights_text = cinnabon_delights_font.render("Cinnabon Delights: " + str(cinnabon_delights), 1, (219, 144, 69))
    cinnabon_delights_text_back = cinnabon_delights_font.render("Cinnabon Delights: " + str(cinnabon_delights), 1, (255, 255, 255))
    window.blit(cinnabon_delights_text, (30, 40))
    window.blit(cinnabon_delights_text_back, (30, 43))
    for bullet in bullets:
        bullet.draw(window)
    pygame.display.update()


#Creates a fading effect on screen
def fade(width, height):
    fade = pygame.Surface((width, height))
    fade.fill((0, 0, 0))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        window.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(5)



#mainloop

run = True
start = True
shootloop = 0
cinnabon_delights = 0
bullets = []

#Initializing objects here
start_button = Button((50, 206, 245), canvas_width/3, canvas_height/2, 250, 100, 'START')
cinnabon_delights_font = pygame.font.SysFont('Comic Sans MS', 40, True, True)
ponyu = Player(0, 600, 100, 100)
cráneo_fuego = Enemy(100, 610, 80, 80, 700)
cráneo_fuego_dos = Enemy(100, 560, 80, 80, 500)


#Initializing speech bubbles here
boss_dialogue1 = pygame.image.load('Dialogue/dialogue1_boss_final.png')
boss_dialogue2 = pygame.image.load('Dialogue/dialogue2_boss_final.png')
boss_dialogue3 = pygame.image.load('Dialogue/dialogue3_boss_final.png')
show_boss_dialogue1 = Dialogue(540, 300, boss_dialogue1)
show_boss_dialogue2 = Dialogue(540, 300, boss_dialogue2)
show_boss_dialogue3 = Dialogue(540, 300, boss_dialogue3)

#Boss Sprite
boss_sprite = pygame.image.load('Sprites/Boss Sprites/Cinnabon Incinerator 1.png')



#All game code is executed here while the game is running
while run:
    #FPS
    clock.tick(34)

    #Allows player to exit the game by clicking on the window's red X
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    #Displays the title screen with a start button
    while start:
        window.fill((255, 255, 255))
        start_button.draw(window, (0, 0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            mousePosition = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            #Changes title screen to game level
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.isOver(mousePosition):
                    start = False
            #Darkens the color of the button when the mouse hovers over the start button
            if event.type == pygame.MOUSEMOTION:
                if start_button.isOver(mousePosition):
                    start_button.color = (41, 126, 191)
            else:
                start_button.color = (33, 150, 243)


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
        ponyu.walk_count = 0
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
    if not(ponyu.is_jump):
        if keys[pygame.K_UP]:
            ponyu.is_jump = True
            ponyu.walk_count = 0
    else:
        if ponyu.jump_count >= -10:
            neg = 1
            if ponyu.jump_count < 0:
                neg = -1
            ponyu.y -= (ponyu.jump_count ** 2) * 0.5 * neg
            ponyu.jump_count -=1
        else:
            ponyu.is_jump = False
            ponyu.jump_count = 10



    #Once Poñyu scores 200 Cinnabon Delights (hits enemy 200x), the player is awarded to end screen
    if cinnabon_delights < 20:
        continue_platform = True
        #Sidescrolling background
        bg_x -= 1.3
        bg_x2 -= 1.3
        if bg_x < bg.get_width() * -1:
            bg_x = bg.get_width()
        if bg_x2 < bg.get_width() * -1:
            bg_x2 = bg.get_width()

        #Respawns enemies
        if cráneo_fuego.visible == False and cráneo_fuego_dos.visible == False:
            cráneo_fuego.y = random.randint(500, 600)
            cráneo_fuego.vel += 2.5
            cráneo_fuego.health = 5
            cráneo_fuego_dos.y = random.randint(450, 550)
            cráneo_fuego_dos.vel += 2.5
            cráneo_fuego_dos.health = 5
            cráneo_fuego.visible = True
            cráneo_fuego_dos.visible = True

    #Calls the function to update the graphics (sprites, background, etc.)
    redrawGameWindow()


    #Once Poñyu collects enough Cinnabons, the background is static and the boss talks
    if cinnabon_delights >= 20:
        continue_platform = False
        cráneo_fuego.visible = False
        cráneo_fuego_dos.visible = False
        redrawGameWindow()
        pygame.time.delay(500)
        #Transitions to speech bubbles and game end
        if continue_platform == False:
            show_boss_dialogue1.appear()
            show_boss_dialogue2.appear()
            pygame.mixer.music.stop()
            fade(canvas_width, canvas_height)
            show_boss_dialogue3.appear()
            fade(canvas_width, canvas_height)
            window.fill((0, 0, 0))
            window.blit(boss_sprite, (canvas_width/3, canvas_height/3))
            pygame.display.update()
            pygame.time.delay(1000)
            fade(canvas_width, canvas_height)
            break


