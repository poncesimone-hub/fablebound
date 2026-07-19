"""
Sistema de Inimigos Comuns para o jogo Laura
"""

import pygame
from dataclasses import dataclass
from typing import Optional


@dataclass
class InimigoStats:
    """Estatísticas de inimigo comum"""
    nome: str
    hp: int
    velocidade: int
    dano: int
    recompensa_moedas: int


class Inimigo:
    """Classe base para inimigos comuns"""
    
    def __init__(self, x: float, y: float, stats: InimigoStats):
        self.x = x
        self.y = y
        self.stats = stats
        self.width = 30
        self.height = 40
        self.vx = stats.velocidade
        self.vy = 0
        self.gravidade = 0.5
        self.em_ar = True
        self.vivo = True
        
    def atualizar(self):
        """Atualiza o estado do inimigo"""
        # Movimento
        self.x += self.vx
        self.y += self.vy
        
        # Gravidade
        self.vy += self.gravidade
        
        # Limites da tela
        if self.x < 0 or self.x > 1280:
            self.vivo = False
            
        # Colisão com chão
        if self.y >= 720 - self.height:
            self.y = 720 - self.height
            self.em_ar = False
            self.vy = 0
            
    def sofrer_dano(self, dano: int):
        """Inimigo sofre dano"""
        self.stats.hp -= dano
        if self.stats.hp <= 0:
            self.vivo = False
            return True  # Inimigo morreu
        return False
        
    def desenhar(self, surface):
        """Desenha o inimigo na tela"""
        pygame.draw.rect(surface, (200, 50, 50), (self.x, self.y, self.width, self.height))
        
        # Barra de HP
        barra_y = self.y - 5
        pygame.draw.rect(surface, (100, 100, 100), (self.x, barra_y, self.width, 3))
        hp_percent = self.stats.hp / 20
        pygame.draw.rect(surface, (0, 255, 0), (self.x, barra_y, self.width * hp_percent, 3))


class Goblin(Inimigo):
    """Inimigo: Goblin"""
    
    def __init__(self, x: float, y: float):
        stats = InimigoStats(
            nome="Goblin",
            hp=20,
            velocidade=2,
            dano=5,
            recompensa_moedas=1
        )
        super().__init__(x, y, stats)


class Skeleton(Inimigo):
    """Inimigo: Esqueleto"""
    
    def __init__(self, x: float, y: float):
        stats = InimigoStats(
            nome="Skeleton",
            hp=30,
            velocidade=3,
            dano=8,
            recompensa_moedas=2
        )
        super().__init__(x, y, stats)


class Fantasma(Inimigo):
    """Inimigo: Fantasma"""
    
    def __init__(self, x: float, y: float):
        stats = InimigoStats(
            nome="Fantasma",
            hp=15,
            velocidade=1,
            dano=6,
            recompensa_moedas=1
        )
        super().__init__(x, y, stats)
        self.em_ar = False  # Fantasmas flutuam
        self.y -= 100
        
    def atualizar(self):
        """Fantasmas se movem diferente"""
        self.x += self.vx
        # Movimento ondulante
        self.y += self.vy * 0.1
        
        if self.x < 0 or self.x > 1280:
            self.vivo = False


class Aranha(Inimigo):
    """Inimigo: Aranha"""
    
    def __init__(self, x: float, y: float):
        stats = InimigoStats(
            nome="Aranha",
            hp=25,
            velocidade=2,
            dano=7,
            recompensa_moedas=2
        )
        super().__init__(x, y, stats)
