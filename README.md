# Areninha 3D - Projeto de Computação Gráfica

Este projeto renderiza uma cena 3D de uma "Areninha" de futebol, baseada em um local real, utilizando Python e OpenGL. O objetivo é aplicar conceitos fundamentais de Computação Gráfica.

## Dependências
Para executar o projeto, você precisa instalar as seguintes bibliotecas:

```bash
pip install PyOpenGL PyOpenGL_accelerate glfw numpy Pillow

Como Executar
Certifique-se de que todas as dependências estão instaladas.

Coloque as imagens de textura necessárias na pasta /imgs.

Execute o arquivo principal:

Bash

python main.py
Controles
W, A, S, D: Mover a câmera para frente, esquerda, trás e direita.

Mouse: Olhar ao redor.

Estrutura do Projeto
O projeto segue uma arquitetura Orientada a Objetos para máxima organização e extensibilidade.

main.py: Ponto de entrada que instancia e executa a aplicação.

/src/app.py: Classe principal que gerencia a janela, o laço de renderização e os componentes.

/src/scene.py: Compõe a cena inteira, gerenciando e desenhando todos os objetos.

/src/objects/: Contém uma classe para cada objeto 3D da cena (Campo, Trave, Bola, etc.).

/src/assets/: Contém utilitários para carregar texturas e desenhar formas primitivas.

