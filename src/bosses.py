"""
Sistema de Bosses para o jogo Laura
"""

import pygame
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional


class BossType(Enum):
    """Tipos de bosses disponíveis"""
    DRAGAO = "Dragão"
    CAVALEIRO = "Cavaleiro"
    MAGO = "Mago"
    BRUXA = "Bruxa"
    GIGANTE = "Gigante"
    PRINCESA = "Princesa"
    REI = "Rei"
    LIVRO_FINAL = "Livro - Boss Final"


@dataclass
class BossStats:
    """Estatísticas do boss"""
    nome: str
    tipo: BossType
    hp: int
    hp_max: int
    velocidade: int
    dano_ataque: int
    intervalo_ataque: int  # frames entre ataques
    recompensa_moedas: int
    dificuldade: int  # 1-10


class Boss:
    """Classe base para bosses"""
    
    def __init__(self, x: float, y: float, stats: BossStats):
        self.x = x
        self.y = y
        self.stats = stats
        self.width = 60
        self.height = 80
        self.vx = stats.velocidade
        self.contador_ataque = 0
        self.vivo = True
        self.tiros = []
        
    def atualizar(self, tiros_inimigos: List):
        """Atualiza o estado do boss"""
        # Movimento lateral
        self.x += self.vx
        
        # Inverter direção ao atingir limites
        if self.x <= 0 or self.x + self.width >= 1280:
            self.vx = -self.vx
            
        # Contador de ataque
        self.contador_ataque += 1
        if self.contador_ataque >= self.stats.intervalo_ataque:
            tiro = self.atacar()
            if tiro:
                tiros_inimigos.append(tiro)
            self.contador_ataque = 0
            
    def atacar(self) -> Optional[dict]:
        """Retorna um tiro do boss"""
        return {
            'tipo': 'boss_tiro',
            'x': self.x + self.width // 2,
            'y': self.y + self.height,
            'velocidade': 5,
            'dano': self.stats.dano_ataque
        }
        
    def sofrer_dano(self, dano: int):
        """Boss sofre dano"""
        self.stats.hp -= dano
        if self.stats.hp <= 0:
            self.vivo = False
            return True  # Boss morreu
        return False
        
    def desenhar(self, surface):
        """Desenha o boss na tela"""
        # Corpo
        pygame.draw.rect(surface, (150, 0, 0), (self.x, self.y, self.width, self.height))
        
        # Barra de HP
        barra_width = self.width
        barra_height = 5
        barra_x = self.x
        barra_y = self.y - 10
        
        pygame.draw.rect(surface, (50, 50, 50), (barra_x, barra_y, barra_width, barra_height))
        hp_percent = self.stats.hp / self.stats.hp_max
        pygame.draw.rect(surface, (0, 255, 0), (barra_x, barra_y, barra_width * hp_percent, barra_height))
        
        # Nome do boss
        font = pygame.font.Font(None, 20)
        nome_text = font.render(self.stats.nome, True, (255, 255, 255))
        surface.blit(nome_text, (self.x - 10, self.y - 30))


class Dragao(Boss):
    """Boss: Dragão"""
    
    def __init__(self, x: float, y: float):
        stats = BossStats(
            nome="Dragão",
            tipo=BossType.DRAGAO,
            hp=150,
            hp_max=150,
            velocidade=2,
            dano_ataque=15,
            intervalo_ataque=60,
            recompensa_moedas=5,
            dificuldade=3
        )
        super().__init__(x, y, stats)


class Cavaleiro(Boss):
    """Boss: Cavaleiro"""
    
    def __init__(self, x: float, y: float):
        stats = BossStats(
            nome="Cavaleiro",
            tipo=BossType.CAVALEIRO,
            hp=120,
            hp_max=120,
            velocidade=3,
            dano_ataque=12,
            intervalo_ataque=50,
            recompensa_moedas=4,
            dificuldade=2
        )
        super().__init__(x, y, stats)


class Mago(Boss):
    """Boss: Mago"""
    
    def __init__(self, x: float, y: float):
        stats = BossStats(
            nome="Mago",
            tipo=BossType.MAGO,
            hp=100,
            hp_max=100,
            velocidade=2,
            dano_ataque=18,
            intervalo_ataque=45,
            recompensa_moedas=5,
            dificuldade=4
        )
        super().__init__(x, y, stats)


