import pygame
from screens import State
from config import *

from classes.battle.button import CombatButton
from classes.battle.container import BattleContainer

from classes.text.dynamic_text import DynamicText

from config.soundmanager import SoundManager
from config.gamestatemanager import GameStateManager
from config.fontmanager import FontManager

from classes.battle.heart import Heart


class Combat(State):
    def __init__(
        self,
        name: str,
        display: pygame.Surface,
        game_state_manager: GameStateManager,
    ):
        # Variáveis padrão de qualquer Cenário
        self.__name = name
        self.__display: pygame.Surface = display
        self.__game_state_manager: GameStateManager = game_state_manager

        self.__execution_counter = 0

        # Criando os groups de sprites
        self.buttons_group = pygame.sprite.Group()  # Grupo dos botões
        self.text_groups = pygame.sprite.Group()  # Grupo dos textos
        self.player_group = pygame.sprite.Group()  # Grupo do player

        # Carrgando o sprite do cursor
        self.cursor = pygame.transform.scale_by(
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'player', 'hearts', 'heart.png')),
            1.8
        )

        self.options: list[CombatButton] = [  # Lista com cada botão
            CombatButton(
                'fight',
                lambda: print('Lutar'),
                self.__display,
                self.cursor,
                [ self.buttons_group ],
                True
            ),
            CombatButton(
                'act',
                lambda: print('Lutar'),
                self.__display,
                self.cursor,
                [ self.buttons_group ],
            ),
            CombatButton(
                'item',
                lambda: print('Lutar'),
                self.__display,
                self.cursor,
                [ self.buttons_group ],
            ),
            CombatButton(
                'mercy',
                lambda: print('Lutar'),
                self.__display,
                self.cursor,
                [ self.buttons_group ],
            ),
        ]
        self.selected_option = 0  # A opção que eu estou analisando agora
        self.trying_to_move_cursor = False  # Variável responsável por controlar e mexer apenas uma opção por vez, sem que o cursor mexa que nem doido

        # Carregando o background da batalha
        self.background = pygame.transform.scale(
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), 'sprites', 'hud', 'battle-background.png')),
            (self.__display.get_width()/1.2, 300)
        )
        self.background_rect = self.background.get_rect()
        self.background_rect.centerx = self.__display.get_width()/2
        self.background_rect.y = 10

        # Iniciando o container da Batalha
        self.battle_container = BattleContainer(self.__display)

        # Variável que gerencia o turno
        self.turn = 'boss'  # "player" ou "boss"

        # Variáveis do Jogador
        self.player = Heart(self.battle_container, self.player_group)

        # self.interaction_text = DynamicText(
        #     'Um inimigo se aproxima',
        #     FontManager.fonts['Gamer'],
        #     30,
        #     40,
        #     [ self.text_groups ],
        #     (self.battle_container.inner_rect.x + 10, self.battle_container.inner_rect.y + 10)
        # )
    

    def move_cursor(self, increment: int):
        """Função responsável por atualizar o índice do cursor

        Args:
            increment (int): Quanto a opção deve aumentar ou diminuir
        """
        if self.selected_option + increment >= len(self.options):  # Se passar da quantidade de opções
            self.selected_option = 0  # Volto para a primeira
        elif self.selected_option + increment < 0:  # Se for menor que 0
            self.selected_option = len(self.options)-1  # Vou para a última opção
        else:  # Se não
            self.selected_option += increment  # Só ando quantas vezes foi pedido


    def on_first_execution(self):
        # Limpando os sons
        SoundManager.stop_music()

    def run(self):
        # Desenhando o background
        self.__display.blit(self.background, self.background_rect)

        # Desenhando Tudo
        self.buttons_group.draw(self.__display)
        self.battle_container.draw()

        # Dando Update em todos os elementos
        self.buttons_group.update()
        self.battle_container.update()

        # Pegando as teclas apertadas
        keys = pygame.key.get_pressed()

        # Ajustando Posição dos botões e suas propriedades
        for i, button in enumerate(self.options):
            if i == self.selected_option:  # Se o botão que eu estiver analisando for a opção selecionada
                button.activated = True  # Eu marco a propriedade de ativado
            else:
                button.activated = False  # Eu removo a propriedade de ativado

            button.rect.center = (  # Centralizo o botão
                (i+1)*(self.__display.get_width()/(len(self.options)+1)),  # Matemática para centralizar os botão bonitinho
                self.__display.get_height()-(button.rect.height)  # Mais matemática pra posicionamento
            )
        
        # Se for o turno do Player
        if self.turn == 'player':
            self.battle_container.resize(1000, 300)  # Redesenho o container da batalha

            # Mexendo cursor
            if keys[pygame.K_LEFT] and not self.trying_to_move_cursor:  # Se eu apertar para a esquerda e não tiver nenhuma seta sendo segurada
                self.move_cursor(-1)  # Movo uma opção
                self.trying_to_move_cursor = True  # Estou tentando mexer o cursor
                SoundManager.play_sound('select.wav')  # Toco o som de trocar opção
            elif keys[pygame.K_RIGHT] and not self.trying_to_move_cursor:  # Se eu aprtar para a direita e não tiver nenhuma seta sendo segurada
                self.move_cursor(1)
                self.trying_to_move_cursor = True
                SoundManager.play_sound('select.wav')
            
            if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                # Só permito mexer de novo o cursor se eu soltar a tecla e apertar de novo
                self.trying_to_move_cursor = False
        else:  # Sen não for o turno do player
            self.battle_container.resize(self.__display.get_width()/3, self.__display.get_height()/2-30)  # Redimensiono o container da batalha

            for btn in self.options:  # Ajustando para nenhum botão ficar selecionado
                btn.activated = False
            
            if keys[pygame.K_u]:
                self.player.apply_effect('inverse')
            
            # Draws que são apenas no turno do boss
            self.player_group.draw(self.__display)
            
            # Updates que são apenas do turno do boss
            self.player_group.update(display=self.__display)

        # Fim do ciclo de vida da cena
        if not self.__execution_counter > 0:
            self.on_first_execution()
            self.__execution_counter += 1
    
    def on_last_execution(self):
        self.__execution_counter = 0

    @property
    def execution_counter(self):
        return self.execution_counter

    @property
    def display(self):
        return self.display
    
    @property
    def game_state_manager(self):
        return self.__game_state_manager
    
    @property
    def name(self):
        return self.__name