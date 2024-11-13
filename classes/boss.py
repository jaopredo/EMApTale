from abc import ABC, abstractmethod
import pygame


class Boss(pygame.sprite.Sprite, ABC):
    @abstractmethod
    def take_damage(self, amount: float):...

    @abstractmethod
    def speak(self, text: str):...

    @abstractmethod
    def load_attacks(self):...

    @abstractmethod
    def draw(self, screen: pygame.Surface):...

    @property
    @abstractmethod
    def voice(self):...

    @property
    @abstractmethod
    def life(self):...

    @property
    @abstractmethod
    def max_life(self):...

    @property
    @abstractmethod
    def defense(self):...

    @property
    @abstractmethod
    def damage(self):...
