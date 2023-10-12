import pygame
import enchant
from settings import *

#show text on surface with parameters given
def draw_text(surface,text,size,color,x,y,orientation):
    font=pygame.font.Font(pygame.font.match_font(FONT_NAME),size)
    text_surface=font.render(text,True,color)
    text_rect=text_surface.get_rect()
    if orientation=='topleft':
        text_rect.topleft=(x,y)
    elif orientation=='midtop':
        text_rect.midtop=(x,y)
    elif orientation=='center':
        text_rect.center=(x,y)
    surface.blit(text_surface,text_rect)

#classes
class Board(pygame.sprite.Sprite):
    def __init__(self,game,x,y,word,num_rounds=6,num_chars=5):
        self.game=game
        self.groups=self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)
        
        self.BORDER=10
        self.TILE_SIZE=(SIDE-(max(num_chars,num_rounds)+1)*self.BORDER)//max(num_chars,num_rounds)
        
        #create game board
        self.image=pygame.Surface((WIDTH,(max(num_chars,num_rounds)+1)*self.BORDER+self.TILE_SIZE*max(num_chars,num_rounds)))
        self.image.fill(BG_COLOR_1)
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
        
        #contain actual characters or None if blank
        self.tiles=[]
        for _ in range(num_rounds):
            row=[]
            for _ in range(num_chars):
                row.append(None)
            self.tiles.append(row)
            
        #contain colors (tuples from settings) to show if char in tile is correct or not
        self.color_tiles=[]
        for _ in range(num_rounds):
            row=[]
            for _ in range(num_chars):
                row.append(WHITE)
            self.color_tiles.append(row)
        
        self.num_rounds=num_rounds
        self.num_chars=num_chars
        self.round=0
        self.char=0
        
        self.word_str=word.upper()
        self.word=list(self.word_str)
        
        self.dict=enchant.Dict("en_US")
        self.current_round_color=BLACK
        
    #update tiles on board on GUI with letters and colors
    def update(self):
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles[i])):
                start_x=WIDTH//2-(int(self.num_chars/2*self.TILE_SIZE)+(self.num_chars//2+1)*self.BORDER)
                
                pygame.draw.rect(self.image,self.color_tiles[i][j],(start_x+self.BORDER+j*(self.TILE_SIZE+self.BORDER),self.BORDER+i*(self.TILE_SIZE+self.BORDER),self.TILE_SIZE,self.TILE_SIZE))
                if self.tiles[i][j] is not None:
                    if i==self.round:
                        draw_text(self.image,self.tiles[i][j],32,self.current_round_color,start_x+self.BORDER+j*(self.TILE_SIZE+self.BORDER)+self.TILE_SIZE/2,self.BORDER+i*(self.TILE_SIZE+self.BORDER)+self.TILE_SIZE/2,'center')
                    else:
                        draw_text(self.image,self.tiles[i][j],32,BLACK,start_x+self.BORDER+j*(self.TILE_SIZE+self.BORDER)+self.TILE_SIZE/2,self.BORDER+i*(self.TILE_SIZE+self.BORDER)+self.TILE_SIZE/2,'center')
    
    #add letter to the current round, if you can
    def add_letter(self,letter):
        if self.can_add_letter():
            self.tiles[self.round][self.char]=letter
            self.char+=1
            
    #delete letter from the current round, if you can
    def delete_letter(self):
        if self.can_delete_letter():
            self.char-=1
            self.tiles[self.round][self.char]=None
            self.current_round_color=BLACK
            
    #submit a full word and check which letters are correct, and end the game if necessary. If you can
    def submit_word(self):
        if self.can_submit_word():
            for i in range(len(self.tiles[self.round])):
                if self.tiles[self.round][i]==self.word[i]:
                    self.color_tiles[self.round][i]=GREEN #means letter is correct
                    self.game.update_letter_button(self.tiles[self.round][i],GREEN)
                elif self.tiles[self.round][i] in self.word and self.check_yellow(i):
                    self.color_tiles[self.round][i]=YELLOW #letter is in word, but not at this index
                    self.game.update_letter_button(self.tiles[self.round][i],YELLOW)
                else:
                    self.color_tiles[self.round][i]=RED #letter is not in word at all
                    self.game.update_letter_button(self.tiles[self.round][i],RED)
            
            if self.tiles[self.round]==self.word:
                self.game.page='end'
            else:
                self.round+=1
                self.char=0
                
            if self.round>=self.num_rounds:
                self.game.page='end'
                
            if self.game.page=='end':
                self.game.stats[self.round]+=1
                self.game.stat_total+=1
                stats_str=''
                for stat in self.game.stats:
                    stats_str+=str(stat)+'\n'
                with open('stats.txt','w') as file:
                    file.write(stats_str)
                    
    #check if tile at index i in current round row should be yellow.
    #if only one of this letter is in the word and it's not at i but hasn't been found yet,
    #or if there is more than one of this letter and at least one hasn't been found
    def check_yellow(self, i):
        target=self.tiles[self.round][i]
        for ind in range(len(self.word_str)):
            if self.word_str[ind]==target and self.tiles[self.round][ind]!=target:   
                return True
        return False
    
    #current round is not full, so can add a letter
    def can_add_letter(self):
        return self.round<self.num_rounds and self.char<self.num_chars
    
    #current round is not empty, so can delete a letter
    def can_delete_letter(self):
        return self.round<self.num_rounds and self.char>0
    
    #current round is full and word is real word, so can submit the word
    def can_submit_word(self):
        if self.char==self.num_chars:
            word=''
            for char in self.tiles[self.round]:
                word+=char
            is_word=self.dict.check(word)
            if not is_word:
                self.current_round_color=RED
        return self.round<self.num_rounds and self.char==self.num_chars and is_word
    
    def reset(self,word):
        for row in self.tiles:
            for i in range(len(row)):
                row[i]=None
                
        for row in self.color_tiles:
            for i in range(len(row)):
                row[i]=WHITE
                
        self.word_str=word.upper()
        self.word=list(self.word_str)
        self.round=0
        self.char=0
    
class Button:
    def __init__(self,game,x,y,image):
        self.game=game
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.centerx=x
        self.rect.y=y
        self.clicked=False
    
    def draw(self):
        action=False
        #get mouse pos
        pos=pygame.mouse.get_pos()
        
        #check mouseover and click conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1 and not self.clicked:
                self.clicked=True
                action=True
            if pygame.mouse.get_pressed()[0]==0 and self.clicked:
                self.clicked=False
        
        self.game.screen.blit(self.image,self.rect)
        return action
    
class Letter_Button(Button):
    def __init__(self,game,x,y,image):
        Button.__init__(self,game,x,y,image)
        self.color=WHITE
