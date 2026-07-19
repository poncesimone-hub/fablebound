#!/usr/bin/env python3
"""
Instalador Automático para Replit
Execute este arquivo para configurar tudo automaticamente
"""

import subprocess
import sys
import os

def instalar_dependencias():
    """Instala as dependências do projeto"""
    print("📦 Instalando dependências...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("✅ Dependências instaladas!")

def verificar_estrutura():
    """Verifica se todos os arquivos estão no lugar"""
    print("\n🔍 Verificando estrutura de arquivos...")
    arquivos_necessarios = [
        "src/main.py",
        "src/bosses.py",
        "src/reliquias.py",
        "src/fases.py",
        "src/inimigos.py",
        "requirements.txt"
    ]
    
    arquivos_faltando = []
    for arquivo in arquivos_necessarios:
        if not os.path.exists(arquivo):
            arquivos_faltando.append(arquivo)
    
    if arquivos_faltando:
        print("❌ Arquivos faltando:")
        for arquivo in arquivos_faltando:
            print(f"  - {arquivo}")
        return False
    else:
        print("✅ Todos os arquivos estão presentes!")
        return True

def main():
    print("""\n
╔════════════════════════════════════════════╗
║  Laura - A Maga do Conto de Fadas        ║
║  Instalador Automático para Replit       ║
╚════════════════════════════════════════════╝
""")
    
    # Verificar estrutura
    if not verificar_estrutura():
        print("\n⚠️  Por favor, certifique-se de que todos os arquivos estão no repositório.")
        sys.exit(1)
    
    # Instalar dependências
    try:
        instalar_dependencias()
    except Exception as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        sys.exit(1)
    
    print("\n" + "="*50)
    print("🎮 Tudo pronto! Digite o comando abaixo para jogar:")
    print("="*50)
    print("\npython src/main.py\n")
    print("="*50)

if __name__ == "__main__":
    main()
