"""
Sistema de Fases para o jogo Laura
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Optional


class FaseType(Enum):
    """Tipos de fases disponíveis"""
    FLORESTA_TERROR = "Floresta do Terror"
    BIBLIOTECA = "Biblioteca"
    COLISEU = "Coliseu"


@dataclass
class Fase:
    """Classe para representar uma fase"""
    nome: str
    tipo: FaseType
    numero: int
    moedas_bonus: int = 5
    dificuldade: int = 1
    background_cor: tuple = (0, 100, 0)  # RGB
    bosses_sequencia: List[str] = None
    
    def __post_init__(self):
        if self.bosses_sequencia is None:
            self.bosses_sequencia = []


class GerenciadorFases:
    """Gerenciador de progressão de fases"""
    
    def __init__(self):
        self.fases = [
            Fase(
                nome="Floresta do Terror",
                tipo=FaseType.FLORESTA_TERROR,
                numero=1,
                moedas_bonus=5,
                dificuldade=1,
                background_cor=(34, 139, 34),
                bosses_sequencia=["DRAGAO", "CAVALEIRO", "MAGO"]
            ),
            Fase(
                nome="Biblioteca",
                tipo=FaseType.BIBLIOTECA,
                numero=2,
                moedas_bonus=5,
                dificuldade=2,
                background_cor=(139, 69, 19),
                bosses_sequencia=["BRUXA", "GIGANTE", "PRINCESA"]
            ),
            Fase(
                nome="Coliseu",
                tipo=FaseType.COLISEU,
                numero=3,
                moedas_bonus=5,
                dificuldade=3,
                background_cor=(128, 128, 128),
                bosses_sequencia=["REI", "LIVRO_FINAL"]
            )
        ]
        self.fase_atual = 0
        
    def get_fase_atual(self) -> Fase:
        """Retorna a fase atual"""
        if self.fase_atual < len(self.fases):
            return self.fases[self.fase_atual]
        return None
        
    def proxima_fase(self) -> bool:
        """Avança para a próxima fase"""
        if self.fase_atual < len(self.fases) - 1:
            self.fase_atual += 1
            return True
        return False
        
    def completou_todas_fases(self) -> bool:
        """Verifica se todas as fases foram completadas"""
        return self.fase_atual >= len(self.fases) - 1
        
    def reset_fases(self):
        """Reseta o progresso de fases"""
        self.fase_atual = 0
