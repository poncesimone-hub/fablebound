"""
Sistema de Relíquias para o jogo Laura
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class TipoReliquia(Enum):
    """Tipos de relíquias disponíveis"""
    VIDA = "Vida"
    VELOCIDADE = "Velocidade"
    RAPIDEZ_ESPECIAL = "Rapidez do Especial"


@dataclass
class Reliquia:
    """Classe para representar uma relíquia"""
    tipo: TipoReliquia
    nome: str
    descricao: str
    efeito: int  # quantidade de aumento
    custo: int = 2
    adquirida: bool = False
    
    def ativar(self, player_stats) -> None:
        """Ativa o efeito da relíquia no jogador"""
        if self.tipo == TipoReliquia.VIDA:
            player_stats.hp_max += self.efeito
            player_stats.hp = player_stats.hp_max
        elif self.tipo == TipoReliquia.VELOCIDADE:
            player_stats.velocidade += self.efeito
        elif self.tipo == TipoReliquia.RAPIDEZ_ESPECIAL:
            player_stats.rapidez_especial += self.efeito


class Loja:
    """Sistema de loja para compra de itens"""
    
    def __init__(self):
        self.reliquias = [
            Reliquia(
                tipo=TipoReliquia.VIDA,
                nome="Cristal da Vida",
                descricao="Aumenta HP máximo em 30",
                efeito=30,
                custo=2
            ),
            Reliquia(
                tipo=TipoReliquia.VELOCIDADE,
                nome="Talismã da Rapidez",
                descricao="Aumenta velocidade de movimento em 2",
                efeito=2,
                custo=2
            ),
            Reliquia(
                tipo=TipoReliquia.RAPIDEZ_ESPECIAL,
                nome="Orbe do Poder",
                descricao="Aumenta velocidade de carregamento do especial",
                efeito=5,
                custo=2
            )
        ]
        
        self.vendedor = {
            'nome': 'Quill',
            'descricao': 'Vendedor mistério da ilha',
            'aparencia': 'Barba, óculos, chapéu de mago costurado'
        }
        
    def comprar_reliquia(self, player_stats, indice_reliquia: int) -> bool:
        """Compra uma relíquia se o jogador tiver moedas suficientes"""
        if indice_reliquia < 0 or indice_reliquia >= len(self.reliquias):
            return False
            
        reliquia = self.reliquias[indice_reliquia]
        
        if reliquia.adquirida:
            return False
            
        if player_stats.moedas >= reliquia.custo:
            player_stats.moedas -= reliquia.custo
            reliquia.ativar(player_stats)
            reliquia.adquirida = True
            return True
            
        return False
        
    def comprar_tiro(self, player_stats, tipo_magia: str) -> bool:
        """Compra um novo tipo de magia se o jogador tiver moedas suficientes"""
        custo = 3
        
        if player_stats.moedas < custo:
            return False
            
        if tipo_magia == "RAIO":
            player_stats.tiros_raio += 10
        elif tipo_magia == "GELO":
            player_stats.tiros_gelo += 10
        elif tipo_magia == "FOGO":
            player_stats.tiros_fogo += 10
        else:
            return False
            
        player_stats.moedas -= custo
        return True
        
    def listar_reliquias_disponiveis(self):
        """Lista relíquias ainda não adquiridas"""
        return [r for r in self.reliquias if not r.adquirida]
        
    def listar_reliquias_adquiridas(self):
        """Lista relíquias já adquiridas"""
        return [r for r in self.reliquias if r.adquirida]
        
    def info_vendedor(self) -> dict:
        """Retorna informações do vendedor Quill"""
        return self.vendedor
