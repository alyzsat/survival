import pygame
import animal_attributes as aa
from mechanics import Animal
import random

START_SCREEN = 0
BUILD_SCREEN = 1
GAME_SCREEN = 2
LOSE_SCREEN = 3
WIN_SCREEN = 4

ATTRIBUTES = [aa.SKIN, aa.DIET, aa.MOVE, aa.BREATH]
ANAMES = ["Skin", "Diet", "Movement", "Breathing"]

white = (255,255,255)

class SurvivalGame:

    def __init__(self):
        pygame.display.set_caption("Survival of the Fittest")
        self._running = True
        self._mode = START_SCREEN
        self._feature = 0
        self._environment = None #"desert" #Does this need to be changed later?
        self._animal = Animal(None, None, None, None) #Kill the game if user does not select all the animal attributes
        random.shuffle (aa.ENVIRONMENTS)

    def run(self):
        pygame.init()
        pygame.display.set_mode((800, 800))
        
       # aa.ENVIRONMENTS.append("space")
        while self._running:
            if self._mode == START_SCREEN:
                self._draw_start_screen()
                
            elif self._mode == BUILD_SCREEN:
                surface = pygame.display.get_surface()
                surface.fill((0,0,0))
                self._draw_build_screen()
                
            elif self._mode == GAME_SCREEN:
                self._game_loop()
                
                        
            elif self._mode == LOSE_SCREEN:
                print("game over in the run")
                self._game_over()
                #something goes here
                pass
                
            else:
                surface = pygame.display.get_surface()
                surface.fill(white)

            self._handle_events()
            pygame.display.flip()

        pygame.quit()
        
        
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_click()

    def _game_loop(self):
        for e in aa.ENVIRONMENTS:
            self._environment = "desert" #e 
            print(self._animal.is_alive(), self._animal.hp)    
            if self._animal.is_alive():
                print('in the if')
                self._draw_environment()
                print(e, self._animal.hp)
                self._animal.will_survive(e)
                self._draw_hp_bar(self._animal.hp)
            else:
                print("end the screen")
                self._mode = LOSE_SCREEN
                break
        if self._mode != LOSE_SCREEN:
            self._mode = WIN_SCREEN
                
    def _game_over(self):
        pygame.display.set_mode((800, 800))
        surface = pygame.display.get_surface()

        font = pygame.font.Font(None, 100)
        gameOver = font.render("Game Over", True, white)
        # Draws the start button
      #  pygame.draw.rect(surface, pygame.color.Color("#60cadb"), (200,500,400,100))

    #    surface.blit(gameOver, (320,520) 
    
    
    
    def _draw_start_screen(self):
        surface = pygame.display.get_surface()

        font = pygame.font.Font(None, 100)
        start_text = font.render("Start", True, white)
        # Draws the start button
        pygame.draw.rect(surface, pygame.color.Color("#60cadb"), (200,500,400,100))

        surface.blit(start_text, (320,520))

        font = pygame.font.Font(None, 180)
        title1 = font.render("Survival", True, white)
        title2 = font.render("of the", True, white)
        title3 = font.render("Fittest", True, white)

        surface.blit(title1, (150,100))
        surface.blit(title2, (230,220))
        surface.blit(title3, (200,340))
        
        
    def _draw_build_screen(self):
        surface = pygame.display.get_surface()
        font = pygame.font.Font(None, 100)
        
        title = font.render(ANAMES[self._feature], True, white)
        surface.blit(title, (400-title.get_width()/2,100))
        
        # Left button
        pygame.draw.polygon(surface, white, [(100,130), (140,110), (140,150)])
        # Right button
        pygame.draw.polygon(surface, white, [(700,130), (660,110), (660,150)])
        x_pos = 200
        y_pos = 100
        
        for ft in ATTRIBUTES[self._feature].keys():
            font = pygame.font.Font(None, 70)
            y_pos += 85
            pygame.draw.rect(surface,  pygame.color.Color("#60cadb"), (x_pos,y_pos,400,65))
            text = font.render(ft.capitalize(), True, white)
            surface.blit(text,(400-text.get_width()/2,y_pos+10))
        
        done = font.render("Done", True, white)
        pygame.draw.rect(surface, pygame.color.Color("#DD2222"), (250,700,300,60) )
        surface.blit(done, (400-done.get_width()/2,705))


    def _handle_click(self):
        cursor_x, cursor_y = pygame.mouse.get_pos()
        
        if self._mode == START_SCREEN:
            if cursor_x >= 200 and cursor_x <= 600 \
            and cursor_y >= 500 and cursor_y <= 600:
                self._mode = BUILD_SCREEN
                
        elif self._mode == BUILD_SCREEN:
            # left button
            if self._feature != 0 and \
            cursor_x >= 100 and cursor_x <= 140 \
            and cursor_y >= 110 and cursor_y <= 150:
                self._feature -= 1
                
            # right button
            elif self._feature != 3 and \
            cursor_x >= 660 and cursor_x <= 700 \
            and cursor_y >= 110 and cursor_y <= 150:
                self._feature += 1
                
            elif cursor_x >= 250 and cursor_x <= 550 \
            and cursor_y >= 700 and cursor_y <= 760:
                self._mode = GAME_SCREEN
               # print("WORKED")
                
            y_pos = 100
            for ft in ATTRIBUTES[self._feature].keys():
                y_pos += 85
                if cursor_x >= 200 and cursor_x <= 600 \
                and cursor_y >= y_pos and cursor_y <= y_pos + 65:
                    self._change_feature(ft)
                
                    
                    
    def _change_feature(self, feature: str):
        if self._feature == 0:
            self._animal.change_skin(feature)
        elif self._feature == 1:
            self._animal.change_diet(feature)
        elif self._feature == 2:
            self._animal.change_move(feature)
        else:
            self._animal.change_breath(feature)
        
        
    def _draw_hp_bar (self, hp):
        surface = pygame.display.get_surface()
        if hp>=10:
            pygame.draw.rect(surface, pygame.color.Color("#890000"), (15,15,50,40))
        if hp>=20:
            pygame.draw.rect(surface, pygame.color.Color("#ad0000"), (65,15,50,40))
        if hp>=30:
            pygame.draw.rect(surface, pygame.color.Color("#db0000"), (115,15,50,40))
        if hp>=40:
            pygame.draw.rect(surface, pygame.color.Color("#e57002"), (165,15,50,40))
        if hp>=50:
            pygame.draw.rect(surface, pygame.color.Color("#e5b002"), (215,15,50,40))
        if hp>=60:
            pygame.draw.rect(surface, pygame.color.Color("#efe702"), (265,15,50,40))
        if hp>=70:
            pygame.draw.rect(surface, pygame.color.Color("#bbef02"), (315,15,50,40))
        if hp>=80:
            pygame.draw.rect(surface, pygame.color.Color("#88ef02"), (365,15,50,40))
        if hp>=90:
            pygame.draw.rect(surface, pygame.color.Color("#40e214"), (415,15,50,40))
        if hp>=100:
            pygame.draw.rect(surface, pygame.color.Color("#20c40d"), (465,15,50,40))
        
        
    def _draw_environment(self):
        screen = pygame.display.get_surface()
      #  screen.fill(white)
        
        img = pygame.image.load(f"{self._environment}.png")
        screen.blit(pygame.transform.scale(img, (800,800)), (0,0))
        
        surface = pygame.display.get_surface()
        pygame.draw.rect(surface, pygame.color.Color("#000000"), (15,15,500,40))
     #   pygame.draw.rect(surface, pygame.color.Color(white), Rect, width=0)
            
   #     self._draw_hp_bar(self._animal.hp)
    

SurvivalGame().run()
