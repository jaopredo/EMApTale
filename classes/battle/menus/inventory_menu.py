import pygame
import os
import math

from config import *
from config.fontmanager import FontManager
from config.soundmanager import SoundManager

from classes.battle.container import BattleContainer
from classes.battle.menus import BattleMenu
from classes.battle.menus.battle_menu_manager import BattleMenuManager

from classes.player import Player
from classes.text.text import Text

class InventoryMenu(BattleMenu):
    def __init__(self, battle_container: BattleContainer):
        self.__options: list[dict] = []  # Lista de opções
        self.container = battle_container  # Container dos menus
        self.display = pygame.display.get_surface()  # A tela do jogo

        self.selected_option = 0
        self.trying_to_move_cursor = False  # Variável responsável por controlar e mexer apenas uma opção por vez, sem que o cursor mexa que nem doido

        # Carregando o sprite do cursor
        self.cursor = pygame.transform.scale_by(
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'player', 'hearts', 'heart.png')),
            1.8
        )
        self.cursor_rect = self.cursor.get_rect()

        # Adicionando os itens como minhas opções
        for i, item in enumerate(Player.inventory):
            self.__options.append({
                'text': Text(f'{i}.{item.name}', FontManager.fonts['Gamer'], int((450*100)/self.display.get_height())),
                'func': lambda: print(item.name)
            })
        
        self.page = 0
        self.items_per_column = 0

        for i, opt in enumerate(self.__options):
            if opt['text'].rect.height*i > self.container.inner_rect.height:
                self.items_per_column = i
                break
        
        self.items_per_page = self.items_per_column * 2
    
    def move_cursor(self, increment: int):
        """Função responsável por atualizar o índice do cursor

        Args:
            increment (int): Quanto a opção deve aumentar ou diminuir
        """
        self.selected_option = (self.selected_option+increment)%len(self.__options)

        self.page = math.floor(self.selected_option/(self.items_per_page))

    def update(self):
        keys = pygame.key.get_pressed()

        self.cursor_rect.center = self.__options[self.selected_option]['text'].rect.center
        self.cursor_rect.left = self.__options[self.selected_option]['text'].rect.right

        if not self.trying_to_move_cursor:
            if keys[pygame.K_DOWN]:
                self.move_cursor(1)
                self.trying_to_move_cursor = True
                SoundManager.play_sound('select.wav')
            if keys[pygame.K_UP]:
                self.move_cursor(-1)
                self.trying_to_move_cursor = True
                SoundManager.play_sound('select.wav')
            if keys[pygame.K_LEFT]:
                self.move_cursor(-self.items_per_column)
                self.trying_to_move_cursor = True
                print(self.selected_option)
            if keys[pygame.K_RIGHT]:
                self.move_cursor(self.items_per_column)
                self.trying_to_move_cursor = True
                SoundManager.play_sound('select.wav')
        
        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.trying_to_move_cursor = False

        if keys[pygame.K_x] or keys[pygame.K_BACKSPACE]:  # Para eu voltar no menu anterior
            BattleMenuManager.go_back()
    
    def draw(self):
        column = 0
        for i in range(self.items_per_page):
            if i >= self.items_per_column:
                column = 1
            
            if (i+self.items_per_page*self.page) >= len(self.__options):
                break
            
            self.__options[(i+self.items_per_page*self.page)]['text'].rect.x = self.container.inner_rect.x + 10*abs(column-1) + self.container.inner_rect.width*column/2
            self.__options[(i+self.items_per_page*self.page)]['text'].rect.y = self.container.inner_rect.y + self.__options[(i+self.items_per_page*self.page)]['text'].rect.height*(i%self.items_per_column)

            self.__options[(i+self.items_per_page*self.page)]['text'].draw(self.display)
        
        self.display.blit(self.cursor, self.cursor_rect)
    
    @property
    def options(self):
        return self.__options
