import pygame
import animal_attributes as aa
from mechanics import Animal
from sentences import d as sentence_parts
import random

START_SCREEN = 0
BUILD_SCREEN = 1
GAME_SCREEN = 2
WIN_SCREEN = 3
LOSE_SCREEN = 4

ATTRIBUTES = [aa.SKIN, aa.DIET, aa.MOVE, aa.BREATH, aa.COLOR]
ANAMES = ["Skin", "Diet", "Movement", "Breathing", "Color"]

white = (255,255,255)
black = (0,0,0)

class SurvivalGame:

    def __init__(self):
        pygame.display.set_caption("Survival of the Fittest", 'backgrounds/default.png')
        pygame.display.set_icon(pygame.image.load('backgrounds/default.png'))
        self._running = True
        self._mode = START_SCREEN
        

    def run(self):
        pygame.init()
        pygame.display.set_mode((800, 800))
        while self._running:
            if self._mode == START_SCREEN:
                self._draw_start_screen()
                
            elif self._mode == BUILD_SCREEN:
                surface = pygame.display.get_surface()
                surface.fill(black)
                self._draw_build_screen()
                
            elif self._mode == GAME_SCREEN:
                self._draw_game_screen()
                   
            elif self._mode == LOSE_SCREEN:
                self._draw_game_over_screen()
                
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
            elif self._feature != len(ATTRIBUTES) - 1 and \
            cursor_x >= 660 and cursor_x <= 700 \
            and cursor_y >= 110 and cursor_y <= 150:
                self._feature += 1
                
            elif cursor_x >= 250 and cursor_x <= 550 \
            and cursor_y >= 700 and cursor_y <= 760:
                self._mode = GAME_SCREEN
                
            y_pos = 100
            for ft in ATTRIBUTES[self._feature].keys():
                y_pos += 85
                if cursor_x >= 50 and cursor_x <= 350 \
                and cursor_y >= y_pos and cursor_y <= y_pos + 65:
                    self._change_feature(ft)
        
        # 620,700,160,80
        elif self._mode == GAME_SCREEN:
            if cursor_x >= 620 and cursor_x <= 780 \
            and cursor_y >= 700 and cursor_y <= 780:
                if not self._animal.is_alive():
                    self._mode = LOSE_SCREEN
                elif self._environment <= len(self._environments) - 2:
                    if self._before_enviro:
                        self._before_enviro = False
                        self._last_known_health = self._animal.hp
                        self._most_damaging_feature = self._animal.will_survive(self._environments[self._environment])
                        self._write_enviro_sentence()
                    else:
                        self._environment += 1
                        self._write_intro_sentence()
                        self._before_enviro = True
                else:
                    self._most_damaging_feature = self._animal.will_survive(self._environments[self._environment])
                    self._write_enviro_sentence()
                    if self._animal.is_alive():
                        self._mode = WIN_SCREEN
                    else:
                        self._mode = LOSE_SCREEN
                        
                    
                
        # (200,600,400,100)
        elif self._mode == LOSE_SCREEN:
            if cursor_x >= 200 and cursor_x <= 600 \
            and cursor_y >= 600 and cursor_y <= 700:
                self._mode = START_SCREEN
                
                
    def _draw_game_screen(self):
        self._draw_environment()
        surface = pygame.display.get_surface()
        
        font = pygame.font.Font(None, 70)
        next_text = font.render("Next", True, white)
        pygame.draw.rect(surface, pygame.color.Color("#60cadb"), (620,700,160,80))
        surface.blit(next_text, (645,720))
        
        img = pygame.image.load("backgrounds/text_box.png")
        surface.blit(pygame.transform.scale(img, (800,800)), (0,0))
        
        font = pygame.font.Font(None, 30)
        if self._sentence != None:
            if "!" in self._sentence:
                sentences = self._sentence.split("!")
                for i in range(len(sentences)):
                    narration = font.render(f"{sentences[i].lstrip()}", True, white)
                    surface.blit(narration, (120,280+i*30))
            elif "." in self._sentence:
                sentences = self._sentence.split(".")
                for i in range(len(sentences)):
                    narration = font.render(f"{sentences[i].lstrip()}", True, white)
                    surface.blit(narration, (120,280+i*30))
            else:
                narration = font.render(f"{self._sentence}", True, white)
                surface.blit(narration, (120,280))
                
        img = pygame.image.load(f"animal/{self._animal.color}.png")
        img = pygame.transform.scale(img, (100,100))
        surface.blit(img, (400-img.get_width()/2,120))
            
        
                
    def _draw_game_over_screen(self):
        self._draw_environment()
        self._add_dark_overlay()
        surface = pygame.display.get_surface()

        font = pygame.font.Font(None, 100)
        gameOver = font.render("Try again :(", True, white)
        font = pygame.font.Font(None, 60)
        gameOver1 = font.render("Your animal wasn't fit enough", True, white)
        gameOver2 = font.render("Health Dropped Down To", True, white)
        font = pygame.font.Font(None, 200)
        gameOver3 = font.render("0", True, white)
        surface.blit(gameOver, (400-gameOver.get_width()/2,200))
        surface.blit(gameOver1, (400-gameOver1.get_width()/2,300))
        surface.blit(gameOver2, (400-gameOver2.get_width()/2,350))
        surface.blit(gameOver3, (400-gameOver3.get_width()/2,450))
        
        pygame.draw.rect(surface, pygame.color.Color("#60cadb"), (200,600,400,100))
        font = pygame.font.Font(None, 100)
        start_over = font.render("Start Over", True, white)
        surface.blit(start_over, (400-start_over.get_width()/2,620))
    
    
    def _draw_start_screen(self):
        self._setup_game()
        surface = pygame.display.get_surface()
        self._draw_default_background()
        
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
        img = pygame.image.load("backgrounds/build.png")
        surface.blit(img, (0,0))

        font = pygame.font.Font(None, 90)
        
        title = font.render(ANAMES[self._feature], True, white)
        surface.blit(title, (400-title.get_width()/2,100))
        
        font = pygame.font.Font(None, 50)
        # Left button
        if self._feature != 0:
            prev = font.render("Prev", True, white)
            surface.blit(prev, (85,70))
            pygame.draw.polygon(surface, white, [(100,130), (140,110), (140,150)])
            
        # Right button
        if self._feature != len(ATTRIBUTES) - 1:
            next = font.render("Next", True, white)
            surface.blit(next, (645,70))
            pygame.draw.polygon(surface, white, [(700,130), (660,110), (660,150)])
            
        x_pos = 50
        y_pos = 100
        font = pygame.font.Font(None, 65)
        for ft in ATTRIBUTES[self._feature].keys():
            y_pos += 85
            
            if self._animal.breath == ft \
            or self._animal.diet == ft \
            or self._animal.skin == ft \
            or self._animal.move == ft \
            or self._animal.color == ft:
                color = "#5392d6"
            else:
                color = "#60dbec"
                
            pygame.draw.rect(surface,  pygame.color.Color(color), (x_pos,y_pos,300,65))
            text = font.render(ft.capitalize(), True, white)
            surface.blit(text,(200-text.get_width()/2,y_pos+10))
            
        img = pygame.image.load(f"animal/{self._animal.color}.png")
        surface.blit(pygame.transform.scale(img, (300,300)), (450,250))
        
        done = font.render("Done", True, white)
        pygame.draw.rect(surface, pygame.color.Color("#444444"), (250,700,300,60) )
        surface.blit(done, (400-done.get_width()/2,710))
                    
                    
    def _draw_win_screen(self):
        surface = pygame.display.get_surface()
        self._draw_default_background()
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
        change = [self._animal.change_skin, self._animal.change_diet,
                  self._animal.change_move, self._animal.change_breath,
                  self._animal.change_color]
        change[self._feature](feature)
        
        
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
        hp = font.render("HP", True, black)
        surface.blit(hp, (360,0))
        
        
    def _draw_environment(self):
        screen = pygame.display.get_surface()
        img = pygame.image.load(f"backgrounds/{self._environments[self._environment]}.png")
        screen.blit(pygame.transform.scale(img, (800,800)), (0,0))
        self._draw_hp_bar()
        
    
    def _draw_default_background(self):
        surface = pygame.display.get_surface()
        img = pygame.image.load("backgrounds/default.png")
        surface.blit(pygame.transform.scale(img, (800,800)), (0,0))
        
        
    def _add_dark_overlay(self):
        screen = pygame.display.get_surface()
        img = pygame.image.load("backgrounds/dark_overlay.png")
        screen.blit(pygame.transform.scale(img, (800,800)), (0,0))
        self._draw_hp_bar()
        
        
    def _setup_game(self):
        self._feature = 0
        self._next_game_screen = False
        self._environments = aa.ENVIRONMENTS
        random.shuffle(self._environments)
        self._before_enviro = True
        self._environment = 0
        self._last_known_health = 100
        self._write_intro_sentence()
        self._animal = Animal(None, None, None, None, "brown")
        
        
    def _write_intro_sentence(self):
        sentence_split = random.choice(sentence_parts['intro']).split("_")
        self._sentence = f"{self._environments[self._environment]}".join(sentence_split)
    
    
    def _write_enviro_sentence(self):
        attributes = [self._animal.skin, self._animal.diet, self._animal.move, self._animal.breath, self._animal.color]
        a_names = ["skin", "diet","move", "breath", "color"]
        
        no_feature = False
        for i in range(len(attributes)):
            if attributes[i] == None:
                no_feature = True
                break
        if no_feature:
            self._sentence = f"{random.choice(sentence_parts['missing ' + a_names[i]])}. Make sure to select a choice for {a_names[i]} next time."
        elif self._animal.hp == 0:
            self._sentence = f"{random.choice(sentence_parts['h gone'])}"
            if no_feature:
                self._sentence += "You haven't selected a " + a_names[i] + " type. You can't live without that."
            else:
                self._sentence += f"Your {self._most_damaging_feature} led to your death. That feature hurts your health in this environment."
        elif self._last_known_health < self._animal.hp:
            self._sentence = f"{random.choice(sentence_parts['h up'])}"            
        elif self._last_known_health > self._animal.hp:
            self._sentence = f"{random.choice(sentence_parts['h down'])}"
            if no_feature:
                self._sentence += "You haven't selected a " + a_names[i] + " type"
            else:
                self._sentence += f"Due to your {self._most_damaging_feature}, you lost health. This doesn't help you in this sort of environment."
        else:
            self._sentence = f"{random.choice(sentence_parts['h same'])}"

