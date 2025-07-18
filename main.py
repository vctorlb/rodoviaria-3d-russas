import sys
import os

# Adiciona o diretório 'src' ao path para que os módulos possam ser encontrados
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from app import App

if __name__ == "__main__":
    try:
        areninha_app = App(width=1920, height=1080)
        areninha_app.run()
    except Exception as e:
        print(f"Ocorreu um erro ao executar a aplicação: {e}")