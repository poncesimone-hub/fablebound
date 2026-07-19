"""
Laura - A Maga do Conto de Fadas
Um jogo run-and-gun com sistema de magia e relíquias
"""

import pygame
import sys
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

# Inicializar Pygame
pygame.init()

# Constantes de Tela
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
DARK_BLUE = (25, 50, 100)

# Configuração da Tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Laura - A Maga do Conto de Fadas")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)


class MagiaType(Enum):
    """Tipos de magia disponíveis"""
    RAIO = "Raio"
    GELO = "Gelo"
    FOGO = "Fogo"


class SuperAtaque(Enum):
    """Super ataques disponíveis"""
    GRANDE_RAIO = "Grande Raio"
    GELEIRA = "Geleira"
    RAIO_FOGO = "Raio de Fogo"


class Fase(Enum):
    """Fases do jogo"""
    FLORESTA_TERROR = "Floresta do Terror"
    BIBLIOTECA = "Biblioteca"
    COLISEU = "Coliseu"


@dataclass
class Reliquia:
    """Classe para representar uma relíquia"""
    nome: str
    efeito: str
    custo: int = 2
    adquirida: bool = False


@dataclass
class PlayerStats:
    """Estatísticas do jogador"""
    hp: int
    hp_max: int
    velocidade: int
    rapidez_especial: int
    moedas: int
    tiros_raio: int
    tiros_gelo: int
    tiros_fogo: int
    barra_especial: float  # 0 a 100
    magia_atual: MagiaType


