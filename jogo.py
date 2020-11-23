import os
import sys

import pygame
from pygame import mixer, KEYDOWN, K_LEFT, K_RIGHT, KEYUP


# Definição das cores em RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (106, 159, 181)
TOMATO = (255, 99, 71)
YELLOW = (255, 255, 0)


# Inicialização do pygame
pygame.init()


# Inicialização da módulo Mixer
mixer.init()


# Definição do tamanho da tela do Pygame
screen = pygame.display.set_mode((800, 600))


# Objetos utilizados na classe InputBox
cor_inativa = pygame.Color('SteelBlue')
cor_ativa = pygame.Color('Blue')
fonte = pygame.font.Font(None, 32)


# Classe utilizada para criação dos InputBoxes
class InputBox:

    def __init__(self, x, y, w, h, texto=''):
        self.retangulo = pygame.Rect(x, y, w, h)
        self.cor = cor_inativa
        self.texto = texto
        self.texto_surface = fonte.render(texto, True, self.cor)
        self.ativo = False

    def eventoInputBox(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.retangulo.collidepoint(evento.pos):
                self.ativo = not self.ativo
            else:
                self.ativo = False
            self.cor = cor_ativa if self.ativo else cor_inativa
        if evento.type == pygame.KEYDOWN:
            if self.ativo:
                if evento.key == pygame.K_RETURN:
                    print(self.texto)
                    self.texto = ''
                elif evento.key == pygame.K_BACKSPACE:
                    self.texto = self.texto[:-1]
                else:
                    self.texto += evento.unicode
                self.texto_surface = fonte.render(self.texto, True, self.cor)

    def atualizarInputBox(self):
        width = max(200, self.texto_surface.get_width() + 10)
        self.retangulo.w = width

    def desenharInputBox(self, screen):
        screen.blit(self.texto_surface, (self.retangulo.x + 5, self.retangulo.y + 5))
        pygame.draw.rect(screen, self.cor, self.retangulo, 2)


# Classe utilizada para criação dos CheckBoxes
class Checkbox:

    def __init__(self, surface, x, y, color=(230, 230, 230), caption="", outline_color=(0, 0, 0),
                 check_color=(0, 0, 0), font_size=50, font_color=(0, 0, 0), text_offset=(28, 1), placar=0):
        self.surface = surface
        self.x = x
        self.y = y
        self.color = color
        self.caption = caption
        self.oc = outline_color
        self.cc = check_color
        self.fs = font_size
        self.fc = font_color
        self.to = text_offset

        self.checkbox_obj = pygame.Rect(self.x, self.y, 35, 35)
        self.checkbox_outline = self.checkbox_obj.copy()

        self.checked = False
        self.active = False
        self.unchecked = True
        self.click = False
        self.placar = placar

    def _draw_button_text(self):
        self.font = pygame.font.Font(None, self.fs)
        self.font_surf = self.font.render(self.caption, True, self.fc)
        w, h = self.font.size(self.caption)
        self.font_pos = (self.x + 35 / 2 - w / 2 + self.to[0], self.y + 35 / 2 - h / 2 + self.to[1])
        self.surface.blit(self.font_surf, self.font_pos)

    def render_checkbox(self):
        if self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
            pygame.draw.circle(self.surface, self.cc, (self.x + 17, self.y + 17), 10)
        elif self.unchecked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
            self.checked = False
        self._draw_button_text()

    def _update(self, event_object):
        x, y = event_object.pos
        px, py, w, h = self.checkbox_obj
        if px < x < px + w and py < y < py + h:
            self.active = True
        else:
            self.active = False

    def _mouse_up(self):
        if self.active and not self.checked and self.click:
            self.placar = self.placar + 1
            self.checked = True
        elif self.active and self.checked and self.click:
            self.placar = self.placar - 1
            self.checked = False
            self.unchecked = True

    def update_checkbox(self, event_object):
        if event_object.type == pygame.MOUSEBUTTONDOWN:
            self.click = True
        if event_object.type == pygame.MOUSEBUTTONUP:
            self._mouse_up()
        if event_object.type == pygame.MOUSEMOTION:
            self._update(event_object)

    def is_checked(self):
        self.x += 1
        self.y += 1

        if self.x > 450:
            self.x -= 450

        if self.y > 450:
            self.y -= 450

        return self.checked

    def is_unchecked(self):
        if self.checked is False:
            return True
        else:
            return False

# -------------------------------------------Funções----------------------------------------------------------------

# Função para criar um novo retângulo
def criarRetangulo(text, rect, inactive_color, active_color, action):
    font = pygame.font.Font("./Assets/Fonts/Bungee-Regular.ttf", 25, bold=True)

    button_rect = pygame.Rect(rect)

    text = font.render(text, True, WHITE)
    text_rect = text.get_rect(center=button_rect.center)

    return [text, text_rect, button_rect, inactive_color, active_color, action, False]


# Função para checar o evento, de quando o mouse estiver em cima do botão ou não
def checarEventoBotao(info, event):
    text, text_rect, rect, inactive_color, active_color, action, hover = info

    if event.type == pygame.MOUSEMOTION:
        info[-1] = rect.collidepoint(event.pos)

    elif event.type == pygame.MOUSEBUTTONDOWN:
        if hover and action:
            action()


# Função para desenhar o botão na tela
def botao(screen, info):
    text, text_rect, rect, inactive_color, active_color, action, hover = info

    if hover:
        color = active_color
    else:
        color = inactive_color

    pygame.draw.rect(screen, color, rect)
    screen.blit(text, text_rect)


# Função do botão Jogar redirecionando para 1º tela
def clicarJogar():
    global estado
    estado = 'jogo'


# Legenda Jogo que aparece na 1º tela
def legendaJogo():
    global estado
    estado = 'legendaJogo'


# Legenda Avatar que aparece na 2º tela
def legendaAvatar():
    global estado
    estado = 'legendaAvatar'


# Legenda Tarefas que aparece na 3º tela
def legendaTarefas():
    global estado
    estado = 'legendaTarefas'


# Legenda Tarefas que aparece na tela de gameover
def legendaGameOver():
    global estado
    estado = 'legendaGameOver'


# Função da tela de Game Over, caso o jogador não consiga completar os objetivos diários
def gameover():
    global estado
    estado = 'gameover'

    fontTituloGameOver = criarRetangulo("GAME OVER", (300, 250, 200, 75), BLUE, BLUE, legendaGameOver)
    fontTituloGameOver2 = criarRetangulo("Você não concluiu as atividades diárias", (300, 300, 200, 75), BLUE, BLUE,
                                         legendaGameOver)
    fontTituloGameOver3 = criarRetangulo("Insista, persista e mais importante NUNCA DESISTA", (300, 400, 200, 75), BLUE,
                                         BLUE, legendaGameOver)
    botaoEncerrar = criarRetangulo("Sair", (300, 500, 200, 75), TOMATO, TOMATO, clicarSair)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                sys.exit()

            checarEventoBotao(botaoEncerrar, evento)

        screen.fill(BLUE)

        botao(screen, fontTituloGameOver)
        botao(screen, fontTituloGameOver2)
        botao(screen, fontTituloGameOver3)
        botao(screen, botaoEncerrar)

        screen.blit(pegarImagem('.\Assets\Images\logo.png'), (300, 40))

        pygame.display.update()


# Função da continuação do jogo, caso o jogador consiga completar todas as atividades diárias
def telaSegundoNivel():
    global estado
    estado = 'telaSegundoNivel'

    fontTituloNivel = criarRetangulo("PARABÉNS, desbloqueou o nível 2", (300, 250, 200, 75), BLUE, BLUE, legendaGameOver)
    fontTituloNivel2 = criarRetangulo("Você concluiu as atividades diárias", (300, 300, 200, 75), BLUE, BLUE,
                                         legendaGameOver)
    fontTituloNivel3 = criarRetangulo("Continue assim a não procrastinar", (300, 400, 200, 75), BLUE,
                                         BLUE, legendaGameOver)
    botaoSegundoNivel = criarRetangulo("Continuar", (300, 500, 200, 75), TOMATO, TOMATO, clicarProximoTarefas)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                clicarProximoTarefasNivel2()

        screen.fill(BLUE)

        botao(screen, fontTituloNivel)
        botao(screen, fontTituloNivel2)
        botao(screen, fontTituloNivel3)
        botao(screen, botaoSegundoNivel)

        screen.blit(pegarImagem('.\Assets\Images\logo.png'), (300, 40))

        pygame.display.update()


# Função da continuação do jogo, caso o jogador consiga completar todas as atividades diárias do nível 2
def telaTerceiroNivel():
    global estado
    estado = 'telaTerceiroNivel'

    fontTituloNivel = criarRetangulo("PARABÉNS, desbloqueou o nível 3", (300, 250, 200, 75), BLUE, BLUE, legendaGameOver)
    fontTituloNivel2 = criarRetangulo("Você concluiu as atividades diárias", (300, 300, 200, 75), BLUE, BLUE,
                                         legendaGameOver)
    fontTituloNivel3 = criarRetangulo("Continue assim a não procrastinar", (300, 400, 200, 75), BLUE,
                                         BLUE, legendaGameOver)
    botaoTerceiroNivel = criarRetangulo("Continuar", (300, 500, 200, 75), TOMATO, TOMATO, clicarProximoTarefas)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                clicarProximoTarefasNivel3()

        screen.fill(BLUE)

        botao(screen, fontTituloNivel)
        botao(screen, fontTituloNivel2)
        botao(screen, fontTituloNivel3)
        botao(screen, botaoTerceiroNivel)

        screen.blit(pegarImagem('.\Assets\Images\logo.png'), (300, 40))

        pygame.display.update()


# Função da continuação do jogo, caso o jogador consiga completar todas as atividades diárias - FEMININO
def telaSegundoNivelFeminino():
    global estado
    estado = 'telaSegundoNivel'

    fontTituloNivel = criarRetangulo("PARABÉNS, desbloqueou o nível 2", (300, 250, 200, 75), BLUE, BLUE, legendaGameOver)
    fontTituloNivel2 = criarRetangulo("Você concluiu as atividades diárias", (300, 300, 200, 75), BLUE, BLUE,
                                         legendaGameOver)
    fontTituloNivel3 = criarRetangulo("Continue assim a não procrastinar", (300, 400, 200, 75), BLUE,
                                         BLUE, legendaGameOver)
    botaoSegundoNivel = criarRetangulo("Continuar", (300, 500, 200, 75), TOMATO, TOMATO, clicarProximoTarefas)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                clicarProximoTarefasNivel2Feminino()

        screen.fill(BLUE)

        botao(screen, fontTituloNivel)
        botao(screen, fontTituloNivel2)
        botao(screen, fontTituloNivel3)
        botao(screen, botaoSegundoNivel)

        screen.blit(pegarImagem('.\Assets\Images\logo.png'), (300, 40))

        pygame.display.update()


# Função da continuação do jogo, caso o jogador consiga completar todas as atividades diárias do nível 2 - FEMININO
def telaTerceiroNivelFeminino():
    global estado
    estado = 'telaTerceiroNivelFeminino'

    fontTituloNivel = criarRetangulo("PARABÉNS, desbloqueou o nível 3", (300, 250, 200, 75), BLUE, BLUE, legendaGameOver)
    fontTituloNivel2 = criarRetangulo("Você concluiu as atividades diárias", (300, 300, 200, 75), BLUE, BLUE,
                                         legendaGameOver)
    fontTituloNivel3 = criarRetangulo("Continue assim a não procrastinar", (300, 400, 200, 75), BLUE,
                                         BLUE, legendaGameOver)
    botaoTerceiroNivel = criarRetangulo("Continuar", (300, 500, 200, 75), TOMATO, TOMATO, clicarProximoTarefas)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                clicarProximoTarefasNivel3Feminino()

        screen.fill(BLUE)

        botao(screen, fontTituloNivel)
        botao(screen, fontTituloNivel2)
        botao(screen, fontTituloNivel3)
        botao(screen, botaoTerceiroNivel)

        screen.blit(pegarImagem('.\Assets\Images\logo.png'), (300, 40))

        pygame.display.update()


# Ultima tela do jogo, caso o jogador consiga completar todas as atividades diárias do nível 3
def ultimaTela():
    global estado
    estado = 'ultimaTela'

    fontTituloNivel = criarRetangulo("PARABÉNS, concluiu todos os objetivos do jogo", (300, 250, 200, 75), BLUE, BLUE, legendaGameOver)
    fontTituloNivel2 = criarRetangulo("Você é mais forte do que imagina, Acredite", (300, 300, 200, 75), BLUE, BLUE,
                                         legendaGameOver)
    fontTituloNivel3 = criarRetangulo("Obrigado por jogar o Day to Day", (300, 400, 200, 75), BLUE,
                                         BLUE, legendaGameOver)
    botaoSair = criarRetangulo("Sair", (300, 500, 200, 75), TOMATO, TOMATO, clicarSair)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                sys.exit()

        screen.fill(BLUE)

        botao(screen, fontTituloNivel)
        botao(screen, fontTituloNivel2)
        botao(screen, fontTituloNivel3)
        botao(screen, botaoSair)

        screen.blit(pegarImagem('.\Assets\Images\logo.png'), (300, 40))

        pygame.display.update()


# Função criada, para definir o título, e legendas das tarefas/horários que aparecem na 4º tela
def tituloLegendasTarefas():
    fontTarefa1 = pygame.font.SysFont("./Assets/Fonts/Bungee-Regular.ttf", 30)
    tarefa1 = fontTarefa1.render("Tarefa 1", True, WHITE)

    fontTarefa2 = pygame.font.SysFont("./Assets/Fonts/Bungee-Regular.ttf", 30)
    tarefa2 = fontTarefa2.render("Tarefa 2", True, WHITE)

    fontTarefa3 = pygame.font.SysFont("./Assets/Fonts/Bungee-Regular.ttf", 30)
    tarefa3 = fontTarefa3.render("Tarefa 3", True, WHITE)

    cama = pygame.image.load("./Assets/Images/cama.png").convert()
    ganhou = pygame.image.load("./Assets/Images/ganhou.png").convert()

    screen.blit(cama, (10, 250))
    screen.blit(ganhou, (570, 300))

    screen.blit(pegarImagem('.\Assets\Images\logo.png'), (100, 40))

    screen.blit(tarefa1, (460, 30, 100, 10))
    screen.blit(tarefa2, (460, 100, 100, 10))
    screen.blit(tarefa3, (460, 170, 100, 10))


# Função criada, para definir o título, e legendas das tarefas/horários que aparecem na 4º tela - NÍVEL 2
def tituloLegendasTarefasNivel2():
    fontTarefa1 = pygame.font.SysFont("./Assets/Fonts/Bungee-Regular.ttf", 30)
    tarefa1 = fontTarefa1.render("Tarefa 1", True, WHITE)

    fontTarefa2 = pygame.font.SysFont("./Assets/Fonts/Bungee-Regular.ttf", 30)
    tarefa2 = fontTarefa2.render("Tarefa 2", True, WHITE)

    fontTarefa3 = pygame.font.SysFont("./Assets/Fonts/Bungee-Regular.ttf", 30)
    tarefa3 = fontTarefa3.render("Tarefa 3", True, WHITE)

    fontTarefa4 = pygame.font.SysFont("./Assets/Fonts/Bungee-Regular.ttf", 30)
    tarefa4 = fontTarefa4.render("Tarefa 4", True, WHITE)

    cama = pygame.image.load("./Assets/Images/cama.png").convert()
    screen.blit(cama, (10, 250))

    ganhou = pygame.image.load("./Assets/Images/ganhou.png").convert()
    screen.blit(ganhou, (570, 300))

    screen.blit(pegarImagem('.\Assets\Images\logo.png'), (100, 40))

    screen.blit(tarefa1, (460, 30, 100, 10))
    screen.blit(tarefa2, (460, 100, 100, 10))
    screen.blit(tarefa3, (460, 170, 100, 10))
    screen.blit(tarefa4, (460, 230, 100, 10))


# Função criada, para definir o título, e legendas das tarefas/horários que aparecem na 4º tela - NÍVEL 3
def tituloLegendasTarefasNivel3():
    fontTarefa1 = pygame.font.SysFont("./Assets/Fonts/Bungee-Regular.ttf", 30)
    tarefa1 = fontTarefa1.render("Tarefa 1", True, WHITE)

    fontTarefa2 = pygame.font.SysFont("./Assets/Fonts/Bungee-Regular.ttf", 30)
    tarefa2 = fontTarefa2.render("Tarefa 2", True, WHITE)

    fontTarefa3 = pygame.font.SysFont("./Assets/Fonts/Bungee-Regular.ttf", 30)
    tarefa3 = fontTarefa3.render("Tarefa 3", True, WHITE)

    fontTarefa4 = pygame.font.SysFont("./Assets/Fonts/Bungee-Regular.ttf", 30)
    tarefa4 = fontTarefa4.render("Tarefa 4", True, WHITE)

    fontTarefa5 = pygame.font.SysFont("./Assets/Fonts/Bungee-Regular.ttf", 30)
    tarefa5 = fontTarefa5.render("Tarefa 5", True, WHITE)

    cama = pygame.image.load("./Assets/Images/cama.png").convert()
    screen.blit(cama, (10, 250))

    ganhou = pygame.image.load("./Assets/Images/ganhou.png").convert()
    screen.blit(ganhou, (570, 300))

    screen.blit(pegarImagem('.\Assets\Images\logo.png'), (100, 40))

    screen.blit(tarefa2, (460, 30, 100, 10))
    screen.blit(tarefa3, (460, 100, 100, 10))
    screen.blit(tarefa4, (460, 170, 100, 10))
    screen.blit(tarefa5, (460, 230, 100, 10))
    screen.blit(tarefa1, (160, 230, 100, 10))


# Função criada, para definir o título, e legendas das tarefas/horários que aparecem na 4º tela - FEMININO
def tituloLegendasTarefasFeminino():
    fontTarefa1 = pygame.font.SysFont("./Assets/Fonts/Bungee-Regular.ttf", 30)
    tarefa1 = fontTarefa1.render("Tarefa 1", True, WHITE)

    fontTarefa2 = pygame.font.SysFont("./Assets/Fonts/Bungee-Regular.ttf", 30)
    tarefa2 = fontTarefa2.render("Tarefa 2", True, WHITE)

    fontTarefa3 = pygame.font.SysFont("./Assets/Fonts/Bungee-Regular.ttf", 30)
    tarefa3 = fontTarefa3.render("Tarefa 3", True, WHITE)

    cama = pygame.image.load("./Assets/Images/cama.png").convert()
    screen.blit(cama, (10, 250))

    ganhou = pygame.image.load("./Assets/Images/ganhou.png").convert()
    screen.blit(ganhou, (570, 300))

    screen.blit(pegarImagem('.\Assets\Images\logo.png'), (100, 40))

    screen.blit(tarefa1, (460, 30, 100, 10))
    screen.blit(tarefa2, (460, 100, 100, 10))
    screen.blit(tarefa3, (460, 170, 100, 10))


# Função criada, para definir o título, e legendas das tarefas/horários que aparecem na 4º tela - NÍVEL 2 FEMININO
def tituloLegendasTarefasNivel2Feminino():
    fontTarefa1 = pygame.font.SysFont("./Assets/Fonts/Bungee-Regular.ttf", 30)
    tarefa1 = fontTarefa1.render("Tarefa 1", True, WHITE)

    fontTarefa2 = pygame.font.SysFont("./Assets/Fonts/Bungee-Regular.ttf", 30)
    tarefa2 = fontTarefa2.render("Tarefa 2", True, WHITE)

    fontTarefa3 = pygame.font.SysFont("./Assets/Fonts/Bungee-Regular.ttf", 30)
    tarefa3 = fontTarefa3.render("Tarefa 3", True, WHITE)

    fontTarefa4 = pygame.font.SysFont("./Assets/Fonts/Bungee-Regular.ttf", 30)
    tarefa4 = fontTarefa4.render("Tarefa 4", True, WHITE)

    cama = pygame.image.load("./Assets/Images/cama.png").convert()
    screen.blit(cama, (10, 250))

    ganhou = pygame.image.load("./Assets/Images/ganhou.png").convert()
    screen.blit(ganhou, (570, 300))

    screen.blit(pegarImagem('.\Assets\Images\logo.png'), (100, 40))

    screen.blit(tarefa1, (460, 30, 100, 10))
    screen.blit(tarefa2, (460, 100, 100, 10))
    screen.blit(tarefa3, (460, 170, 100, 10))
    screen.blit(tarefa4, (460, 230, 100, 10))


# Função criada, para definir o título, e legendas das tarefas/horários que aparecem na 4º tela - NÍVEL 3 FEMININO
def tituloLegendasTarefasNivel3Feminino():
    fontTarefa1 = pygame.font.SysFont("./Assets/Fonts/Bungee-Regular.ttf", 30)
    tarefa1 = fontTarefa1.render("Tarefa 1", True, WHITE)

    fontTarefa2 = pygame.font.SysFont("./Assets/Fonts/Bungee-Regular.ttf", 30)
    tarefa2 = fontTarefa2.render("Tarefa 2", True, WHITE)

    fontTarefa3 = pygame.font.SysFont("./Assets/Fonts/Bungee-Regular.ttf", 30)
    tarefa3 = fontTarefa3.render("Tarefa 3", True, WHITE)

    fontTarefa4 = pygame.font.SysFont("./Assets/Fonts/Bungee-Regular.ttf", 30)
    tarefa4 = fontTarefa4.render("Tarefa 4", True, WHITE)

    fontTarefa5 = pygame.font.SysFont("./Assets/Fonts/Bungee-Regular.ttf", 30)
    tarefa5 = fontTarefa5.render("Tarefa 5", True, WHITE)

    cama = pygame.image.load("./Assets/Images/cama.png").convert()
    screen.blit(cama, (10, 250))

    ganhou = pygame.image.load("./Assets/Images/ganhou.png").convert()
    screen.blit(ganhou, (570, 300))

    screen.blit(pegarImagem('.\Assets\Images\logo.png'), (100, 40))

    screen.blit(tarefa2, (460, 30, 100, 10))
    screen.blit(tarefa3, (460, 100, 100, 10))
    screen.blit(tarefa4, (460, 170, 100, 10))
    screen.blit(tarefa5, (460, 230, 100, 10))
    screen.blit(tarefa1, (160, 230, 100, 10))


# Função do botão próximo (instruções), redirecionando para página Tarefas - NÍVEL 1
def clicarProximoTarefas():
    global estado
    estado = 'proximaTelaTarefas'

    clock = pygame.time.Clock()
    input_box1 = InputBox(400, 50, 140, 32)
    input_box2 = InputBox(400, 120, 140, 32)
    input_box3 = InputBox(400, 190, 140, 32)

    # Criando objeto Clock
    CLOCKTICK = pygame.USEREVENT + 1
    pygame.time.set_timer(CLOCKTICK, 36000)  # Configurado o timer do Pygame para execução a cada 1 segundo
    temporizador = 60

    cb1 = Checkbox(screen, 650, 45)
    cb2 = Checkbox(screen, 650, 120)
    cb3 = Checkbox(screen, 650, 190)

    input_boxes = [input_box1, input_box2, input_box3]

    masculino = pygame.image.load("./Assets/Images/homem.png").convert()

    # Declarando a fonte do placar e variável contadora
    font = pygame.font.SysFont('sans', 40)

    botaoNenhumaTarefa = criarRetangulo("Não concluí", (510, 485, 200, 75), BLUE, TOMATO, gameover)

    x, y = 300, 300
    move_x, move_y = 0, 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    move_x -= 1
                if event.key == K_RIGHT:
                    move_x += 1
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    move_x = 0

            # Capturando evendo de relogio e atualizando a variável contadora
            if event.type == CLOCKTICK:
                temporizador = temporizador - 1

            checarEventoBotao(botaoNenhumaTarefa, event)

            x += move_x
            y += move_y

            for box in input_boxes:
                box.eventoInputBox(event)

            cb1.update_checkbox(event)
            cb2.update_checkbox(event)
            cb3.update_checkbox(event)

        # Finalizando o jogo
        if temporizador == 0:
            gameover()

        # renderizando as fontes do placar na tela
        score1 = font.render('Placar ' + str(cb1.placar + cb2.placar + cb3.placar), True, (WHITE))
        screen.blit(score1, (300, 500))

        screen.blit(masculino, (x, y))
        botao(screen, botaoNenhumaTarefa)

        for box in input_boxes:
            box.atualizarInputBox()

        for box in input_boxes:
            box.desenharInputBox(screen)

        # renderizando as fontes do cronometro na tela do usuario
        timer1 = font.render('Tempo ' + str(temporizador), True, (YELLOW))
        screen.blit(timer1, (50, 500))

        cb1.render_checkbox()
        cb2.render_checkbox()
        cb3.render_checkbox()

        if not cb1.is_unchecked() and not cb2.is_unchecked() and not cb3.is_unchecked():
            telaSegundoNivel()

        pygame.display.flip()
        clock.tick(60)

        screen.fill(BLUE)

        tituloLegendasTarefas()


# Função do botão próximo (instruções), redirecionando para página Tarefas - NÍVEL 2
def clicarProximoTarefasNivel2():
    global estado
    estado = 'clicarProximoTarefasNivel2'

    clock = pygame.time.Clock()
    input_box1 = InputBox(400, 50, 140, 32)
    input_box2 = InputBox(400, 120, 140, 32)
    input_box3 = InputBox(400, 190, 140, 32)
    input_box4 = InputBox(400, 250, 140, 32)

    # Criando objeto Clock
    CLOCKTICK = pygame.USEREVENT + 1
    pygame.time.set_timer(CLOCKTICK, 36000)  # Configurado o timer do Pygame para execução a cada 1 segundo
    temporizador = 120

    cb1 = Checkbox(screen, 650, 45)
    cb2 = Checkbox(screen, 650, 120)
    cb3 = Checkbox(screen, 650, 190)
    cb4 = Checkbox(screen, 650, 250)
    input_boxes = [input_box1, input_box2, input_box3, input_box4]

    masculino = pygame.image.load("./Assets/Images/homem.png").convert()

    # Declarando a fonte do placar e variável contadora
    font = pygame.font.SysFont('sans', 40)

    botaoNenhumaTarefa = criarRetangulo("Não concluí", (510, 485, 200, 75), BLUE, TOMATO, gameover)

    x, y = 300, 300
    move_x, move_y = 0, 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    move_x -= 1
                if event.key == K_RIGHT:
                    move_x += 1
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    move_x = 0

            # Capturando evendo de relogio e atualizando a variável contadora
            if event.type == CLOCKTICK:
                temporizador = temporizador - 1

            checarEventoBotao(botaoNenhumaTarefa, event)

            x += move_x
            y += move_y

            for box in input_boxes:
                box.eventoInputBox(event)

            cb1.update_checkbox(event)
            cb2.update_checkbox(event)
            cb3.update_checkbox(event)
            cb4.update_checkbox(event)

        # Finalizando o jogo
        if temporizador == 0:
            gameover()

        # renderizando as fontes do placar na tela
        score1 = font.render('Placar ' + str(cb1.placar + cb2.placar + cb3.placar + cb4.placar), True, (WHITE))
        screen.blit(score1, (300, 500))

        screen.blit(masculino, (x, y))
        botao(screen, botaoNenhumaTarefa)

        for box in input_boxes:
            box.atualizarInputBox()

        for box in input_boxes:
            box.desenharInputBox(screen)

        # renderizando as fontes do cronometro na tela do usuario
        timer1 = font.render('Tempo ' + str(temporizador), True, (YELLOW))
        screen.blit(timer1, (50, 500))

        cb1.render_checkbox()
        cb2.render_checkbox()
        cb3.render_checkbox()
        cb4.render_checkbox()

        if not cb1.is_unchecked() and not cb2.is_unchecked() and not cb3.is_unchecked() and not cb4.is_unchecked():
            telaTerceiroNivel()

        pygame.display.flip()
        clock.tick(60)

        screen.fill(BLUE)

        tituloLegendasTarefasNivel2()


# Função do botão próximo (instruções), redirecionando para página Tarefas - NÍVEL 3
def clicarProximoTarefasNivel3():
    global estado
    estado = 'clicarProximoTarefasNivel3'

    clock = pygame.time.Clock()
    input_box1 = InputBox(400, 50, 140, 32)
    input_box2 = InputBox(400, 120, 140, 32)
    input_box3 = InputBox(400, 190, 140, 32)
    input_box4 = InputBox(400, 250, 140, 32)
    input_box5 = InputBox(100, 250, 140, 32)

    # Criando objeto Clock
    CLOCKTICK = pygame.USEREVENT + 1
    pygame.time.set_timer(CLOCKTICK, 36000)  # Configurado o timer do Pygame para execução a cada 1 segundo
    temporizador = 180

    cb1 = Checkbox(screen, 650, 45)
    cb2 = Checkbox(screen, 650, 120)
    cb3 = Checkbox(screen, 650, 190)
    cb4 = Checkbox(screen, 650, 250)
    cb5 = Checkbox(screen, 320, 250)
    input_boxes = [input_box1, input_box2, input_box3, input_box4, input_box5]

    masculino = pygame.image.load("./Assets/Images/homem.png").convert()

    # Declarando a fonte do placar e variável contadora
    font = pygame.font.SysFont('sans', 40)

    botaoNenhumaTarefa = criarRetangulo("Não concluí", (510, 485, 200, 75), BLUE, TOMATO, gameover)

    x, y = 300, 300
    move_x, move_y = 0, 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    move_x -= 1
                if event.key == K_RIGHT:
                    move_x += 1
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    move_x = 0

            # Capturando evendo de relogio e atualizando a variável contadora
            if event.type == CLOCKTICK:
                temporizador = temporizador - 1

            checarEventoBotao(botaoNenhumaTarefa, event)

            x += move_x
            y += move_y

            for box in input_boxes:
                box.eventoInputBox(event)

            cb1.update_checkbox(event)
            cb2.update_checkbox(event)
            cb3.update_checkbox(event)
            cb4.update_checkbox(event)
            cb5.update_checkbox(event)

        # Finalizando o jogo
        if temporizador == 0:
            gameover()

        # renderizando as fontes do placar na tela
        score1 = font.render('Placar ' + str(cb1.placar + cb2.placar + cb3.placar + cb4.placar + cb5.placar), True, (WHITE))
        screen.blit(score1, (300, 500))

        screen.blit(masculino, (x, y))
        botao(screen, botaoNenhumaTarefa)

        for box in input_boxes:
            box.atualizarInputBox()

        for box in input_boxes:
            box.desenharInputBox(screen)

        # renderizando as fontes do cronometro na tela do usuario
        timer1 = font.render('Tempo ' + str(temporizador), True, (YELLOW))
        screen.blit(timer1, (50, 500))

        cb1.render_checkbox()
        cb2.render_checkbox()
        cb3.render_checkbox()
        cb4.render_checkbox()
        cb5.render_checkbox()

        if not cb1.is_unchecked() and not cb2.is_unchecked() and not cb3.is_unchecked() and not cb4.is_unchecked() and not cb5.is_unchecked():
            ultimaTela()

        pygame.display.flip()
        clock.tick(60)

        screen.fill(BLUE)

        tituloLegendasTarefasNivel3()


# Função do botão próximo (instruções Feminino), redirecionando para página Tarefas
def clicarProximoTarefasFeminino():
    global estado
    estado = 'proximaTelaTarefasFeminino'

    clock = pygame.time.Clock()
    input_box1 = InputBox(400, 50, 140, 32)
    input_box2 = InputBox(400, 120, 140, 32)
    input_box3 = InputBox(400, 190, 140, 32)

    # Criando objeto Clock
    CLOCKTICK = pygame.USEREVENT + 1
    pygame.time.set_timer(CLOCKTICK, 36000)  # Configurado o timer do Pygame para execução a cada 1 segundo
    temporizador = 60

    cb1 = Checkbox(screen, 650, 45)
    cb2 = Checkbox(screen, 650, 120)
    cb3 = Checkbox(screen, 650, 190)
    input_boxes = [input_box1, input_box2, input_box3]

    feminino = pygame.image.load("./Assets/Images/mulher.png").convert()

    # Declarando a fonte do placar e variável contadora
    font = pygame.font.SysFont('sans', 40)

    botaoNenhumaTarefa = criarRetangulo("Não concluí", (510, 485, 200, 75), BLUE, TOMATO, gameover)

    x, y = 300, 300
    move_x, move_y = 0, 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    move_x -= 1
                if event.key == K_RIGHT:
                    move_x += 1
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    move_x = 0

            # Capturando evendo de relogio e atualizando a variável contadora
            if event.type == CLOCKTICK:
                temporizador = temporizador - 1

            checarEventoBotao(botaoNenhumaTarefa, event)

            x += move_x
            y += move_y

            for box in input_boxes:
                box.eventoInputBox(event)

            cb1.update_checkbox(event)
            cb2.update_checkbox(event)
            cb3.update_checkbox(event)

        # Finalizando o jogo
        if temporizador == 0:
            gameover()

        # renderizando as fontes do placar na tela
        score1 = font.render('Placar ' + str(cb1.placar + cb2.placar + cb3.placar), True, (WHITE))
        screen.blit(score1, (300, 500))

        screen.blit(feminino, (x, y))
        botao(screen, botaoNenhumaTarefa)

        for box in input_boxes:
            box.atualizarInputBox()

        for box in input_boxes:
            box.desenharInputBox(screen)

        # renderizando as fontes do cronometro na tela do usuario
        timer1 = font.render('Tempo ' + str(temporizador), True, (YELLOW))
        screen.blit(timer1, (50, 500))

        cb1.render_checkbox()
        cb2.render_checkbox()
        cb3.render_checkbox()

        if not cb1.is_unchecked() and not cb2.is_unchecked() and not cb3.is_unchecked():
            telaSegundoNivel()

        pygame.display.flip()
        clock.tick(60)

        screen.fill(BLUE)

        tituloLegendasTarefasFeminino()


# Função do botão próximo (instruções Feminino), redirecionando para página Tarefas - NÍVEL 2
def clicarProximoTarefasNivel2Feminino():
    global estado
    estado = 'clicarProximoTarefasNivel2'

    clock = pygame.time.Clock()
    input_box1 = InputBox(400, 50, 140, 32)
    input_box2 = InputBox(400, 120, 140, 32)
    input_box3 = InputBox(400, 190, 140, 32)
    input_box4 = InputBox(400, 250, 140, 32)

    # Criando objeto Clock
    CLOCKTICK = pygame.USEREVENT + 1
    pygame.time.set_timer(CLOCKTICK, 36000)  # Configurado o timer do Pygame para execução a cada 1 segundo
    temporizador = 120

    cb1 = Checkbox(screen, 650, 45)
    cb2 = Checkbox(screen, 650, 120)
    cb3 = Checkbox(screen, 650, 190)
    cb4 = Checkbox(screen, 650, 250)
    input_boxes = [input_box1, input_box2, input_box3, input_box4]

    feminino = pygame.image.load("./Assets/Images/homem.png").convert()

    # Declarando a fonte do placar e variável contadora
    font = pygame.font.SysFont('sans', 40)

    botaoNenhumaTarefa = criarRetangulo("Não concluí", (510, 485, 200, 75), BLUE, TOMATO, gameover)

    x, y = 300, 300
    move_x, move_y = 0, 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    move_x -= 1
                if event.key == K_RIGHT:
                    move_x += 1
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    move_x = 0

            # Capturando evendo de relogio e atualizando a variável contadora
            if event.type == CLOCKTICK:
                temporizador = temporizador - 1

            checarEventoBotao(botaoNenhumaTarefa, event)

            x += move_x
            y += move_y

            for box in input_boxes:
                box.eventoInputBox(event)

            cb1.update_checkbox(event)
            cb2.update_checkbox(event)
            cb3.update_checkbox(event)
            cb4.update_checkbox(event)

        # Finalizando o jogo
        if temporizador == 0:
            gameover()

        # renderizando as fontes do placar na tela
        score1 = font.render('Placar ' + str(cb1.placar + cb2.placar + cb3.placar + cb4.placar), True, (WHITE))
        screen.blit(score1, (300, 500))

        screen.blit(feminino, (x, y))
        botao(screen, botaoNenhumaTarefa)

        for box in input_boxes:
            box.atualizarInputBox()

        for box in input_boxes:
            box.desenharInputBox(screen)

        # renderizando as fontes do cronometro na tela do usuario
        timer1 = font.render('Tempo ' + str(temporizador), True, (YELLOW))
        screen.blit(timer1, (50, 500))

        cb1.render_checkbox()
        cb2.render_checkbox()
        cb3.render_checkbox()
        cb4.render_checkbox()

        if not cb1.is_unchecked() and not cb2.is_unchecked() and not cb3.is_unchecked() and not cb4.is_unchecked():
            telaTerceiroNivel()

        pygame.display.flip()
        clock.tick(60)

        screen.fill(BLUE)

        tituloLegendasTarefasNivel2Feminino()


# Função do botão próximo (instruções Feminino), redirecionando para página Tarefas - NÍVEL 3
def clicarProximoTarefasNivel3Feminino():
    global estado
    estado = 'clicarProximoTarefasNivel3Feminino'

    clock = pygame.time.Clock()
    input_box1 = InputBox(400, 50, 140, 32)
    input_box2 = InputBox(400, 120, 140, 32)
    input_box3 = InputBox(400, 190, 140, 32)
    input_box4 = InputBox(400, 250, 140, 32)
    input_box5 = InputBox(100, 250, 140, 32)

    # Criando objeto Clock
    CLOCKTICK = pygame.USEREVENT + 1
    pygame.time.set_timer(CLOCKTICK, 36000)  # Configurado o timer do Pygame para execução a cada 1 segundo
    temporizador = 180

    cb1 = Checkbox(screen, 650, 45)
    cb2 = Checkbox(screen, 650, 120)
    cb3 = Checkbox(screen, 650, 190)
    cb4 = Checkbox(screen, 650, 250)
    cb5 = Checkbox(screen, 320, 250)
    input_boxes = [input_box1, input_box2, input_box3, input_box4, input_box5]

    feminino = pygame.image.load("./Assets/Images/mulher.png").convert()

    # Declarando a fonte do placar e variável contadora
    font = pygame.font.SysFont('sans', 40)

    botaoNenhumaTarefa = criarRetangulo("Não concluí", (510, 485, 200, 75), BLUE, TOMATO, gameover)

    x, y = 300, 300
    move_x, move_y = 0, 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    move_x -= 1
                if event.key == K_RIGHT:
                    move_x += 1
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    move_x = 0

            # Capturando evendo de relogio e atualizando a variável contadora
            if event.type == CLOCKTICK:
                temporizador = temporizador - 1

            checarEventoBotao(botaoNenhumaTarefa, event)

            x += move_x
            y += move_y

            for box in input_boxes:
                box.eventoInputBox(event)

            cb1.update_checkbox(event)
            cb2.update_checkbox(event)
            cb3.update_checkbox(event)
            cb4.update_checkbox(event)
            cb5.update_checkbox(event)

        # Finalizando o jogo
        if temporizador == 0:
            gameover()

        # renderizando as fontes do placar na tela
        score1 = font.render('Placar ' + str(cb1.placar + cb2.placar + cb3.placar + cb4.placar + cb5.placar), True, (WHITE))
        screen.blit(score1, (300, 500))

        screen.blit(feminino, (x, y))
        botao(screen, botaoNenhumaTarefa)

        for box in input_boxes:
            box.atualizarInputBox()

        for box in input_boxes:
            box.desenharInputBox(screen)

        # renderizando as fontes do cronometro na tela do usuario
        timer1 = font.render('Tempo ' + str(temporizador), True, (YELLOW))
        screen.blit(timer1, (50, 500))

        cb1.render_checkbox()
        cb2.render_checkbox()
        cb3.render_checkbox()
        cb4.render_checkbox()
        cb5.render_checkbox()

        if not cb1.is_unchecked() and not cb2.is_unchecked() and not cb3.is_unchecked() and not cb4.is_unchecked() and not cb5.is_unchecked():
            ultimaTela()

        pygame.display.flip()
        clock.tick(60)

        screen.fill(BLUE)

        tituloLegendasTarefasNivel3Feminino()


# Função do botão próximo (avatar masculino), redirecionando para página Instruções
def clicarProximoInstrucoes():
    global estado
    estado = 'clicarProximoInstrucoes'


# Função do botão próximo (avatar feminino), redirecionando para página Instruções
def clicarProximoInstrucoesFeminino():
    global estado
    estado = 'clicarProximoInstrucoesFeminino'


# Função do botão Opções
def clicarOpcoes():
    global estado
    estado = 'opcoes'


# Função do botão Sair
def clicarSair():
    global estado
    global jogoRodando

    estado = 'sair'
    jogoRodando = False


# Função do botão Voltar
def clicarVoltar():
    global estado
    estado = 'menu'


# Função de ligar som do jogo
def clicarLigarSom():
    global estado
    estado = 'opcoes'

    mixer.music.unpause()


# Função de desligar som do jogo
def clicarDesligarSom():
    global estado
    estado = 'opcoes'

    mixer.music.pause()


# Função com objetivo de retornar uma imagem
def pegarImagem(caminho):
    global conjImagens
    imagem = conjImagens.get(caminho)
    if imagem is None:
        diretorio = caminho.replace('/', os.sep).replace('\\', os.sep)
        imagem = pygame.image.load(diretorio)
        conjImagens[caminho] = imagem
    return imagem


# -------------------------------------------Funções----------------------------------------------------------------

# -------------------------------------------Definição Pygame/Criação dos botões------------------------------------

# Carregamento da música de fundo
mixer.music.load('./Assets/Audio/fundo.mp3')
mixer.music.play()

# Titulo do jogo
pygame.display.set_caption("Day to day game")

# Criação do retângulo da Surface
screen_rect = screen.get_rect()

# Criação de um vetor, para armazenar as imagens
conjImagens = {}

estado = 'menu'

# Botões Menu
botaoJogar = criarRetangulo("Jogar", (300, 300, 200, 75), BLUE, TOMATO, clicarJogar)
botaoOpcoes = criarRetangulo("Opções", (300, 400, 200, 75), BLUE, TOMATO, clicarOpcoes)
botaoSair = criarRetangulo("Sair", (300, 500, 200, 75), BLUE, TOMATO, clicarSair)

botaoVoltar = criarRetangulo("Voltar", (300, 500, 200, 75), BLUE, TOMATO, clicarVoltar)

# Botão som nas Opções
botaoLigarSom = criarRetangulo("Som ON", (300, 300, 200, 75), BLUE, TOMATO, clicarLigarSom)
botaoDesligarSom = criarRetangulo("Som OFF", (300, 400, 200, 75), BLUE, TOMATO, clicarDesligarSom)

# Jogo 1º tela / Avatar
legendaJogoAvatar = criarRetangulo("Escolha seu avatar", (300, 250, 200, 75), BLUE, BLUE, legendaAvatar)
botaoProximoInstrucoes = criarRetangulo("Masculino", (200, 500, 200, 75), BLUE, TOMATO, clicarProximoInstrucoes)
botaoProximoInstrucoes2 = criarRetangulo("Feminino", (400, 500, 200, 75), BLUE, TOMATO, clicarProximoInstrucoesFeminino)

# Jogo 2º Tela / Instruções
legenda1Jogo = criarRetangulo("Ajude seu avatar a sair da PROCASTINAÇÃO", (300, 250, 200, 75), BLUE, BLUE, legendaJogo)
legenda2Jogo = criarRetangulo("Comece definindo os horários com 3 tarefas", (300, 350, 200, 75), BLUE, BLUE,
                              legendaJogo)
botaoProximoTarefas = criarRetangulo("Próximo", (300, 500, 200, 75), BLUE, TOMATO, clicarProximoTarefas)
botaoProximoTarefasFeminino = criarRetangulo("Próximo", (300, 500, 200, 75), BLUE, TOMATO, clicarProximoTarefasFeminino)

# -------------------------------------------Definição Pygame/Criação dos botões------------------------------------

# -------------------------------------------Funcionamento do Jogo--------------------------------------------------

jogoRodando = True

while jogoRodando:

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogoRodando = False

        if estado == 'menu':
            checarEventoBotao(botaoJogar, event)
            checarEventoBotao(botaoOpcoes, event)
            checarEventoBotao(botaoSair, event)
        elif estado == 'jogo':
            checarEventoBotao(botaoProximoInstrucoes, event)
            checarEventoBotao(botaoProximoInstrucoes2, event)
        elif estado == 'opcoes':
            checarEventoBotao(botaoLigarSom, event)
            checarEventoBotao(botaoDesligarSom, event)
            checarEventoBotao(botaoVoltar, event)
        elif estado == 'clicarProximoInstrucoes':
            checarEventoBotao(botaoProximoTarefas, event)
            clicarProximoInstrucoes()
        elif estado == 'clicarProximoInstrucoesFeminino':
            checarEventoBotao(botaoProximoTarefasFeminino, event)
            clicarProximoInstrucoesFeminino()
        elif estado == 'proximaTelaJogo':
            clicarProximoTarefas()

    screen.fill(BLUE)
    background = pygame.image.load("./Assets/Images/checklist.png").convert()

    screen.blit(pegarImagem('.\Assets\Images\logo.png'), (300, 40))

    # Estados para mostrar a tela de cada opção
    if estado == 'menu':
        botao(screen, botaoJogar)
        botao(screen, botaoOpcoes)
        botao(screen, botaoSair)
    elif estado == 'jogo':
        masculino = pygame.image.load("./Assets/Images/homem.png").convert()
        screen.blit(masculino, (220, 325))
        feminino = pygame.image.load("./Assets/Images/mulher.png").convert()
        screen.blit(feminino, (420, 325))

        botao(screen, legendaJogoAvatar)
        botao(screen, botaoProximoInstrucoes)
        botao(screen, botaoProximoInstrucoes2)
    elif estado == 'clicarProximoInstrucoes':
        botao(screen, legenda1Jogo)
        botao(screen, legenda2Jogo)
        botao(screen, botaoProximoTarefas)
    elif estado == 'clicarProximoInstrucoesFeminino':
        botao(screen, legenda1Jogo)
        botao(screen, legenda2Jogo)
        botao(screen, botaoProximoTarefasFeminino)
    elif estado == 'opcoes':
        botao(screen, botaoLigarSom)
        botao(screen, botaoDesligarSom)
        botao(screen, botaoVoltar)

    pygame.display.update()

pygame.quit()