class Bruxa(Boss):
    """Boss: Bruxa"""
    
    def __init__(self, x: float, y: float):
        stats = BossStats(
            nome="Bruxa",
            tipo=BossType.BRUXA,
            hp=110,
            hp_max=110,
            velocidade=2,
            dano_ataque=14,
            intervalo_ataque=55,
            recompensa_moedas=4,
            dificuldade=3
        )
        super().__init__(x, y, stats)


class Gigante(Boss):
    """Boss: Gigante"""
    
    def __init__(self, x: float, y: float):
        stats = BossStats(
            nome="Gigante",
            tipo=BossType.GIGANTE,
            hp=200,
            hp_max=200,
            velocidade=1,
            dano_ataque=20,
            intervalo_ataque=70,
            recompensa_moedas=6,
            dificuldade=5
        )
        super().__init__(x, y, stats)
        self.width = 80
        self.height = 120


class Princesa(Boss):
    """Boss: Princesa"""
    
    def __init__(self, x: float, y: float):
        stats = BossStats(
            nome="Princesa",
            tipo=BossType.PRINCESA,
            hp=90,
            hp_max=90,
            velocidade=3,
            dano_ataque=10,
            intervalo_ataque=40,
            recompensa_moedas=3,
            dificuldade=2
        )
        super().__init__(x, y, stats)


class Rei(Boss):
    """Boss: Rei"""
    
    def __init__(self, x: float, y: float):
        stats = BossStats(
            nome="Rei",
            tipo=BossType.REI,
            hp=160,
            hp_max=160,
            velocidade=2,
            dano_ataque=16,
            intervalo_ataque=50,
            recompensa_moedas=6,
            dificuldade=4
        )
        super().__init__(x, y, stats)


class LivroFinal(Boss):
    """Boss Final: O Livro"""
    
    def __init__(self, x: float, y: float):
        stats = BossStats(
            nome="O Livro - Boss Final",
            tipo=BossType.LIVRO_FINAL,
            hp=300,
            hp_max=300,
            velocidade=2,
            dano_ataque=25,
            intervalo_ataque=30,
            recompensa_moedas=20,
            dificuldade=10
        )
        super().__init__(x, y, stats)
        self.width = 70
        self.height = 100
        
    def desenhar(self, surface):
        """Desenha o Livro Final na tela"""
        # Livro (retângulo com formas)
        pygame.draw.rect(surface, (101, 67, 33), (self.x, self.y, self.width, self.height))
        
        # Páginas
        pygame.draw.line(surface, (200, 200, 150), 
                        (self.x + self.width//2, self.y),
                        (self.x + self.width//2, self.y + self.height), 2)
        
        # Barra de HP
        barra_width = self.width
        barra_height = 5
        barra_x = self.x
        barra_y = self.y - 10
        
        pygame.draw.rect(surface, (50, 50, 50), (barra_x, barra_y, barra_width, barra_height))
        hp_percent = self.stats.hp / self.stats.hp_max
        pygame.draw.rect(surface, (255, 0, 0), (barra_x, barra_y, barra_width * hp_percent, barra_height))
        
        # Nome do boss
        font = pygame.font.Font(None, 20)
        nome_text = font.render(self.stats.nome, True, (255, 215, 0))
        surface.blit(nome_text, (self.x - 30, self.y - 30))


def criar_boss(tipo: BossType, x: float, y: float) -> Boss:
    """Factory para criar bosses"""
    bosses_map = {
        BossType.DRAGAO: Dragao,
        BossType.CAVALEIRO: Cavaleiro,
        BossType.MAGO: Mago,
        BossType.BRUXA: Bruxa,
        BossType.GIGANTE: Gigante,
        BossType.PRINCESA: Princesa,
        BossType.REI: Rei,
        BossType.LIVRO_FINAL: LivroFinal,
    }
    
    boss_class = bosses_map.get(tipo)
    if boss_class:
        return boss_class(x, y)
    return None
