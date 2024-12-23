import pygame
import os
from screens import State

from config import *
from config.gamestatemanager import GameStateManager
from config.fontmanager import FontManager
from config.soundmanager import SoundManager
from config.eventmanager import EventManager

from classes.text.dynamic_text import DynamicText

class IntroCutscene(State):
    def __init__(self, name: str, display: pygame.Surface):
        self.__name = name
        self.__display = display
        self.__execution_counter = 0

        self.__variables = {}

        self.stage = 0
        self.texts = [
            "Bem vindo a Fundação Getulio Vargas! Após um longo semestre você se encontra em uma situação difícil...",
            "Conseguiu, com muito esforço, conquistar um CR 5.9, mas você precisa mais do que isso!",
            "Buscando a redenção, você pretende encarar as AS para se provar digno de um CR 7+",
            "Mas não tenha otimismo, pois 5 Entidades da EMAp tentarão impedi-lo de conseguir! Boa sorte!",
            "               ", 
            "                                   ", 
            " ", 

        ]
        self.images = [
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), "sprites", "cutscene", "c11.png")),
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), "sprites", "cutscene", "c12.png")),
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), "sprites", "cutscene", "c16.png")), 
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), "sprites", "cutscene", "c15.png")),
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), "sprites", "cutscene", "c18.jpeg")),
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), "sprites", "cutscene", "logo1-bgp.png")),
            pygame.image.load(os.path.join(GET_PROJECT_PATH(), "sprites", "cutscene", "c18.jpeg"))

        ]
        self.letters_per_second = 17

        self.current_text = DynamicText(
            text=self.texts[self.stage],
            font=FontManager.fonts['Pixel'],
            letters_per_second=self.letters_per_second,
            text_size=self.get_resolution_display(),
            max_length=self.__display.get_width() - 40,
            position=(self.__display.get_width() // 4, self.__display.get_height() // 1.6),
            color=(255, 255, 255),
            sound="text_2.wav"  
        )

        self.current_image = self.images[self.stage]

        # Variáveis que controlam o tempo dos elementos da cutscene
        self.initial_time = 0 # tempo global estático, inicial da cutscenes
        self.current_time_local = 0 # tempo local da cutscene, como se 0 inicia-se no mesmo momento
        self.wait_a_second = 2000 # tempo do intervalo em si, tempo do intervalo entre as imagens e textos
        self.last_time_define = 0 # contador interno para verificar se o intervalo foi passado ou não
       
        # Variáveis para alterar a opacidade das imagens no decorrer do tempo
        self.alpha = 0
        self.sub_alpha = 0

    def on_first_execution(self):

        self.current_time_local = 0 # tempo local da cutscene, como se 0 inicia-se no mesmo momento
        self.wait_a_second = 2000 # tempo do intervalo em si, tempo do intervalo entre
        self.last_time_define = 0 # contador interno para verificar se o intervalo foi passado ou não
        
        # Variáveis para alterar a opacidade das imagens no decorrer do tempo
        self.alpha = 0
        self.sub_alpha = 0

        self.stage = 0
        self.current_text = DynamicText(
            text=self.texts[self.stage],
            font=FontManager.fonts['Pixel'],
            letters_per_second=self.letters_per_second,
            text_size=self.get_resolution_display(),
            max_length=self.__display.get_width() - 40,
            position=(self.__display.get_width() // 4, self.__display.get_height() // 1.6),
            color=(255, 255, 255),
            sound="text_2.wav"  
        )
        SoundManager.stop_music()
        SoundManager.play_music(os.path.join(GET_PROJECT_PATH(), "sounds", "intro_history.mp3"))
       
       # Define uma única vez
        self.initial_time = pygame.time.get_ticks()


    def get_resolution_display(self):
        """Algo como a responsividade em CSS
        """
        
        # Pega as dimensões da tela
        info = pygame.display.Info()
        screen_width = info.current_w
        screen_height = info.current_h

        # Verifica a resolução e define valores mutáveis
        if screen_width == 1280 and screen_height == 720:  # HD
            return 30
        elif screen_width == 1920 and screen_height == 1080:  # FHD
            return 40
        else:  
            return 30


    def run(self):
        if not self.__execution_counter > 0:
            self.on_first_execution()
            self.__execution_counter += 1


        # ============== DEFINE PRINCIPALMENTE OS CONTROLES DO TEMPO ===============
        # Define as variáveis de tempo atuais, global=currenti_time e local=self.current_time_local
        current_time = pygame.time.get_ticks()
        self.current_time_local = current_time - self.initial_time

        # Define o last_time_define única e exclusivamente quando o texto acabou e seu valor for igual a zero 
        if self.current_text.finished and self.last_time_define == 0:
            self.last_time_define = self.current_time_local
            
            # Da útlima image history para o título do jogo, dar um intervalo maior (gerar suspense)
            if  self.stage == len(self.images) -1:
                self.wait_a_second += 1000
            else:
                self.wait_a_second = 1600   

        # Verificar se o tempo de espera passou
        if self.current_text.finished and self.last_time_define + self.wait_a_second < self.current_time_local:
            
            # Modifica as variáveis para continuar valendo o loop
            self.stage += 1
            self.last_time_define = 0            

            if self.stage < len(self.texts):
                self.current_text = DynamicText(
                    text=self.texts[self.stage],
                    font=FontManager.fonts['Pixel'],  
                    letters_per_second=self.letters_per_second,
                    text_size=self.get_resolution_display(),
                    max_length=self.__display.get_width() - 40,
                    position=(self.__display.get_width() // 4, self.__display.get_height() // 1.6),
                    color=(255, 255, 255),
                    sound="text_2.wav"
                )

                self.current_image = self.images[self.stage]


        # ============== CONFIGURA IAMGEM, TEMPOS E SONS ===============
        # Desenho da imagem e texto
        if self.stage < len(self.texts):  
            
            # Define a largura/altura da tela e da imagem (todas as imagens tem o mesmo tamanho! 1280 x 720)
            screen_width, screen_height = self.__display.get_size()
            image_width, image_height = self.current_image.get_size()

            # Configura o tamano e a posição da imagem, para a última, deixa em tela cheia
            if  self.stage == len(self.images)-2:
                # Para última imagem, deixa em tela cheia e toca a música
                new_width = screen_width * 1.01
                aspect_ratio = image_height / image_width  
                new_height = new_width * aspect_ratio  
                x_pos = screen_width * 0.5 - new_width * 0.5  
                y_pos = screen_height * 0.5 - new_height * 0.5  
                SoundManager.stop_music()
                SoundManager.play_sound("intro_noise.ogg")

            else:
                # Ajusta as variáveis da dimensão da iamgem e texto
                new_width = screen_width * 0.5  
                aspect_ratio = image_height / image_width  
                new_height = new_width * aspect_ratio  

                # Redimensionar a imagem
                resized_image = pygame.transform.scale(self.current_image, (int(new_width), int(new_height)))

                # Calcular a posição centralizada e levemente para cima
                x_pos = screen_width * 0.5 - new_width * 0.5 
                y_pos = screen_height * 0.5 - new_height * 0.5 - screen_height * 0.2 


            resized_image = pygame.transform.scale(self.current_image, (int(new_width), int(new_height)))
            image_rect = resized_image.get_rect(topleft=(x_pos, y_pos))
        

            # =============== CONTROLE DE OPACIDADE =================
            if self.stage < len(self.images) -3:

                # Define para esclarecer a imagem | Fade In
                if current_time - self.last_time_define >= self.wait_a_second:
                    self.alpha += 2
                
                # Define para escurecer a imagem | Fade On 
                if self.last_time_define != 0:
                    self.sub_alpha += 3.15
                    self.alpha = 255 - self.sub_alpha
                else:
                    self.sub_alpha = 0
            else:
                self.sub_alpha = 0
                self.alpha = 255
            # Deixa na escala dentro do alpha permitido, apenas por redundância
            self.alpha = min(max(self.alpha, 0), 255)
            # Valeu Spaniol pela Nice Dick!
            resized_image.set_alpha(self.alpha)

            
            # =============== PLOTA IMAGEM, CONFIGURA TEXTO, PLOTA TEXTO =================
            # Plota a imagem
            self.__display.blit(resized_image, image_rect)

            # Ajusta o texto para que não ultrapasse a largura da imagem
            text_max_width = new_width  
            self.current_text.max_length = int(text_max_width - 40) 
            self.current_text.update()
            # Plota o texto
            self.current_text.draw(self.__display)  


            # Pula a cutscene
            for event in EventManager.events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE or event.key == pygame.K_SPACE:
                        if self.stage < len(self.texts) -3:
                            self.stage += 1
                            self.current_text = DynamicText(
                                text=self.texts[self.stage],
                                font=FontManager.fonts['Pixel'],  
                                letters_per_second=self.letters_per_second,
                                text_size=self.get_resolution_display(),
                                max_length=self.__display.get_width() - 40,
                                position=(self.__display.get_width() // 4, self.__display.get_height() // 1.6),
                                color=(255, 255, 255),
                                sound="text_2.wav"
                            )
                            self.current_image = self.images[self.stage]
                    
        else:
            GameStateManager.set_state('emap')
            
        
    def on_last_execution(self):    
        self.__execution_counter = 0
        self.stage = 0 
        self.current_image = self.images[self.stage]
        self.current_text = self.texts[self.stage]
        SoundManager.stop_music()


    @property
    def execution_counter(self):
        return self.execution_counter


    @property
    def display(self):
        return self.display


    @property
    def name(self):
        return self.__name    
    
    
    @property
    def variables(self):
        return self.__variables
    

    @variables.setter
    def variables(self, value: dict):
        if not isinstance(value, dict):
            raise TypeError("Você precisa passar um dicionário")
        self.__variables = value
