import pygame
import sys
import random
import math

# Inicialização do Pygame
pygame.init()

# Configurações da tela
largura_tela, altura_tela = 800, 600
tela = pygame.display.set_mode((largura_tela, altura_tela))

# Cores
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
BRANCO = (255, 255, 255)

# Definindo o título da janela
pygame.display.set_caption('Jogo do Quadrado Azul')

# Definindo o quadrado azul e a barra verde
quadrado = pygame.Rect(100, altura_tela - 150, 50, 50)
barra = pygame.Rect(150, altura_tela - 100, 200, 20)

# Velocidade de movimento e de pulo
velocidade = 5
velocidade_pulo = -18
gravidade = 1

# Estado do pulo
pulando = False
velocidade_y = 0

# Posição da câmera
posicao_camera_x = 0

# Lista de plataformas
plataformas = [barra]

# Função para gerar plataformas aleatórias
def gerar_plataforma(posicao_x):
    altura_maxima_pulo = abs(velocidade_pulo) ** 2 / (2 * gravidade)
    altura_maxima_plataforma = random.randint(20, altura_maxima_pulo * 0.85)
    return pygame.Rect(posicao_x, random.randint(100, altura_tela - altura_maxima_plataforma - 50), 200, altura_maxima_plataforma)

# Loop do jogo
rodando = True
while rodando:
    # Verificando os eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and not pulando:
                pulando = True
                velocidade_y = velocidade_pulo

    # Aplicando gravidade
    if pulando:
        quadrado.y += velocidade_y
        velocidade_y += gravidade

    # Verificar colisão com as plataformas
    for plataforma in plataformas:
        if quadrado.colliderect(plataforma) and velocidade_y >= 0.02:
            pulando = False
            velocidade_y = 0
            quadrado.bottom = plataforma.top
            break
    else:
        if quadrado.bottom >= altura_tela:
            pulando = False
            velocidade_y = 0
            quadrado.bottom = altura_tela

    # Movimentação horizontal
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        quadrado.x -= velocidade
    if teclas[pygame.K_RIGHT]:
        quadrado.x += velocidade

    # Ajustar a posição da câmera para centrar o jogador
    posicao_camera_x = quadrado.centerx - largura_tela // 2

    # Gerar novas plataformas conforme necessário
    while plataformas[-1].right - posicao_camera_x < largura_tela:
        nova_posicao_x = plataformas[-1].right + int(random.randint(200, 400) * 0.9)  # Diminuindo em 10%
        nova_plataforma = gerar_plataforma(nova_posicao_x)
        plataformas.append(nova_plataforma)

    # Remover plataformas que estão fora da tela
    plataformas = [plataforma for plataforma in plataformas if plataforma.right - posicao_camera_x > 0]

    # Preenchendo o fundo
    tela.fill(BRANCO)

    # Desenhando as plataformas (ajustando pela posição da câmera)
    for plataforma in plataformas:
        pygame.draw.rect(tela, VERDE, plataforma.move(-posicao_camera_x, 0))

    # Desenhando o quadrado (ajustando pela posição da câmera)
    pygame.draw.rect(tela, AZUL, quadrado.move(-posicao_camera_x, 0))

    # Atualizando a tela
    pygame.display.flip()

    # Limitando a 60 FPS
    pygame.time.Clock().tick(60)

# Encerrando o Pygame
pygame.quit()
sys.exit()
