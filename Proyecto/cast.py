import pygame
from math import * 
from OpenGL.GL import *




colors = [
  (0, 20, 10),
  (4, 91, 82),
  (219, 242, 38),
  (0, 0, 255),
  (255, 255, 255)
]
SKY = (50, 100, 200)
GROUND = (163, 152, 154)
TRANSPARENT = (152, 0, 136,255)
TRANSPARENT2 = (152, 0, 135,255)
TRANSPARENT3 = (151, 0, 136,255)

walls = {
    "1": pygame.image.load('./Proyecto/p4n.png'),
    "2": pygame.image.load('./Proyecto/p4n.png'),
    "3": pygame.image.load('./Proyecto/p3n.png'),
    "4": pygame.image.load('./Proyecto/p2N.png'),
    "5": pygame.image.load('./Proyecto/p1N.png'),
}
sprite1 = pygame.image.load('./Proyecto/espadasN.png')
sprite2 = pygame.image.load('./Proyecto/espada2N.png')


enemies = [
    {
        "x": 125,
        "y": 125,
        "sprite": sprite2,
        "Distance": False,
        "Taked": False,

    },
    {
         "x": 300,
         "y": 300,
         "sprite": sprite1,
         "Distance": False,
         "Taked": False,
     },
     {
         "x": 400,
         "y": 420,
         "sprite": sprite1,
         "Distance": False,
         "Taked": False,
     },
     {
         "x": 350,
         "y": 80,
         "sprite": sprite2,
         "Distance": False,
         "Taked": False,
     },
     

    
]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Raycaster(object):
    def __init__ (self, screen):
        self.screen = screen
        x, y, self.width, self.height = screen.get_rect()
        self.blocksize = 50
        self.map = []
        self.player = {
            "x": int(self.blocksize + self.blocksize / 2),
            "y": int(self.blocksize + self.blocksize / 2),
            "fov": int(pi/3),
            "a": int(pi/3),
        }
        self.llaves = 0
        self.gameOver = False
        self.clear_z()
        
    
    def clear_z(self):
        self.zbuffer = [99999 for z in range (0,int(self.width/2))]


    def point(self, x, y, c = WHITE):
        self.screen.set_at((x, y), c)

    def block(self, x, y, wall):
        for i in range(x, x + self.blocksize):
            for j in range(y, y + self.blocksize):
                tx = int((i - x) * 128 / self.blocksize)
                ty = int((j - y) * 128 / self.blocksize)
                c = wall.get_at((tx, ty))
                self.point(i, j, c)

    def load_map(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))
    
    def draw_map(self):
        for x in range(0, 500, self.blocksize):
            for y in range(0, 500, self.blocksize):
                i = int(x/self.blocksize)
                j = int(y/self.blocksize)
                if self.map[j][i] != ' ':
                    self.block(x, y, walls[self.map[j][i]])

    def draw_player(self):
        self.point(self.player["x"], self.player["y"])

    def render(self):
        self.draw_map()
        self.draw_player()
        density = 60
        for i in range(0, density):
            a = self.player["a"] - self.player["fov"] / 2 + self.player["fov"]*i/density
            d, c, tx = self.cast_ray(a)
        for i in range(0, 500):
            self.point(499, i)
            self.point(500, i)
            self.point(501, i)
        for i in range(0, int(self.width/2)):
            a = self.player["a"] - self.player["fov"] / 2 + self.player["fov"]*i/(self.width/2)
            d, c, tx = self.cast_ray(a)
            x = int(self.width/2) + i
            var = (d * cos(a - self.player["a"]))
            if var == 0:
                self.gameOver = True
                self.player['x'] = int(self.blocksize + self.blocksize / 2)
                self.player['y'] = int(self.blocksize + self.blocksize / 2)
            else:
                h = (self.height/(d * cos(a - self.player["a"]))) * self.height/10
                if self.zbuffer[i]  >= d:
                    self.draw_stake(x, h, c, tx)
                    self.zbuffer[i] = d


            
        for enemy in enemies:
            if enemy["Taked"] == False:
                    self.point(int(enemy["x"]), int(enemy["y"]),(255,0,0))
            else:
                pass
        
        for enemy in enemies:
                if enemy["Taked"] == False:
                    self.draw_sprite(enemy)
                else:
                    pass
    

    def draw_sprite(self,sprite):
        sprite_a = atan2(
            sprite["y"] - self.player["y"],
            sprite["x"] - self.player["x"],
        )
        
        #Distancia de la espada al jugador
        d = ((self.player["x"] - sprite["x"])**2 + (self.player["y"] - sprite["y"])**2)**0.5

        #Distancia de la espada al jugador
        if d < 65:
            self.change_sword(sprite)

        
        sprit_size = int((500/d) * (500/10))

        sprite_x = int(
            500 + 
            (sprite_a - self.player["a"]) * 500/self.player["fov"] + sprit_size/2)
        
        sprite_y = int(500/2 - sprit_size/2)


        for x in range(sprite_x, sprite_x + sprit_size):
            for y in range(sprite_y, sprite_y + sprit_size):
                tx = int((x - sprite_x) * 128/sprit_size)  
                ty = int((y - sprite_y) * 128/sprit_size)  
                c = sprite["sprite"].get_at((tx,ty))

                if c != TRANSPARENT and c != TRANSPARENT2:
                    if (x > int(self.width/2) and x < self.width):
                        if self.zbuffer[x - 500] >= d:
                            self.point(x,y,c)
                            self.zbuffer[x - 500] = d
            


    def cast_ray(self, a):
        d = 0
        ox = self.player["x"]
        oy = self.player["y"]

        while True:
            x = int(ox + d*cos(a))
            y = int(oy + d*sin(a))

            i = int(x/self.blocksize)
            j = int(y/self.blocksize)

            if self.map[j][i] != ' ':
                hitx = x - i * self.blocksize
                hity = y - j * self.blocksize
                
                if 1 < hitx < self.blocksize-1:
                    maxhit = hitx
                else:
                    maxhit = hity

                tx = int(maxhit * 128 / self.blocksize)

                return d, self.map[j][i], tx
            
            self.point(x, y)


            d += 1
    
    def change_sword(self, sprite):
        sprite["Distance"] = True

    def draw_stake(self, x, h, c, tx):
        start_y = int(self.height/2 - h/2)
        end_y = int(self.height/2 + h/2)
        height = end_y - start_y

        for y in range(start_y, end_y):
            ty = int((y - start_y) * 128 / height)
            color = walls[c].get_at((tx, ty))
            self.point(x, y, color)

        
    def draw_image(self, imagen):
        for x in range(0,r.width):
            for y in range(0,r.height):
                r.point(x,y,imagen.get_at((x,y)))
    
    def get_sword(self):
        for enemy in enemies:
            if enemy["Taked"] == False and enemy['Distance'] == True:
                enemy["Taked"] = True
                self.llaves += 1
    def get_num_espadas(self):
        return self.llaves
    def update_fps(self, clock, font):
        fps = str(int(clock.get_fps()))
        fps_text = font.render(fps, 1, pygame.Color("coral"))
        return fps_text




pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('./Proyecto/got.mp3')
pygame.mixer.music.set_volume(0.2)
sword_sound = pygame.mixer.Sound('./Proyecto/SwordH.mp3')
steps = pygame.mixer.Sound('./Proyecto/Steps2.mp3')


screen = pygame.display.set_mode((1000, 500))
r = Raycaster(screen)

pygame.mixer.music.play()

imgload_page = pygame.image.load('./Proyecto/Cg.png')
img_selectlevel = pygame.image.load('./Proyecto/lvl.png')
img_victoria = pygame.image.load('./Proyecto/Finalg.png')
img_derrota = pygame.image.load('./Proyecto/derrota2.png')
img_controles = pygame.image.load('./Proyecto/controles.png')

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 25)

select_level = False
controls_page = False
load_page = True


while load_page:
    r.draw_image(imgload_page)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                load_page = False
                select_level = True
            if event.key == pygame.K_r:
                load_page = False
                controls_page = True
while controls_page:
    r.draw_image(img_controles)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                controls_page = False
                select_level = True

while select_level:
    r.draw_image(img_selectlevel)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                load_page = False
                select_level = False
                r.load_map('./Proyecto/map.txt')
            if event.key == pygame.K_h:
                load_page = False
                select_level = False
                r.load_map('./Proyecto/map2.txt')


victoria = False
running = True
Fallo = False
while running:
    r.clear_z()
    screen.fill(BLACK, (0, 0, r.width/2, r.height))
    screen.fill(SKY, (r.width/2, 0, r.width, r.height/2))
    screen.fill(GROUND, (r.width/2, r.height/2, r.width, r.height/2))

    r.render()
    r.screen.blit(r.update_fps(clock,font),(510,0))
    clock.tick(60)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                pygame.mixer.Sound.play(steps)
                r.player["x"] += 10
                if r.gameOver == True:
                    running = False
                    Fallo = True

            if event.key == pygame.K_LEFT:
                pygame.mixer.Sound.play(steps)
                r.player["x"] -= 10
                if r.gameOver == True:
                    running = False
                    Fallo = True

            if event.key == pygame.K_UP:
                pygame.mixer.Sound.play(steps)
                r.player["y"] -= 10
                if r.gameOver == True:
                    running = False
                    Fallo = True

            if event.key == pygame.K_DOWN:
                pygame.mixer.Sound.play(steps)
                r.player["y"] += 10
                if r.gameOver == True:
                    running = False
                    Fallo = True
            
            if event.key ==pygame.K_p:
                pygame.mixer.music.pause()
            if event.key == pygame.K_r:
                pygame.mixer.music.unpause()

            if event.key == pygame.K_a:
                r.player["a"] += pi/10
            if event.key == pygame.K_d:
                r.player["a"] -= pi/10
            if event.key == pygame.K_SPACE:
                pygame.mixer.Sound.play(sword_sound)
                r.get_sword()
                llaves = r.get_num_espadas()
                if llaves == 4:
                    running = False
                    victoria = True

while victoria:
    r.draw_image(img_victoria)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                load_page = False
                select_level = True
while Fallo:
    r.draw_image(img_derrota)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                load_page = False
                select_level = True



            
