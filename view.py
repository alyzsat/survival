import pygame
import animal_attributes as aa
from mechanics import Animal
import random

START_SCREEN = 0
BUILD_SCREEN = 1
GAME_SCREEN = 2
WIN_SCREEN = 3
LOSE_SCREEN = 4

ATTRIBUTES = [aa.SKIN, aa.DIET, aa.MOVE, aa.BREATH]
ANAMES = ["Skin", "Diet", "Movement", "Breathing"]

white = (255,255,255)

class SurvivalGame:

    def __init__(self):
        pygame.display.set_caption("Survival of the Fittest")
        self._running = True
        self._mode = START_SCREEN
        self._feature = 0
        self._next_game_screen = False
        self._environments = aa.ENVIRONMENTS[:4]
        random.shuffle (self._environments)
        self._environment = 0 #"desert" #Does this need to be changed later?
        self._animal = Animal(None, None, None, None) #Kill the game if user does not select all the animal attributes
        

    def run(self):
        pygame.init()
        pygame.display.set_mode((800, 800))
        while self._running:
            if self._mode == START_SCREEN:
                self._draw_start_screen()
                
            elif self._mode == BUILD_SCREEN:
                surface = pygame.display.get_surface()
                surface.fill((0,0,0))
                self._draw_build_screen()
                
            elif self._mode == GAME_SCREEN:
                self._draw_game_screen()
                   
            elif self._mode == LOSE_SCREEN:
                self._game_over()
                
            elif self._mode == WIN_SCREEN:
                self._draw_win_screen()
                
            else:
                # If something goes wrong and we bring up a screen that we don't have,
                # display this
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
                
                
    def _draw_game_screen(self):
        self._draw_environment()
        surface = pygame.display.get_surface()
        
        attributes = [self._animal.skin, self._animal.move, self._animal.breath, self._animal.diet]
        
        for att in attributes:
            if att == None:
                self._animal.kill()
        
        font = pygame.font.Font(None, 70)
        next_text = font.render("Next", True, white)
        pygame.draw.rect(surface, pygame.color.Color("#60cadb"), (400,650,400,100))
        surface.blit(next_text, (400,650))

        enviro = self._environments[self._environment]
        if not self._animal.is_alive():
            self._mode = LOSE_SCREEN
        
        if self._next_game_screen and self._animal.is_alive():
            if self._environment <= len(self._environments) - 2:
                self._environment += 1
                self._animal.will_survive(enviro)
            elif self._environment == len(self._environments) - 1:
                self._animal.will_survive(enviro)
                self._mode = WIN_SCREEN
            self._next_game_screen = False
            

    def _game_loop(self):
        for e in aa.ENVIRONMENTS:
            self._environment = "desert" #e 
            self._draw_environment()
            self._animal.will_survive(e)
            self._draw_hp_bar(self._animal.hp)
            if not self._animal.is_alive():
                self._mode = LOSE_SCREEN
                break
        if self._mode != LOSE_SCREEN:
            self._mode = WIN_SCREEN
                
                
    def _game_over(self):
        pygame.display.set_mode((800, 800))
        surface = pygame.display.get_surface()

        font = pygame.font.Font(None, 100)
        gameOver = font.render("Game Over :(", True, white)
        surface.blit(gameOver, (200,400))
    
    
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
        
        font = pygame.font.Font(None, 50)
        # Left button
        if self._feature != 0:
            prev = font.render("Prev", True, white)
            surface.blit(prev, (85,70))
            pygame.draw.polygon(surface, white, [(100,130), (140,110), (140,150)])
            
        # Right button
        if self._feature != 3:
            next = font.render("Next", True, white)
            surface.blit(next, (645,70))
            pygame.draw.polygon(surface, white, [(700,130), (660,110), (660,150)])
            
        x_pos = 200
        y_pos = 100
        font = pygame.font.Font(None, 70)
        for ft in ATTRIBUTES[self._feature].keys():
            y_pos += 85
            
            if self._animal.breath == ft \
            or self._animal.diet == ft \
            or self._animal.skin == ft \
            or self._animal.move == ft:
                color = "#5392d6"
            else:
                color = "#60dbec"
                
            pygame.draw.rect(surface,  pygame.color.Color(color), (x_pos,y_pos,400,65))
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
                
            y_pos = 100
            for ft in ATTRIBUTES[self._feature].keys():
                y_pos += 85
                if cursor_x >= 200 and cursor_x <= 600 \
                and cursor_y >= y_pos and cursor_y <= y_pos + 65:
                    self._change_feature(ft)
        
        # 400,650,400,100
        elif self._mode == GAME_SCREEN:
            if self._feature != 0 and \
            cursor_x >= 400 and cursor_x <= 800 \
            and cursor_y >= 650 and cursor_y <= 750:
                self._next_game_screen = True
            
                    
                    
    def _draw_win_screen(self):
        surface = pygame.display.get_surface()
        surface.fill((0,0,0))
        
        self._draw_hp_bar()
        
        font = pygame.font.Font(None,90)
        text1 = font.render("You have survived!", True, white)
        text2 = font.render("Your animal is superior!", True, white)
        text3 = font.render("Your score is", True, white)
        
        font = pygame.font.Font(None,150)
        text4 = font.render(str(self._animal.hp), True, white)
        
        surface.blit(text1, (400-text1.get_width()/2,200))
        surface.blit(text2, (400-text2.get_width()/2,300))
        surface.blit(text3, (400-text3.get_width()/2,400))
        surface.blit(text4, (400-text4.get_width()/2,500))
        
                     
                    
    def _change_feature(self, feature: str):
        if self._feature == 0:
            self._animal.change_skin(feature)
        elif self._feature == 1:
            self._animal.change_diet(feature)
        elif self._feature == 2:
            self._animal.change_move(feature)
        else:
            self._animal.change_breath(feature)
        
        
    def _draw_hp_bar (self):
        surface = pygame.display.get_surface()
        
        surface = pygame.display.get_surface()
        pygame.draw.rect(surface, pygame.color.Color("#000000"), (145,45,510,50))
        
        colors = ["#890000", "#ad0000", "#db0000","#e57002", "#e5b002",
                  "#efe702", "#bbef02", "#88ef02", "#40e214", "#20c40d"]
        
        for i in range(len(colors)):
            if self._animal.hp >= (i + 1) * 10:
                pygame.draw.rect(surface, pygame.color.Color(colors[i]), (150+50*i,50,50,40))
                
        font = pygame.font.Font(None, 70)
        hp = font.render("HP", True, (0,0,0))
        surface.blit(hp, (360,0))
        
        
    def _draw_environment(self):
        screen = pygame.display.get_surface()
        img = pygame.image.load(f"{self._environments[self._environment]}.png")
        screen.blit(pygame.transform.scale(img, (800,800)), (0,0))
        self._draw_hp_bar()

    

SurvivalGame().run()