class Laura:
    """Classe principal do personagem Laura"""
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.velocidade_base = 5
        self.velocidade_pulo = 12
        self.pode_pular_duplo = True
        self.em_ar = False
        self.velocidade_y = 0
        self.gravidade = 0.5
        
        # Stats
        self.stats = PlayerStats(
            hp=100,
            hp_max=100,
            velocidade=self.velocidade_base,
            rapidez_especial=1,
            moedas=0,
            tiros_raio=30,  # Começa apenas com raio
            tiros_gelo=0,
            tiros_fogo=0,
            barra_especial=0.0,
            magia_atual=MagiaType.RAIO
        )
        
        # Movimento
        self.vx = 0
        self.vy = 0
        
    def atualizar(self, teclas):
        """Atualiza o estado do personagem"""
        # Movimento horizontal
        self.vx = 0
        if teclas[pygame.K_a]:
            self.vx = -self.stats.velocidade
        if teclas[pygame.K_d]:
            self.vx = self.stats.velocidade
            
        # Pulo
        if teclas[pygame.K_SPACE] and not self.em_ar:
            self.vy = -self.velocidade_pulo
            self.em_ar = True
            self.pode_pular_duplo = True
        elif teclas[pygame.K_SPACE] and self.pode_pular_duplo and self.em_ar:
            self.vy = -self.velocidade_pulo
            self.pode_pular_duplo = False
            
        # Dash (Shift)
        if teclas[pygame.K_LSHIFT]:
            self.vx *= 2
            
        # Atualizar posição
        self.x += self.vx
        self.y += self.vy
        
        # Aplicar gravidade
        self.vy += self.gravidade
        
        # Verificar colisão com chão
        if self.y >= SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height
            self.em_ar = False
            self.vy = 0
            
        # Limites da tela horizontal
        if self.x < 0:
            self.x = 0
        if self.x + self.width > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width
            
    def atirar(self) -> Optional[dict]:
        """Gera um tiro baseado na magia atual"""
        magia = self.stats.magia_atual
        
        if magia == MagiaType.RAIO and self.stats.tiros_raio > 0:
            self.stats.tiros_raio -= 1
            self.stats.barra_especial = min(100, self.stats.barra_especial + (100/30))
            return {
                'tipo': MagiaType.RAIO,
                'x': self.x + self.width,
                'y': self.y + self.height // 2,
                'velocidade': 8,
                'dano': 10
            }
        elif magia == MagiaType.GELO and self.stats.tiros_gelo > 0:
            self.stats.tiros_gelo -= 1
            self.stats.barra_especial = min(100, self.stats.barra_especial + (100/30))
            return {
                'tipo': MagiaType.GELO,
                'x': self.x + self.width,
                'y': self.y + self.height // 2,
                'velocidade': 6,
                'dano': 8
            }
        elif magia == MagiaType.FOGO and self.stats.tiros_fogo > 0:
            self.stats.tiros_fogo -= 1
            self.stats.barra_especial = min(100, self.stats.barra_especial + (100/30))
            return {
                'tipo': MagiaType.FOGO,
                'x': self.x + self.width,
                'y': self.y + self.height // 2,
                'velocidade': 7,
                'dano': 12
            }
        return None
        
    def desenhar(self, surface):
        """Desenha Laura na tela"""
        # Corpo (capa vermelha)
        pygame.draw.rect(surface, (200, 0, 0), (self.x, self.y, self.width, self.height))
        
        # Cabeça
        pygame.draw.circle(surface, (255, 200, 150), (self.x + self.width//2, self.y - 10), 8)
        
        # Varinha (preta com ponta branca)
        pygame.draw.line(surface, BLACK, (self.x + self.width, self.y + 15), 
                        (self.x + self.width + 30, self.y + 15), 3)
        pygame.draw.circle(surface, WHITE, (self.x + self.width + 30, self.y + 15), 4)


class Jogo:
    """Classe principal do jogo"""
    
    def __init__(self):
        self.laura = Laura(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.tiros = []
        self.bosses = []
        self.moedas_coletadas = 0
        self.fase_atual = Fase.FLORESTA_TERROR
        self.running = True
        self.ticks_desde_tiro = 0
        self.ticks_entre_tiros = 10  # Frame rate entre tiros
        
    def processar_eventos(self):
        """Processa eventos do jogo"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_1:
                    self.laura.stats.magia_atual = MagiaType.RAIO
                if event.key == pygame.K_2:
                    self.laura.stats.magia_atual = MagiaType.GELO
                if event.key == pygame.K_3:
                    self.laura.stats.magia_atual = MagiaType.FOGO
                    
    def atualizar(self):
        """Atualiza a lógica do jogo"""
        teclas = pygame.key.get_pressed()
        
        # Atualizar Laura
        self.laura.atualizar(teclas)
        
        # Sistema de tiro automático
        if teclas[pygame.K_UP]:
            self.ticks_desde_tiro += 1
            if self.ticks_desde_tiro >= self.ticks_entre_tiros:
                tiro = self.laura.atirar()
                if tiro:
                    self.tiros.append(tiro)
                self.ticks_desde_tiro = 0
        else:
            self.ticks_desde_tiro = 0
            
        # Atualizar tiros
        self.tiros = [t for t in self.tiros if t['x'] < SCREEN_WIDTH]
        for tiro in self.tiros:
            tiro['x'] += tiro['velocidade']
            
    def desenhar(self):
        """Desenha todos os elementos do jogo"""
        screen.fill((135, 206, 235))  # Céu azul
        
        # Desenhar chão
        pygame.draw.rect(screen, (34, 139, 34), (0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20))
        
        # Desenhar Laura
        self.laura.desenhar(screen)
        
        # Desenhar tiros
        for tiro in self.tiros:
            cor = (255, 215, 0) if tiro['tipo'] == MagiaType.RAIO else \
                  (173, 216, 230) if tiro['tipo'] == MagiaType.GELO else \
                  (255, 165, 0)
            pygame.draw.circle(screen, cor, (int(tiro['x']), int(tiro['y'])), 5)
            
        # Interface UI
        self.desenhar_ui()
        
        pygame.display.flip()
        
    def desenhar_ui(self):
        """Desenha a interface do usuário"""
        # HP
        hp_text = font.render(f"HP: {self.laura.stats.hp}/{self.laura.stats.hp_max}", True, WHITE)
        screen.blit(hp_text, (10, 10))
        
        # Moedas
        moedas_text = font.render(f"Moedas: {self.laura.stats.moedas}", True, GOLD)
        screen.blit(moedas_text, (10, 50))
        
        # Magia Atual
        magia_text = small_font.render(f"Magia: {self.laura.stats.magia_atual.value}", True, WHITE)
        screen.blit(magia_text, (10, 90))
        
        # Tiros Disponíveis
        tiros_text = small_font.render(
            f"Raio: {self.laura.stats.tiros_raio} | Gelo: {self.laura.stats.tiros_gelo} | Fogo: {self.laura.stats.tiros_fogo}",
            True, WHITE
        )
        screen.blit(tiros_text, (10, 120))
        
        # Barra de Especial (Estrela Dourada)
        barra_x, barra_y = 10, 160
        barra_width = 150
        pygame.draw.rect(screen, (100, 100, 100), (barra_x, barra_y, barra_width, 20))
        pygame.draw.rect(screen, GOLD, (barra_x, barra_y, int(barra_width * self.laura.stats.barra_especial / 100), 20))
        especial_text = small_font.render(f"★ {self.laura.stats.barra_especial:.0f}%", True, GOLD)
        screen.blit(especial_text, (barra_x + barra_width + 10, barra_y + 2))
        
        # Instruções
        instrucoes_text = small_font.render("A/D: Mover | SPACE: Pular | SHIFT: Dash | UP: Atirar | 1/2/3: Magia", True, WHITE)
        screen.blit(instrucoes_text, (10, SCREEN_HEIGHT - 30))
        
        # Fase atual
        fase_text = small_font.render(f"Fase: {self.fase_atual.value}", True, WHITE)
        screen.blit(fase_text, (SCREEN_WIDTH - 300, 10))
        
    def executar(self):
        """Loop principal do jogo"""
        while self.running:
            self.processar_eventos()
            self.atualizar()
            self.desenhar()
            clock.tick(FPS)
            
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    jogo = Jogo()
    jogo.executar()
