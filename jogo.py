import os
import pygame
from pygame import mixer

# Definição das cores em RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (106, 159, 181)
TOMATO = (255,99,71)

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
        width = max(200, self.texto_surface.get_width()+10)
        self.retangulo.w = width

    def desenharInputBox(self, screen):
        screen.blit(self.texto_surface, (self.retangulo.x+5, self.retangulo.y+5))
        pygame.draw.rect(screen, self.cor, self.retangulo, 2)

#-------------------------------------------Funções----------------------------------------------------------------

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

# Função criada, para definir o título, e legendas das tarefas/horários que aparecem na 4º tela
def tituloLegendasTarefas():

    fontTituloTarefas = pygame.font.SysFont("./Assets/Fonts/Bungee-Regular.ttf", 32, bold=True)
    tituloTarefas = fontTituloTarefas.render("Coloque 3 tarefas da sua rotina", True, WHITE)

    fontTarefa1 = pygame.font.SysFont("./Assets/Fonts/Bungee-Regular.ttf", 30)
    tarefa1 = fontTarefa1.render("Tarefa 1", True, WHITE)

    fontTarefa2 = pygame.font.SysFont("./Assets/Fonts/Bungee-Regular.ttf", 30)
    tarefa2 = fontTarefa2.render("Tarefa 2", True, WHITE)

    fontTarefa3 = pygame.font.SysFont("./Assets/Fonts/Bungee-Regular.ttf", 30)
    tarefa3 = fontTarefa3.render("Tarefa 3", True, WHITE)

    fontHorarioTarefa1 = pygame.font.SysFont("./Assets/Fonts/Bungee-Regular.ttf", 30)
    horarioTarefa1 = fontHorarioTarefa1.render("Horário da 1º Tarefa", True, WHITE)

    fontHorarioTarefa2 = pygame.font.SysFont("./Assets/Fonts/Bungee-Regular.ttf", 30)
    horarioTarefa2 = fontHorarioTarefa2.render("Horário da 2º Tarefa", True, WHITE)

    fontHorarioTarefa3 = pygame.font.SysFont("./Assets/Fonts/Bungee-Regular.ttf", 30)
    horarioTarefa3 = fontHorarioTarefa3.render("Horário da 3º Tarefa", True, WHITE)

    botaoContinuarTarefas = criarRetangulo("Continuar", (300, 500, 200, 75), BLUE, TOMATO, clicarProximoTarefas)

    botao(screen, botaoContinuarTarefas)

    screen.blit(tituloTarefas, (200, 100, 200, 75))

    screen.blit(tarefa1, (160, 180, 100, 10))
    screen.blit(tarefa2, (160, 280, 100, 10))
    screen.blit(tarefa3, (160, 380, 100, 10))

    screen.blit(horarioTarefa1, (505, 180, 100, 10))
    screen.blit(horarioTarefa2, (505, 280, 100, 10))
    screen.blit(horarioTarefa3, (505, 380, 100, 10))

# Função do botão próximo (instruções), redirecionando para página Tarefas
def clicarProximoTarefas():
    global estado
    estado = 'proximaTelaTarefas'

    clock = pygame.time.Clock()
    input_box1 = InputBox(100, 200, 140, 32)
    input_box2 = InputBox(100, 300, 140, 32)
    input_box3 = InputBox(100, 400, 140, 32)

    input_box4 = InputBox(500, 200, 140, 32)
    input_box5 = InputBox(500, 300, 140, 32)
    input_box6 = InputBox(500, 400, 140, 32)

    input_boxes = [input_box1, input_box2, input_box3, input_box4, input_box5, input_box6]
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            for box in input_boxes:
                box.eventoInputBox(event)

        for box in input_boxes:
            box.atualizarInputBox()

        for box in input_boxes:
            box.desenharInputBox(screen)

        pygame.display.flip()
        clock.tick(30)

        screen.fill(BLUE)

        tituloLegendasTarefas()

# Função do botão próximo (avatar), redirecionando para página Instruções
def clicarProximoInstrucoes():
    global estado
    estado = 'clicarProximoInstrucoes'

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
#-------------------------------------------Funções----------------------------------------------------------------

#-------------------------------------------Definição Pygame/Criação dos botões------------------------------------

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
botaoProximoInstrucoes = criarRetangulo("Próximo", (300, 500, 200, 75), BLUE, TOMATO, clicarProximoInstrucoes)

# Jogo 2º Tela / Instruções
legenda1Jogo = criarRetangulo("Ajude seu avatar a sair da PROCASTINAÇÃO", (300, 250, 200, 75), BLUE, BLUE, legendaJogo)
legenda2Jogo = criarRetangulo("Comece definindo os horários com 3 tarefas", (300, 350, 200, 75), BLUE, BLUE, legendaJogo)
botaoProximoTarefas = criarRetangulo("Próximo", (300, 500, 200, 75), BLUE, TOMATO, clicarProximoTarefas)

# Jogo 3º Tela / Tarefas


# Jogo 4º Tela / Animação


# Jogo 5º Tela / Gameover


#-------------------------------------------Definição Pygame/Criação dos botões------------------------------------

#-------------------------------------------Funcionamento do Jogo--------------------------------------------------

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
        elif estado == 'opcoes':
            checarEventoBotao(botaoLigarSom, event)
            checarEventoBotao(botaoDesligarSom, event)
            checarEventoBotao(botaoVoltar, event)
        elif estado == 'clicarProximoInstrucoes':
            checarEventoBotao(botaoProximoTarefas, event)
            clicarProximoInstrucoes()
        elif estado == 'proximaTelaJogo':
            clicarProximoTarefas()

    screen.fill(BLUE)
    background = pygame.image.load("./Assets/Images/checklist.png").convert()
    #screen.blit(background, (0,0))

    screen.blit(pegarImagem('.\Assets\Images\logo.png'), (300, 40))

    # Estados para mostrar a tela de cada opção
    if estado == 'menu':
        botao(screen, botaoJogar)
        botao(screen, botaoOpcoes)
        botao(screen, botaoSair)
    elif estado == 'jogo':
        masculino = pygame.image.load("./Assets/Images/masculino.png").convert()
        screen.blit(masculino, (250,325))
        feminino = pygame.image.load("./Assets/Images/feminino.png").convert()
        screen.blit(feminino, (420, 325))

        botao(screen, legendaJogoAvatar)
        botao(screen, botaoProximoInstrucoes)
    elif estado == 'clicarProximoInstrucoes':
        botao(screen, legenda1Jogo)
        botao(screen, legenda2Jogo)
        botao(screen, botaoProximoTarefas)
    elif estado == 'opcoes':
        botao(screen, botaoLigarSom)
        botao(screen, botaoDesligarSom)
        botao(screen, botaoVoltar)

    pygame.display.update()

pygame.quit()

#-------------------------------------------Funcionamento do Jogo--------------------------------------------------