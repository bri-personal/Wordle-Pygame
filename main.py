import pygame
import random
from os import path
from settings import *
from sprites import *
from words import *
        
class Game:
    def __init__(self):
        #initialize pygame and create window
        pygame.init()
        pygame.mixer.init()
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock=pygame.time.Clock()
        self.font_name=pygame.font.match_font(FONT_NAME)
        self.load_data()
        self.running=True
        
    #load images, sounds, etc.
    def load_data(self):
        self.dir=path.dirname(__file__)
        self.img_dir=path.join(self.dir,'img')
        self.snd_dir=path.join(self.dir,'snd')
    
    #start a new game
    def new(self):
        self.all_sprites=pygame.sprite.Group()
        #num_rounds default to 5 and num_chars default to 6. this is the order they are in the param list
        self.board=Board(self,0,0,random.choice(WORDS_5))
        
        #make reset button
        img=pygame.Surface((SIDE//3,self.board.TILE_SIZE*2//3))
        img.fill(BLACK)
        img_rect=img.get_rect()
        pygame.draw.rect(img,WHITE,(5,5,img_rect.width-10,img_rect.height-10))
        draw_text(img,'NEW WORD',36,RED,img_rect.width//2,img_rect.height//2,'center')
        self.reset_button=Button(self,WIDTH//2,self.board.rect.height//2-BORDER-img_rect.height,img)
        
        #make back button for stats page
        img=pygame.Surface((SIDE//3,self.board.TILE_SIZE*2//3))
        img.fill(BLACK)
        img_rect=img.get_rect()
        pygame.draw.rect(img,WHITE,(5,5,img_rect.width-10,img_rect.height-10))
        draw_text(img,'BACK',36,RED,img_rect.width//2,img_rect.height//2,'center')
        self.back_button=Button(self,WIDTH//2,HEIGHT-BORDER*3-img_rect.height,img)
        
        #make reset stats button for stats page
        img=pygame.Surface((SIDE//3,self.board.TILE_SIZE*2//3))
        img.fill(BLACK)
        img_rect=img.get_rect()
        pygame.draw.rect(img,WHITE,(5,5,img_rect.width-10,img_rect.height-10))
        draw_text(img,'RESET',36,RED,img_rect.width//2,img_rect.height//2,'center')
        self.reset_stats_button=Button(self,WIDTH//2,HEIGHT-BORDER*6-img_rect.height*2,img)
        
        #make stats button
        img=pygame.Surface((SIDE//3,self.board.TILE_SIZE*2//3))
        img.fill(BLACK)
        img_rect=img.get_rect()
        pygame.draw.rect(img,WHITE,(5,5,img_rect.width-10,img_rect.height-10))
        draw_text(img,'STATS',36,RED,img_rect.width//2,img_rect.height//2,'center')
        self.stats_button=Button(self,WIDTH//2,self.board.rect.height//2+BORDER,img)
        
        #make letter buttons
        self.letter_buttons={}
        x=WIDTH//2-int(LETTER_BUTTON_SIZE*5+BORDER*4.5)+LETTER_BUTTON_SIZE//2
        y=self.board.rect.bottom+BORDER
        for let in ['Q','W','E','R','T','Y','U','I','O','P']:
            img=pygame.Surface((LETTER_BUTTON_SIZE,LETTER_BUTTON_SIZE))
            img.fill(WHITE)
            img_rect=img.get_rect()
            draw_text(img,let,32,BLACK,img_rect.width//2,BORDER,'midtop')
            self.letter_buttons[let]=Letter_Button(self,x,y,img)
            x+=LETTER_BUTTON_SIZE+BORDER
           
        x=WIDTH//2-int(LETTER_BUTTON_SIZE*4.5+BORDER*4)+LETTER_BUTTON_SIZE//2
        y+=LETTER_BUTTON_SIZE+BORDER
        
        for let in ['A','S','D','F','G','H','J','K','L']:
            img=pygame.Surface((LETTER_BUTTON_SIZE,LETTER_BUTTON_SIZE))
            img.fill(WHITE)
            img_rect=img.get_rect()
            draw_text(img,let,32,BLACK,img_rect.width//2,BORDER,'midtop')
            self.letter_buttons[let]=Letter_Button(self,x,y,img)
            x+=LETTER_BUTTON_SIZE+BORDER
            
        x=WIDTH//2-int(LETTER_BUTTON_SIZE*3.5+BORDER*3)+LETTER_BUTTON_SIZE//2
        y+=LETTER_BUTTON_SIZE+BORDER
        
        for let in ['Z','X','C','V','B','N','M']:
            img=pygame.Surface((LETTER_BUTTON_SIZE,LETTER_BUTTON_SIZE))
            img.fill(WHITE)
            img_rect=img.get_rect()
            draw_text(img,let,32,BLACK,img_rect.width//2,img_rect.height//2,'center')
            self.letter_buttons[let]=Letter_Button(self,x,y,img)
            x+=LETTER_BUTTON_SIZE+BORDER
            
        #make enter button
        img=img=pygame.Surface((LETTER_BUTTON_SIZE*1.5,LETTER_BUTTON_SIZE))
        img.fill(WHITE)
        img_rect=img.get_rect()
        draw_text(img,'ENTER',24,BLACK,img_rect.width//2,img_rect.height//2,'center')
        self.enter_button=Button(self,WIDTH//2-int(LETTER_BUTTON_SIZE*5+BORDER*4.5)+LETTER_BUTTON_SIZE*1.5//2,self.board.rect.bottom+BORDER+(LETTER_BUTTON_SIZE+BORDER)*2,img)
        
        #make delete button
        img=img=pygame.Surface((LETTER_BUTTON_SIZE*1.5,LETTER_BUTTON_SIZE))
        img.fill(WHITE)
        img_rect=img.get_rect()
        draw_text(img,'DELETE',24,BLACK,img_rect.width//2,img_rect.height//2,'center')
        self.delete_button=Button(self,WIDTH//2+int(LETTER_BUTTON_SIZE*5+BORDER*4.5)-LETTER_BUTTON_SIZE*1.5//2,self.board.rect.bottom+BORDER+(LETTER_BUTTON_SIZE+BORDER)*2,img)
        
        #stats
        try:
            self.stats=[]
            with open('stats.txt') as file:
                lines = file.readlines()
                for line in lines:
                    self.stats.append(int(line))
        except:
            self.stats=[0,0,0,0,0,0,0] #6 rounds, plus 1 if you lose
            
        self.stat_total=0
        for stat in self.stats:
            self.stat_total+=stat
            
        self.page='play'
        self.run()

    #main loop calls other methods for specific pages
    def run(self):
        self.playing=True
        while self.playing:
            #keep loop running at correct speed
            self.clock.tick(FPS)
            if self.page=='play':
                self.play_screen()
            elif self.page=='end':
                self.end_screen()
            elif self.page=='stats':
                self.stats_screen()
            else:
                print("Page not found!")
                self.page='start'
            
    #default game loop method
    def play_screen(self):
        #process input (events)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_BACKSPACE:
                    self.board.delete_letter()
                if event.key==pygame.K_RETURN:
                    self.board.submit_word()
                if event.key==pygame.K_a:
                    self.board.add_letter('A')
                if event.key==pygame.K_b:
                    self.board.add_letter('B')
                if event.key==pygame.K_c:
                    self.board.add_letter('C')
                if event.key==pygame.K_d:
                    self.board.add_letter('D')
                if event.key==pygame.K_e:
                    self.board.add_letter('E')
                if event.key==pygame.K_f:
                    self.board.add_letter('F')
                if event.key==pygame.K_g:
                    self.board.add_letter('G')
                if event.key==pygame.K_h:
                    self.board.add_letter('H')
                if event.key==pygame.K_i:
                    self.board.add_letter('I')
                if event.key==pygame.K_j:
                    self.board.add_letter('J')
                if event.key==pygame.K_k:
                    self.board.add_letter('K')
                if event.key==pygame.K_l:
                    self.board.add_letter('L')
                if event.key==pygame.K_m:
                    self.board.add_letter('M')
                if event.key==pygame.K_n:
                    self.board.add_letter('N')
                if event.key==pygame.K_o:
                    self.board.add_letter('O')
                if event.key==pygame.K_p:
                    self.board.add_letter('P')
                if event.key==pygame.K_q:
                    self.board.add_letter('Q')
                if event.key==pygame.K_r:
                    self.board.add_letter('R')
                if event.key==pygame.K_s:
                    self.board.add_letter('S')
                if event.key==pygame.K_t:
                    self.board.add_letter('T')
                if event.key==pygame.K_u:
                    self.board.add_letter('U')
                if event.key==pygame.K_v:
                    self.board.add_letter('V')
                if event.key==pygame.K_w:
                    self.board.add_letter('W')
                if event.key==pygame.K_x:
                    self.board.add_letter('X')
                if event.key==pygame.K_y:
                    self.board.add_letter('Y')
                if event.key==pygame.K_z:
                    self.board.add_letter('Z')
        
        #update
        self.all_sprites.update()
        
        #draw/render
        self.screen.fill(BLACK)
        
        if self.enter_button.draw():
            self.board.submit_word()
            
        if self.delete_button.draw():
            self.board.delete_letter()
        
        for let in self.letter_buttons.keys():
            if self.letter_buttons[let].draw():
                self.board.add_letter(let)
        
        self.all_sprites.draw(self.screen)
        
        pygame.display.flip()

    def stats_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
                
        self.screen.fill(BLUE)
        pygame.draw.rect(self.screen,WHITE,(WIDTH//8,BORDER,WIDTH*3//4,HEIGHT-BORDER*6-self.back_button.rect.height))
        draw_text(self.screen,'STATS',48,BLACK,WIDTH//2,BORDER*2,'midtop')
        if self.stat_total==1:
            draw_text(self.screen,str(self.stat_total)+' Game',32,BLACK,WIDTH//2,BORDER*3+48,'midtop')
        else:
            draw_text(self.screen,str(self.stat_total)+' Games',32,BLACK,WIDTH//2,BORDER*3+48,'midtop')
        
        y=BORDER*4+48*2 
        for i in range(len(self.stats)):
            if i<6:
                draw_text(self.screen,str(i+1)+':',48,BLACK,WIDTH//8+BORDER*2,y,'topleft')
            else:
                draw_text(self.screen,'X:',48,BLACK,WIDTH//8+BORDER*2,y,'topleft')
            if self.stat_total>0:
                pygame.draw.rect(self.screen,BLUE,(WIDTH//8+BORDER*7,y,(WIDTH*3//4-BORDER*13)*self.stats[i]//self.stat_total,48))
                draw_text(self.screen,str(self.stats[i]),48,BLACK,WIDTH//8+BORDER*6+(WIDTH*3//4-BORDER*13)*self.stats[i]//self.stat_total+BORDER*2,y,'topleft')
            else:
                draw_text(self.screen,str(self.stats[i]),48,BLACK,WIDTH//8+BORDER*7+BORDER*2,y,'topleft')
            y+=BORDER+48
        
        if self.reset_stats_button.draw():
            self.reset_stats()
        if self.back_button.draw():
            self.page='end'
        
        pygame.display.flip()
        
    #end screen shown when game is over
    def end_screen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False
            
        #draw buttons/sprites from play screen, but they dont do anything
        self.screen.fill(BLACK)
        draw_text(self.screen,"GAME OVER",48,WHITE,WIDTH//2,SIDE+BORDER,'midtop')
        draw_text(self.screen,"THE WORD WAS "+self.board.word_str,32,WHITE,WIDTH//2,SIDE+BORDER*2+48,'midtop')
        if self.board.round<self.board.num_rounds:
            if self.board.round+1==1:
                draw_text(self.screen,"YOU WON IN "+str(self.board.round+1)+" ROUND",32,WHITE,WIDTH//2,SIDE+BORDER*3+48+32,'midtop')
            else:
                draw_text(self.screen,"YOU WON IN "+str(self.board.round+1)+" ROUNDS",32,WHITE,WIDTH//2,SIDE+BORDER*3+48+32,'midtop')
        
        self.all_sprites.draw(self.screen)
            
        if self.stats_button.draw():
            self.page='stats'
        
        if self.reset_button.draw():
            self.reset()
        pygame.display.flip()
        
    def reset(self):
        self.board.reset(random.choice(WORDS_5))
        for let in self.letter_buttons.keys():
            self.update_letter_button(let,WHITE)
        self.page='play'
        
    def reset_stats(self):
        self.stat_total=0
        for i in range(len(self.stats)):
            self.stats[i]=0
        #reset stats on file too
        stats_str=''
        for stat in self.stats:
            stats_str+=str(stat)+'\n'
        with open('stats.txt','w') as file:
            file.write(stats_str)
        
    def update_letter_button(self,let,color):
        if color!=YELLOW or (color==YELLOW and self.letter_buttons[let].color!=GREEN and self.letter_buttons[let].color!=RED):
            self.letter_buttons[let].color=color
            self.letter_buttons[let].image.fill(color)
            draw_text(self.letter_buttons[let].image,let,32,BLACK,self.letter_buttons[let].rect.width//2,BORDER,'midtop')
            

g=Game()
while g.running:
    g.new()

pygame.quit()