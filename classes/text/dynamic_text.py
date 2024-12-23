import pygame
from config import FPS

from config.soundmanager import SoundManager


class DynamicText:
    """Classe mostra o texto dinamicamente, letra por letra
    """
    def __init__(
        self,
        text: str,
        font: str,
        letters_per_second: int,
        text_size: int = 12,
        max_length: float = 0,
        position: tuple[float] = (0,0),
        color: pygame.Color = (255,255,255),
        sound: str = None
    ):
        """Inicialização da classe

        Args:
            text (str): Qual o texto deve ser exibido
            font (str): O nome da fonte que vai ser usada (Olhar no gerenciador de fontes)
            size (int, optional): Tamanho da fonte. Defaults to 12.
            color (pygame.Color, optional): Cor da fonte. Defaults to (255, 255, 255).
            letters_per_second (int): Quantas letras aparecem por segundo
        """

        self.text = text  # Texto Completo
        self.progressive_text = ''  # Texto que vai ser alterado para dar o efeito de letra por letra
        self.font = pygame.font.Font(font, text_size)  # Fonte que vai ser usada

        self.max_length = max_length  # Largura máxima
        self.position = position  # Posição do texto
        self.color = color  # Cor do texto

        self.rows = [  # Lista que vai contar as linhas
            self.font.render(self.progressive_text, True, self.color)
        ]
        self.wich_row_to_update = 0  # Qual linha está sendo atualizada
        self.letter_counter = 0  # Contador para saber a próxima letra

        self.counter = 0  # Variável que controla quando uma nova letra vai ser adicionada
        self.letter_rate = FPS/letters_per_second  # Frequência de letras por segundo

        self.finished = False  # Variavel que diz se o texto ja foi todo escrito

        self.sound = sound

    def restart(self, new_text: str = None):
        if new_text:
            self.text = new_text
        self.progressive_text = ''
        self.counter = 0
        self.wich_row_to_update = 0
        self.letter_counter = 0
        self.rows = [
            self.font.render(self.progressive_text, True, self.color)
        ]
        self.finished = False
    
    def skip_text(self):
        self.progressive_text = ''
        for letter in self.text:
            self.progressive_text += letter

            new_text = self.font.render(self.progressive_text, True, self.color)

            if new_text.get_rect().width >= self.max_length:  # Se a linha passar da largura máxima
                self.progressive_text = letter
                self.rows.append(self.font.render(self.progressive_text, True, self.color))
                self.wich_row_to_update += 1

                new_text = self.font.render(self.progressive_text, True, self.color)

            # Atualizo a linha com o novo texto
            self.rows[self.wich_row_to_update] = new_text

            # Atualizo a próxima letra
            self.letter_counter += 1

        self.finished = True
        
    def update(self, *args, **kwargs):

        self.counter += 1  # Incrementa o contador

        # Se for hora de adicionar uma nova letra e ainda restarem letras a processar
        if self.counter >= self.letter_rate and not self.letter_counter >= len(self.text):
            self.counter = 0  # Reseta o contador
            
            if self.text[self.letter_counter] != ' ' and self.sound:
                SoundManager.stop_sound(self.sound)
                SoundManager.play_sound(self.sound)

            # Pegamos o texto restante
            remaining_text = self.text[self.letter_counter:]
            next_space_index = remaining_text.find(' ')  # Índice do próximo espaço
            if next_space_index == -1:
                next_space_index = len(remaining_text)  # Última palavra

            # Define a palavra atual
            next_word = remaining_text[:next_space_index + 1]

            # Renderiza a linha atual com a próxima palavra para checar o tamanho
            temp_line = self.progressive_text + next_word
            rendered_line = self.font.render(temp_line, True, self.color)

            # Se a próxima palavra não couber, inicie uma nova linha
            if rendered_line.get_rect().width >= self.max_length:
                self.progressive_text = ''  # Reseta o texto da linha
                self.rows.append(self.font.render(self.progressive_text, True, self.color))
                self.wich_row_to_update += 1

            # Adiciona uma letra à vez na linha atual
            next_letter = self.text[self.letter_counter]
            self.progressive_text += next_letter

            # Atualiza o texto renderizado
            new_text = self.font.render(self.progressive_text, True, self.color)

            # Atualiza a linha atual
            self.rows[self.wich_row_to_update] = new_text

            # Incrementa o contador de letras
            self.letter_counter += 1

            # Se todo o texto foi processado, marca como finalizado
            if self.letter_counter >= len(self.text):
                self.finished = True



    def draw(self, screen: pygame.Surface):
        for i, text in enumerate(self.rows):
            text_rect = text.get_rect()
            text_rect.x = self.position[0]
            text_rect.y = self.position[1]+i*text_rect.height
            screen.blit(text, text_rect)
