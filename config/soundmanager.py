import pygame
import os
from config import GET_PROJECT_PATH


class SoundManager:
    """Classe responsável pelo gerenciamento dos sons do jogo
    """
    audios: dict[str, pygame.mixer.Sound] = {
    }  # Dicionários dos sons carregados

    chanels: list[pygame.mixer.Channel] = [
    ]

    volume = 1  # Volume geral (Todo som vai ter o mesmo volume)

    @classmethod
    def add_chanel(cls):
        cls.chanels.append(pygame.mixer.Channel(len(cls.chanels)))

    @classmethod
    def is_chanel_playing(cls, id: int):
        return cls.chanels[id].get_busy()
    
    @classmethod
    def play_music(cls, file: str, loop: int = 0, start: float = 0, fade_ms: int = 0):
        """Dou play na música que foi passada

        Args:
            file (str): Caminho da música
            loop (int, optional): Quantas vezes vai dar loop, -1 repete indefinidamente. Defaults to 0.
            start (int, float): Momento no tempo em que a música é tocada. Defaults to 0.
            fade_ms (int, optional): Em quantos milisegundos a música vai se esvair até o volume 0. Defaults to 0.
        """
        pygame.mixer.music.unload()  
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(loop, start, fade_ms)
    
    @staticmethod
    def unload_music(cls):
        """Descarrega a música que está na fila
        """
        pygame.mixer.music.unload()
    
    @classmethod
    def load_all_sounds(cls):
        """Carrega todos os sons da pasta de sons
        """
        # Eu pego o local da pasta independente do sistema
        base_path = os.path.join(GET_PROJECT_PATH(), 'sounds')
        for sound in os.scandir(base_path):  # Para cada arquivo dentro da pasta de sons
            if 'msc' not in sound.name.split('_'):
                # Eu não carrego os arquivos do tipo "msc" pois
                #são músicas de fundo (Longas), vou carregar apenas os efeitos sonoros
                cls.audios[sound.name] = pygame.mixer.Sound(os.path.join(base_path, sound.name))
    
    @classmethod
    def unload_sounds(cls):
        """Deleto todos os sons que eu carreguei
        """
        for key in cls.audios.keys():
            del cls.audios[key]
    
    @classmethod
    def load_and_play(cls, sound):
        """Carrega um som e da play instantaneamente

        Args:
            sound (str): Nome do arquivo
        """
        pygame.mixer.Sound(os.path.join(GET_PROJECT_PATH(), 'sounds', sound)).play()
    
    @classmethod
    def play_sound(cls, sound_name: str, channel: int = None, loops: int = 0):
        """Tocar um son pelo nome passado

        Args:
            sound_name (str): Nome do arquivo que deve ser tocado
        """
        if channel != None:
            cls.chanels[channel].play(cls.audios[sound_name])
        else:
            cls.audios[sound_name].play(loops=loops)

    @classmethod
    def stop_sound(cls, sound_name: str):
        """Para o som especificado

        Args:
            sound_name (str): Nome do som
        """
        cls.audios[sound_name].stop()
    
    @staticmethod
    def stop_music():
        """Paro a música
        """
        pygame.mixer.music.stop()
    
    @staticmethod
    def pause_music():
        """Pauso a música
        """
        pygame.mixer.music.pause()
    
    @staticmethod
    def resume_music():
        """Resumo a música
        """
        pygame.mixer.music.unpause()
    
    @staticmethod
    def is_playing():
        """Retorna se o canal de música está sendo utilizado
        """
        return pygame.mixer.music.get_busy()
    

    # @property
    # def volume(self):
    #     """Getter do meu volume

    #     Returns:
    #         int: O valor atual do volume
    #     """
    #     return self.__volume

    # @volume.setter
    # def volume(self, vol: float):
    #     """Setter do meu volume

    #     Args:
    #         vol (float): Volume que eu quero colocar

    #     Raises:
    #         ValueError: Levanto se o valor não estiver entre 0 e 1
    #     """
    #     if not 0<=vol<=1:
    #         raise ValueError("Você precisa fornecer um número entre 0 e 1")
    #     self.__volume = vol
    #     pygame.mixer.music.set_volume(self.__volume)
