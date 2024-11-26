import pygame
from classes.text.dynamic_text import DynamicText
from config.eventmanager import EventManager

class InteractionManager:
    def __init__(self, interactions, player, chatbox, tecla_z_image):
        """
        Gerencia as interações do jogador com objetos do mapa.
        :param interactions: Lista de objetos de interação carregados do mapa.
        :param player: Referência ao jogador (para posição).
        :param chatbox: Imagem da caixa de texto.
        :param tecla_z_image: Imagem da tecla "Z" para exibir quando na área de interação.
        """
        self.interactions = interactions
        self.player = player
        self.active_interaction = None
        self.interaction_in_progress = False  # Para manter interações
        self.dynamic_text = None  # Controla o texto dinâmico da interação
        self.chatbox = chatbox
        self.tecla_z_image = tecla_z_image
        self.chatbox_position = None  # Será configurada na inicialização

    def set_chatbox_position(self, position):
        """
        Define a posição da caixa de texto.
        :param position: Posição da caixa de texto.
        """
        self.chatbox_position = position

    def check_interaction(self):
        """
        Verifica se o jogador está próximo de um objeto de interação.
        :param events: Lista de eventos do Pygame.
        :return: Objeto de interação ativo (se houver).
        """
        player_rect = self.player.rect
        for interaction in self.interactions:
            rect = pygame.Rect(interaction['x'], interaction['y'], interaction['width'], interaction['height'])

            # Jogador está na área de interação
            if player_rect.colliderect(rect):
                self.active_interaction = interaction
                return interaction

        # Se o jogador saiu de todas as áreas de interação
        self.active_interaction = None
        return None

    def handle_interaction(self):
        """
        Gerencia a lógica de interações, incluindo exibição de textos dinâmicos.
        :param events: Lista de eventos do Pygame.
        """
        for event in EventManager.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    # Inicia ou encerra interações
                    if self.dynamic_text:
                        if self.dynamic_text.finished:
                            # Encerra a interação
                            self.dynamic_text = None
                            self.active_interaction = None
                    elif self.active_interaction:
                        # Inicia interação com texto dinâmico
                        self.dynamic_text = DynamicText(
                            text=f"{self.active_interaction['value']}",
                            font="fonts/Gamer.ttf",
                            letters_per_second=20,
                            text_size=70,
                            position=(
                                self.chatbox_position[0] + 20,  # Margem lateral
                                self.chatbox_position[1] + 20  # Margem superior
                            ),
                            color=(255, 255, 255),
                            max_length=self.chatbox.get_width() - 40
                        )
                elif event.key == pygame.K_RETURN or event.key == pygame.K_z:
                    # Pula o texto se não estiver terminado
                    if self.dynamic_text and not self.dynamic_text.finished:
                        self.dynamic_text.skip_text()

    def render_interaction(self, display):
        """
        Renderiza elementos da interação (tecla "Z", caixa de texto, texto dinâmico).
        :param display: Superfície principal do Pygame.
        """
        # Exibe a tecla "Z" se o jogador estiver na área de interação
        if self.active_interaction and not self.dynamic_text:
            display.blit(self.tecla_z_image, (20, 20))

        # Renderiza a caixa de texto e o texto dinâmico
        if self.dynamic_text:
            display.blit(self.chatbox, self.chatbox_position)
            self.dynamic_text.update()
            self.dynamic_text.draw(display)
