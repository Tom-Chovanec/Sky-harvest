import pygame
import random

pygame.init()
pygame.font.init()

icon = pygame.transform.scale(pygame.image.load("assets/playerdefault.png"), (32, 32))
pygame.display.set_caption("SKY harvest")
pygame.display.set_icon(icon)

scenes = {
   "MAIN_MENU": 1,
   "GAME":      2,
}

screenWidth = 1200
screenHeight = 800
score = 0
fHighscore = open("highscore.txt")
highScore = fHighscore.read()
fHighscore.close()
scene = scenes["MAIN_MENU"]
health = 3
maxObjects = 5
running = True
objects = []

screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
scoreFont = pygame.font.SysFont("Montsserat Thin Bold", 100)
mainFont = pygame.font.SysFont("Montsserat Regular", 150)

mainMenuBackgroundSprite = pygame.image.load("assets/mainmenu.png")
gamebackgroundSprite = pygame.transform.scale(pygame.image.load("assets/background.jpg"), (screenWidth, screenHeight))
heartSprite = pygame.image.load("assets/heart.png")



class Player():
  sprites = [pygame.image.load("assets/playerdefault.png"), pygame.image.load("assets/playerleft.png"), pygame.image.load("assets/playerright.png")]
  sprite = sprites[0]
  width = sprite.get_width()
  height = sprite.get_height()
  speed = 3
  acceleration = 0
  topSpeed = 10
  friction = 0.5
  X = 0
  Y = screenHeight-width

  def render():
    if Player.acceleration == 0 :
      Player.sprite = Player.sprites[0]
    elif Player.acceleration < 0 :
      Player.sprite = Player.sprites[1]
    elif Player.acceleration > 0 :
      Player.sprite = Player.sprites[2]
    screen.blit(Player.sprite, (Player.X, Player.Y))

  def move():
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
      Player.acceleration -= (Player.speed - Player.friction)
    if keys[pygame.K_d] or keys [pygame.K_RIGHT]:
      Player.acceleration += (Player.speed - Player.friction)

    if Player.acceleration > Player.topSpeed:
      Player.acceleration = Player.topSpeed
    if Player.acceleration < -Player.topSpeed:
      Player.acceleration = -Player.topSpeed

    Player.X += Player.acceleration

    if Player.X < 0:
      Player.X = 0
    if Player.X > screenWidth-Player.width:
      Player.X = screenWidth-Player.width  

    if Player.acceleration < 0:
      Player.acceleration += Player.friction
    if Player.acceleration > 0:
      Player.acceleration -= Player.friction

class Object():
  def __init__(self, id):
        self.id = id
        self.sprites = [pygame.image.load("assets/apple.png"),pygame.image.load("assets/banana.png"),pygame.image.load("assets/coconut.png"), pygame.image.load("assets/grape.png")]
        self.sprite = random.choice(self.sprites)
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()
        self.X = random.randint(0, screenWidth - self.width)
        self.Y = -random.randint(500, 1500)
        self.rect = self.sprite.get_rect()
        self.speed = 3

  def render(self):
      screen.blit(self.sprite, (self.X, self.Y))
  def move(self):
      self.Y += self.speed
      

  def collision(self):
      global score, health
      if self.X < player.X + player.width and player.X < self.X + self.width and self.Y + self.height > screenHeight - player.width:
          self.Y = 0 -random.randint(500, 800)
          self.X = random.randint(0, screenWidth - self.width)
          self.sprite = random.choice(self.sprites)
          score += 1
      if self.Y > screenHeight:
        health -= 1
        self.Y = 0 -random.randint(500, 800)
        self.X = random.randint(0, screenWidth - self.width)
        self.sprite = random.choice(self.sprites)

def highscore():
  global highScore, score
  if score > int(highScore):
    fHighscore = open("highscore.txt", "w")
    fHighscore.write(str(score))
    fHighscore = open("highscore.txt")
    highScore = fHighscore.read()
    fHighscore.close()


player = Player

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  if scene == scenes["MAIN_MENU"]:
    screen.blit(mainMenuBackgroundSprite, (0,0))
    if screenWidth/2-750/2 < pygame.mouse.get_pos()[0] < screenWidth/2+750/2 and pygame.mouse.get_pressed()[0] and 450 < pygame.mouse.get_pos()[1] < 550:
      scene = scenes["GAME"]
    if 225 < pygame.mouse.get_pos()[0] < 975 and pygame.mouse.get_pressed()[0] and 600 < pygame.mouse.get_pos()[1] < 700:
      running = False
     

  if scene == scenes["GAME"]:
    n = score//10 + 1
    while len(objects) < n < maxObjects +1:
       objects.append(Object(n))

    highscore()

    player.move()
    screen.fill("blue")
    for object in objects:
       object.collision()
       object.move()

    screen.blit(gamebackgroundSprite, (0,0))

    for object in objects:
       object.render()

    player.render() 
    if health == 0:
      scene = scenes["MAIN_MENU"]
      health = 3
      score = 0
      objects = []
    
    for i in range(1, health + 1):
       screen.blit(heartSprite, (screenWidth - i * 100, 20))
    text = scoreFont.render(str(score), True, (0, 0, 0))
    highScoretext = scoreFont.render(f"High: {str(highScore)}", True, (0, 0, 0))
    screen.blit(text, (screenWidth/2-text.get_width()/2, 20))
    screen.blit(highScoretext, (20, 20))

  pygame.display.flip()
  clock.tick(120)

pygame.quit()