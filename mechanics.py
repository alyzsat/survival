'''
Created on Apr 6, 2019

@author: Nayeri
'''

from animal_attributes import SKIN 
from animal_attributes import DIET
from animal_attributes import MOVE
from animal_attributes import BREATH
from animal_attributes import COLOR


class Animal:
    skin = None
    diet = None
    move = None
    breath = None
    color = None
    hp = 0 
    
    def __init__ (self, s, d, m, b, c):
        self.skin = s
        self.diet = d
        self.move = m 
        self.breath = b
        self.color = c
        self.hp = 100
        
    #adjust the hp, enviro is str
    #func changes the hp
    def will_survive (self, enviro) -> str:
        '''Returns the feature that causes it to lose the most damage'''
        attributes = [self.skin, self.move, self.breath, self.diet]
        for att in attributes:
            if att == None:
                self.kill()
                return "missing bodily functions"
                
        if self.is_alive():
            self.hp += SKIN [self.skin] [enviro]
            self.hp += DIET [self.diet] [enviro]
            self.hp += MOVE [self.move] [enviro]
            self.hp += BREATH [self.breath] [enviro]
            self.hp += COLOR [self.color] [enviro]
            if self.hp > 100:
                self.hp = 100
            elif self.hp < 0:
                self.hp = 0
                
            damages = [SKIN [self.skin] [enviro], DIET [self.diet] [enviro],
                       MOVE [self.move] [enviro], BREATH [self.breath] [enviro]]
            
            if SKIN [self.skin] [enviro] < sum(damages)/len(damages):
                return self.skin
            if DIET [self.diet] [enviro] < sum(damages)/len(damages):
                return self.diet
            if MOVE [self.move] [enviro] < sum(damages)/len(damages):
                return self.move
            if BREATH [self.breath] [enviro] < sum(damages)/len(damages):
                return self.breath
        
    def is_alive (self):
        return self.hp > 0
    
    def change_skin(self, newS):
        self.skin = newS
    
    def change_diet(self, newD):
        self.diet = newD
    
    def change_move(self,newM):
        self.move = newM
    
    def change_breath(self, newB):
        self.breath = newB
    
    def change_color(self, newC):
        self.color = newC
        
    def kill(self):
        self.hp = 0
        
    
    
    
