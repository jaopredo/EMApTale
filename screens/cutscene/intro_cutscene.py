import pygame
from screens import State
from config.gamestatemanager import GameStateManager
from config.fontmanager import FontManager
from config.soundmanager import SoundManager
from classes.text.dynamic_text import DynamicText

class IntroCutscene(State):
    def __init__(self, name: str, display: pygame.Surface, game_state_manager: GameStateManager):
        self.__name = name
        self.__display = display
        self.__game_state_manager = game_state_manager
        self.__execution_counter = 0

        self.stage = 0
        self.texts = [
            "Bem vindo a Fundação Getulio Vargas!",
            "Após um longo semestre de inúmeros desafios, você se encontra em uma situação difícil... ",
            "Conseguiu, com muito esforço, conquistar um CR 5.9, mas você quer - (e precisa) - mais do que isso!",
            "Buscando a redenção, você pretende encarar as Avaliações Suplementares para se provar digno de um CR 7+",
            "Mas não tenha otimisto, pois 5 Entidades da EMAp tentarão impedir você de conseguir",
            "Tenha cuidado e nunca se esqueça: você nunca estará sozinho...",
            "       ", 

        ]
        self.images = [
            pygame.image.load("/home/brunofs/core/fgv/cdia/p2/lp/a2/EMApTale/sprites/cutscene/c11.png"),
            pygame.image.load("/home/brunofs/core/fgv/cdia/p2/lp/a2/EMApTale/sprites/cutscene/c12.png"),
            pygame.image.load("/home/brunofs/core/fgv/cdia/p2/lp/a2/EMApTale/sprites/cutscene/c13.png"),
            pygame.image.load("/home/brunofs/core/fgv/cdia/p2/lp/a2/EMApTale/sprites/cutscene/c14.png"),
            pygame.image.load("/home/brunofs/core/fgv/cdia/p2/lp/a2/EMApTale/sprites/cutscene/c15.png"), 
            pygame.image.load("/home/brunofs/core/fgv/cdia/p2/lp/a2/EMApTale/sprites/cutscene/c16.png"),
            pygame.image.load("/home/brunofs/core/fgv/cdia/p2/lp/a2/EMApTale/sprites/cutscene/c17.png"),

        ]
        self.current_text = DynamicText(
            text=self.texts[self.stage],
            font=FontManager.fonts['Pixel'],
            letters_per_second=13,
            text_size=40,
            max_length=self.__display.get_width() - 40,
            position=(self.__display.get_width() // 4, self.__display.get_height() // 1.6)
        )
        self.current_image = self.images[self.stage]

        self.wait_after_text = 2200 
        self.last_stage_change_time = 4500 

        self.teste = 0

    def on_first_execution(self):
        SoundManager.stop_music()
        SoundManager.play_music("/home/brunofs/core/fgv/cdia/p2/lp/a2/EMApTale/sounds/intro_history.mp3", fade_ms=860)
        

    def run(self):
        current_time = pygame.time.get_ticks()

        print(current_time, self.wait_after_text, self.last_stage_change_time)

        if not self.__execution_counter > 0:
            self.on_first_execution()
            self.__execution_counter += 1

        # Marcar o tempo de término do texto apenas uma vez
        if self.current_text.is_finished and self.last_stage_change_time == 0:
            self.last_stage_change_time = current_time
            self.teste = current_time = 0

        # Verificar se o tempo de espera passou
        if self.current_text.is_finished and current_time - self.last_stage_change_time > self.wait_after_text:
            self.stage += 1
            self.last_stage_change_time = 0  # Resetar o tempo
            self.teste = current_time
            
            # Toca a música e aparece o nome do jogo
            if self.stage == len(self.images)-1:
                SoundManager.play_sound("intro_noise.ogg")

            # Configurar novo texto e imagem apenas se houver mais estágios
            if self.stage < len(self.texts):
                self.current_text = DynamicText(
                    text=self.texts[self.stage],
                    font=FontManager.fonts['Pixel'],
                    letters_per_second=15,
                    text_size=40,
                    max_length=self.__display.get_width() - 40,
                    position=(self.__display.get_width() // 4, self.__display.get_height() // 1.6)  # Posição fixa do texto
                )
                self.current_image = self.images[self.stage]

        # Desenho da imagem e texto
        if self.stage < len(self.texts):  # Garante que o estágio seja válido
            # Calcular a posição da imagem no centro, levemente para cima
            screen_width, screen_height = self.__display.get_size()
            image_width, image_height = self.current_image.get_size()

            # Redimensionar a imagem proporcionalmente
            new_width = screen_width * 0.5  # 50% da largura da tela
            aspect_ratio = image_height / image_width  # Calcula a razão de aspecto original
            new_height = new_width * aspect_ratio  # Ajusta a altura proporcionalmente

            # Redimensionar a imagem
            resized_image = pygame.transform.scale(self.current_image, (int(new_width), int(new_height)))
            resized_image.set_alpha((self.teste) / 10)

            # Calcular a posição centralizada e levemente para cima
            x_pos = screen_width * 0.5 - new_width * 0.5  # Centraliza horizontalmente
            y_pos = screen_height * 0.5 - new_height * 0.5 - screen_height * 0.2  # Centraliza verticalmente e sobe 20%

            image_rect = resized_image.get_rect(topleft=(x_pos, y_pos))
            self.__display.blit(resized_image, image_rect)

            # Ajustar o texto para que não ultrapasse a largura da imagem
            text_max_width = new_width  # A largura máxima para o texto é a largura da imagem
            self.current_text.max_length = int(text_max_width - 40)  # 40px de margem para o texto
            self.current_text.update()
            self.current_text.draw(self.__display)    
        

        else:
            self.__game_state_manager.set_state('emap')
            SoundManager.stop_music()
            

        
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
    def game_state_manager(self):
        return self.__game_state_manager