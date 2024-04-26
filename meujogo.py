import pygame
import sys
import random
import unicodedata

# Inicialização do Pygame
pygame.init()
pygame.mixer.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo da Forca")

background_image = pygame.image.load("background6.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
background_image1 = pygame.image.load("fundoforca1.png")
background_image1 = pygame.transform.scale(background_image1, (WIDTH, HEIGHT))
background_image2 = pygame.image.load("vitoria.jpg")
background_image2 = pygame.transform.scale(background_image2, (WIDTH, HEIGHT))
background_image3 = pygame.image.load("derrota.webp")
background_image3 = pygame.transform.scale(background_image3, (WIDTH, HEIGHT))


# Carregar imagens da forca
images = [
    pygame.transform.scale(pygame.image.load("img/forca-0.png"), (400, 400)),
    pygame.transform.scale(pygame.image.load("img/forca-1.png"), (400, 400)),
    pygame.transform.scale(pygame.image.load("img/forca-2.png"), (400, 400)),
    pygame.transform.scale(pygame.image.load("img/forca-3.png"), (400, 400)),
    pygame.transform.scale(pygame.image.load("img/forca-4.png"), (400, 400)),
    pygame.transform.scale(pygame.image.load("img/forca-5.png"), (400, 400)),
    pygame.transform.scale(pygame.image.load("img/forca-6.png"), (400, 400))
]

# Carregar sons
correct_sound = pygame.mixer.Sound("sounds/acerto.wav")
incorrect_sound = pygame.mixer.Sound("sounds/erro.wav")
win_sound = pygame.mixer.Sound("sounds/vitoria.wav")
lose_sound = pygame.mixer.Sound("sounds/derrota.wav")

# Dicionário de temas, palavras e dicas
word_themes = {
    "animais": {
        "facil": [
            {"palavra": "GATO", "dica": "Animal doméstico com pelos e garras retráteis."},
            {"palavra": "CACHORRO", "dica": "O melhor amigo do homem."},
            {"palavra": "LEÃO", "dica": "Rei da selva."},
            {"palavra": "ELEFANTE", "dica": "Maior animal terrestre."},
        ],
        "medio": [
            {"palavra": "GIRAFA", "dica": "Animal com pescoço longo."},
            {"palavra": "TIGRE", "dica": "Animal listrado e feroz."},
            {"palavra": "ZEBRA", "dica": "Animal listrado da savana africana."},
            {"palavra": "COBRA", "dica": "Réptil rastejante."},
        ],
        "dificil": [
            {"palavra": "HIPOPÓTAMO", "dica": "Mamífero herbívoro semiaquático de grande porte."},
            {"palavra": "JAGUATIRICA", "dica": "Felino selvagem encontrado nas Américas."},
            {"palavra": "ORNITORRINCO", "dica": "Animal mamífero ovíparo e semiaquático."},
            {"palavra": "GAVIÃO", "dica": "Ave de rapina."},
        ]
    },
    "frutas": {
        "facil": [
            {"palavra": "MORANGO", "dica": "Pequena fruta vermelha e doce."},
            {"palavra": "BANANA", "dica": "Fruta amarela e alongada."},
            {"palavra": "MAÇÃ", "dica": "Fruta redonda e verde ou vermelha."},
            {"palavra": "LARANJA", "dica": "Fruta cítrica."},
        ],
        "medio": [
            {"palavra": "UVA", "dica": "Pequena fruta arredondada."},
            {"palavra": "ABACAXI", "dica": "Fruta tropical com casca espinhosa."},
            {"palavra": "MANGA", "dica": "Fruta tropical de polpa suculenta."},
            {"palavra": "KIWI", "dica": "Fruta pequena e peluda."},
        ],
        "dificil": [
            {"palavra": "CAJÁ", "dica": "Fruta de polpa amarela e ácida."},
            {"palavra": "TAMARINDO", "dica": "Fruta tropical de sabor agridoce."},
            {"palavra": "RAMBUTAN", "dica": "Fruta asiática com casca peluda."},
            {"palavra": "JABUTICABA", "dica": "Fruta brasileira de polpa suculenta."},
        ]
    },
    "países": {
        "facil": [
            {"palavra": "BRASIL", "dica": "Maior país da América do Sul."},
            {"palavra": "JAPÃO", "dica": "Arquipélago no leste da Ásia."},
            {"palavra": "ITÁLIA", "dica": "País europeu conhecido por sua gastronomia."},
            {"palavra": "EGITO", "dica": "País conhecido por suas pirâmides."},
        ],
        "medio": [
            {"palavra": "AUSTRÁLIA", "dica": "País que também é um continente."},
            {"palavra": "CANADÁ", "dica": "País na América do Norte."},
            {"palavra": "ARGENTINA", "dica": "País sul-americano famoso por sua carne e danças."},
            {"palavra": "ÍNDIA", "dica": "País da Ásia conhecido por sua diversidade cultural."},
        ],
        "dificil": [
            {"palavra": "CROÁCIA", "dica": "País europeu banhado pelo Mar Adriático."},
            {"palavra": "NIGÉRIA", "dica": "País da África Ocidental."},
            {"palavra": "NORUEGA", "dica": "País escandinavo famoso por seus fiordes."},
            {"palavra": "INDONÉSIA", "dica": "País insular no sudeste asiático."},
        ]
    }
}

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (35, 142, 104)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Função para desenhar texto na tela
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

# Função para desenhar botão
def draw_button(color, x, y, width, height, text, font, text_color):
    pygame.draw.rect(screen, color, (x, y, width, height))# Desenha o retângulo do botão
    text_surface = font.render(text, True, text_color)# Renderiza o texto do botão
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))# Obtém o retângulo que envolve o texto
    screen.blit(text_surface, text_rect)# Desenha o texto do botão na tela

# Função para desenhar o botão de dica na tela
def draw_hint_button(screen):
    hint_button_rect = pygame.Rect(650, 20, 100, 40)
    pygame.draw.rect(screen, (0, 255, 0), hint_button_rect)
    font = pygame.font.SysFont(None, 24)
    text = font.render("Dica", True, (0, 0, 0))
    screen.blit(text, (675, 30))
# Função para exibir a tela inicial
def initial_screen():
    while True:
        # Desenhar a imagem de fundo na tela
        screen.blit(background_image, (0, 0))
        font_title = pygame.font.Font(None, 70)
        draw_text("JOGO DA FORCA", font_title, WHITE, WIDTH / 2, HEIGHT / 2 - 140)
        draw_button(GREEN, WIDTH / 2 - 100, HEIGHT / 2, 200, 50, "JOGAR", pygame.font.Font(None, 35), WHITE)
        draw_button(GREEN, WIDTH / 2 - 100, HEIGHT / 2 + 70, 200, 50, "PONTUAÇÕES", pygame.font.Font(None, 35), WHITE)
        draw_button(RED, WIDTH / 2 - 100, HEIGHT / 2 + 140, 200, 50, "SAIR", pygame.font.Font(None, 35), WHITE)  # Botão de sair
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if WIDTH / 2 - 100 <= mouse_pos[0] <= WIDTH / 2 + 100 and HEIGHT / 2 <= mouse_pos[1] <= HEIGHT / 2 + 50:
                    return "play"
                elif WIDTH / 2 - 100 <= mouse_pos[0] <= WIDTH / 2 + 100 and HEIGHT / 2 + 70 <= mouse_pos[1] <= HEIGHT / 2 + 120:
                    return "scores"
                elif WIDTH / 2 - 100 <= mouse_pos[0] <= WIDTH / 2 + 100 and HEIGHT / 2 + 140 <= mouse_pos[1] <= HEIGHT / 2 + 190:  # Verifica se o botão de sair foi clicado
                    pygame.quit()
                    sys.exit()


# Função para escolher um tema
def choose_theme():
    theme = None
    while theme not in word_themes:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for idx, theme_name in enumerate(word_themes.keys()):
                    button_x = WIDTH / 2 - 150
                    button_y = HEIGHT / 2 + idx * 50
                    if button_x <= mouse_pos[0] <= button_x + 300 and button_y <= mouse_pos[1] <= button_y + 40:
                        theme = theme_name
                        break
        screen.blit(background_image, (0, 0))
        draw_text("Escolha um tema:", pygame.font.Font(None, 60), WHITE, WIDTH / 2, HEIGHT / 2 - 100)
        for idx, theme_name in enumerate(word_themes.keys()):
            button_x = WIDTH / 2 - 150
            button_y = HEIGHT / 2 + idx * 50
            draw_button(GREEN, button_x, button_y, 300, 40, theme_name.capitalize(), pygame.font.Font(None, 30), WHITE)
        pygame.display.update()
    return theme

# Função para escolher a dificuldade
def choose_difficulty():
    difficulty = None
    while difficulty not in ['facil', 'medio', 'dificil']:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for idx, diff in enumerate(['facil', 'medio', 'dificil']):
                    button_x = WIDTH / 2 - 150
                    button_y = HEIGHT / 2 + idx * 50
                    if button_x <= mouse_pos[0] <= button_x + 300 and button_y <= mouse_pos[1] <= button_y + 40:
                        difficulty = diff
                        break
        screen.blit(background_image, (0, 0))
        draw_text("Escolha a dificuldade:", pygame.font.Font(None, 60), WHITE, WIDTH / 2, HEIGHT / 2 - 100)
        for idx, diff in enumerate(['fácil', 'médio', 'difícil']):
            button_x = WIDTH / 2 - 150
            button_y = HEIGHT / 2 + idx * 50
            draw_button(GREEN, button_x, button_y, 300, 40, diff.capitalize(), pygame.font.Font(None, 30), WHITE)
        pygame.display.update()
    return difficulty

# Função para escolher uma palavra e dica aleatória baseada no tema e dificuldade
def choose_word_and_hint(theme, difficulty, used_words):
    available_words = [word_info for word_info in word_themes[theme][difficulty] if word_info["palavra"] not in used_words]
    if not available_words:
        return None, None  # Retorna None se todas as palavras já foram usadas
    word_info = random.choice(available_words)
    return word_info["palavra"], word_info["dica"]


# Função para remover acentos e caracteres especiais
def normalize_string(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

# Função para desenhar a palavra e a dica
def draw_word_and_hint(word, hint, guessed_letters):
    display_word = ""
    for letter in word:
        if normalize_string(letter) in guessed_letters:
            display_word += letter + " "
        else:
            display_word += "_ "
    font = pygame.font.SysFont(None, 80)
    text_word = font.render(display_word, True, BLACK)
    screen.blit(text_word, (100, 380))

    font_hint = pygame.font.SysFont(None, 40)
    text_hint = font_hint.render("Dica: " + hint, True, BLACK)
    screen.blit(text_hint, (15, 15))

# Função para desenhar a lista de letras já escolhidas
def draw_guessed_letters(guessed_letters):
    font = pygame.font.SysFont(None, 36)
    text = font.render("Letras escolhidas:", True, BLACK)
    screen.blit(text, (500, 200))
    y = 250
    for letter in guessed_letters:
        text = font.render(letter, True, BLACK)
        screen.blit(text, (570, y))
        y += 25

# Função para desenhar as tentativas restantes
def draw_attempts(tries):
    font = pygame.font.SysFont(None, 36)
    text = font.render("Tentativas restantes: {}".format(6 - tries), True, BLACK)
    screen.blit(text, (500, 100))

# Função para desenhar a mensagem de vitória
def draw_win_frame(word):
    screen.blit(background_image2, (0, 0))
    font = pygame.font.SysFont(None, 48)
    text = font.render(f"A palavra era: {word}", True, GREEN)
    screen.blit(text, (WIDTH / 2 - 175, HEIGHT / 2 + 50))
    pygame.display.flip()
    pygame.time.wait(3000)

# Função para desenhar a mensagem de derrota
def draw_lose_frame(word):
    screen.blit(background_image3, (0, 0))
    font = pygame.font.SysFont(None, 48)
    text = font.render(f"A palavra era: {word}", True, RED)
    screen.blit(text, (WIDTH / 2 - 175, HEIGHT / 2 + 50))
    pygame.display.flip()
    pygame.time.wait(3000)

# Função para desenhar o frame de jogar novamente
def draw_play_again_frame():
    screen.blit(background_image, (0, 0))
    font = pygame.font.SysFont(None, 50)
    text = font.render("Deseja jogar novamente este tema?", True, WHITE)
    screen.blit(text, (WIDTH / 2 - 300, HEIGHT / 2 - 50))
    draw_button(GREEN, WIDTH / 2 - 100, HEIGHT / 2, 100, 40, "Sim", pygame.font.Font(None, 30), WHITE)
    draw_button(RED, WIDTH / 2 + 20, HEIGHT / 2, 100, 40, "Não", pygame.font.Font(None, 30), WHITE)
    pygame.display.flip()  # Atualiza a tela após desenhar todos os elementos

# Função para perguntar se o jogador deseja jogar novamente
def ask_play_again():
    draw_play_again_frame()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if WIDTH / 2 - 100 <= mouse_pos[0] <= WIDTH / 2 - 100 + 100 and HEIGHT / 2 <= mouse_pos[1] <= HEIGHT / 2 + 40:
                    return True
                elif WIDTH / 2 + 20 <= mouse_pos[0] <= WIDTH / 2 + 20 + 100 and HEIGHT / 2 <= mouse_pos[1] <= HEIGHT / 2 + 40:
                    return False


# Função para salvar a pontuação
def save_score(name, score):
    with open("highscores.txt", "a") as file:
        file.write(f"{name}: {score}\n")

# Função para carregar as pontuações mais altas
def load_highscores():
    try:
        with open("highscores.txt", "r") as file:
            scores = file.readlines()
            scores = [score.strip() for score in scores if score.strip()]  # Remove linhas em branco
            scores = [score for score in scores if len(score.split(": ")) >= 2]  # Remove linhas sem o formato esperado
            return scores
    except FileNotFoundError:
        return []


# Função para exibir as pontuações mais altas
def show_highscores():
    highscores = load_highscores()
    highscores_sorted = sorted(highscores, key=lambda x: float(x.split(": ")[1]), reverse=True)  # Ordena as pontuações em ordem decrescente convertendo para float
    screen.blit(background_image, (0, 0))
    font = pygame.font.SysFont(None, 45)
    font1 = pygame.font.SysFont(None, 30)
    draw_text("TOP 5 MELHORES PONTUAÇÕES:", font, WHITE, WIDTH / 2, 100)
    y = 200
    for idx, score in enumerate(highscores_sorted[:5], start=1):  # Usamos a lista ordenada
        draw_text(score, font1, WHITE, WIDTH / 2, y)
        y += 30
    draw_button(GREEN, WIDTH / 2 - 50, HEIGHT - 100, 100, 40, "Voltar", pygame.font.Font(None, 30), WHITE)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if WIDTH / 2 - 50 <= mouse_pos[0] <= WIDTH / 2 + 50 and HEIGHT - 100 <= mouse_pos[1] <= HEIGHT - 60:
                    return


# Função para pedir o nome do jogador
player_name = None

def ask_player_name():
    global player_name  # Acessa a variável global player_name
    if player_name is None:  # Verifica se o nome do jogador ainda não foi definido
        screen.fill(WHITE)  # Limpa a tela para evitar que o texto fique borrado
        font = pygame.font.SysFont(None, 70)
        font1 = pygame.font.SysFont(None, 55)
        draw_text("Bem-vindo ao jogo da forca", font, WHITE, WIDTH / 2 + 200, HEIGHT / 2 + 600)
        draw_text("Digite seu nome:", font, WHITE, WIDTH / 2, HEIGHT / 2 - 50)
        pygame.display.flip()
        name = ""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        player_name = name  # Define o nome do jogador na variável global
                        return name
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode
            screen.blit(background_image, (0, 0))  # Limpa a tela antes de redesenhar o nome para evitar borrões
            draw_text("Bem-vindo ao jogo da forca", font, WHITE, WIDTH / 2, HEIGHT / 2 - 150)
            draw_text("Digite seu nome:", font1, WHITE, WIDTH / 2, HEIGHT / 2 - 50)
            
            # Desenha a caixa de entrada de texto
            pygame.draw.rect(screen, WHITE, (WIDTH / 2 - 150, HEIGHT / 2, 300, 40), 2)
            
            # Ajusta o tamanho da fonte com base na largura da caixa de entrada
            input_font = pygame.font.SysFont(None, 36)
            input_text = input_font.render(name, True, WHITE)
            text_width, text_height = input_font.size(name)
            text_x = WIDTH / 2 - text_width / 2 + 140  # Calcula a posição X para centralizar o texto
            text_y = HEIGHT / 2 + 20 - text_height / 2  # Calcula a posição Y para centralizar o texto
            if text_width > 290:  # Ajusta o texto se a largura exceder a largura da caixa
                name = name[:-1]  # Remove o último caractere
            draw_text(name, input_font, WHITE, text_x, text_y)  # Desenha o texto centralizado na caixa
            
            pygame.display.flip()
    else:
        return player_name  # Retorna o nome do jogador já definido

# Função para exibir a tela de falta de palavras disponíveis
def draw_no_words_screen():
    screen.blit(background_image, (0, 0))
    font = pygame.font.SysFont(None, 48)
    text1 = font.render("Não há mais palavras disponíveis", True, WHITE)
    text2 = font.render("nesta dificuldade", True, WHITE)
    screen.blit(text1, (WIDTH / 2 - 250, HEIGHT / 2 - 50))
    screen.blit(text2, (WIDTH / 2 - 125, HEIGHT / 2 ))
    pygame.display.flip()
    pygame.time.wait(3000)
    
# Função para desenhar o botão HOME na parte inferior esquerda
def draw_home_button():
    draw_button(GREEN, 20, HEIGHT - 40, 80, 30, "SAIR", pygame.font.Font(None, 25), WHITE)

# Função para verificar se o botão HOME na parte inferior esquerda foi pressionado
def is_home_button_pressed(mouse_pos):
    return 20 <= mouse_pos[0] <= 100 and HEIGHT - 40 <= mouse_pos[1] <= HEIGHT - 10


# Função principal do jogo
def main():
    while True:
        screen_mode = initial_screen()
        if screen_mode == "play":
            player_name = ask_player_name()  # Solicita o nome do jogador
            theme = choose_theme()
            play_game(theme)
        elif screen_mode == "scores":
            show_highscores()
        else:
            pygame.quit()
            sys.exit()

# Função para exibir a tela inicial
def initial_screen():
    while True:
        # Desenhar a imagem de fundo na tela
        screen.blit(background_image, (0, 0))
        font_title = pygame.font.Font(None, 70)
        draw_text("JOGO DA FORCA", font_title, WHITE, WIDTH / 2, HEIGHT / 2 - 140)
        draw_button(GREEN, WIDTH / 2 - 100, HEIGHT / 2, 200, 50, "JOGAR", pygame.font.Font(None, 35), WHITE)
        draw_button(GREEN, WIDTH / 2 - 100, HEIGHT / 2 + 70, 200, 50, "PONTUAÇÕES", pygame.font.Font(None, 35), WHITE)
        draw_home_button()  # Adicionando o botão HOME
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if WIDTH / 2 - 100 <= mouse_pos[0] <= WIDTH / 2 + 100 and HEIGHT / 2 <= mouse_pos[1] <= HEIGHT / 2 + 50:
                    return "play"
                elif WIDTH / 2 - 100 <= mouse_pos[0] <= WIDTH / 2 + 100 and HEIGHT / 2 + 70 <= mouse_pos[1] <= HEIGHT / 2 + 120:
                    return "scores"
                elif is_home_button_pressed(mouse_pos):  # Verifica se o botão HOME foi pressionado
                    return "home"  # Retorna à tela inicial

# Função para verificar se o botão HOME na parte inferior esquerda foi pressionado
def is_home_button_pressed(mouse_pos):
    return 20 <= mouse_pos[0] <= 100 and HEIGHT - 40 <= mouse_pos[1] <= HEIGHT - 10

# Função para calcular a pontuação do jogador
def calculate_score(tries):
    max_attempts = 6  # Número máximo de tentativas permitidas
    max_penalty = 100  # Penalidade máxima por tentativa errada
    penalty_per_attempt = max_penalty / max_attempts
    score = max(max_penalty - tries * penalty_per_attempt, 0)
    return round(score)  # Arredonda o valor da pontuação


# Função para salvar a pontuação
def save_score(name, score):
    with open("highscores.txt", "a") as file:
        file.write(f"{name}: {score}\n")

# Função para iniciar a partida do jogo da forca
def play_game(theme):
    used_words = []  # Inicializando a lista de palavras usadas
    while True:
        play_game_screen(theme, used_words)
        if not ask_play_again():
            return  # Se o jogador não quiser jogar novamente, saímos da função

# Função para exibir a tela de jogo
def play_game_screen(theme, used_words):
    while True:
        while True:
            difficulty = choose_difficulty()
            if difficulty == "back_to_theme":  # Verifica se o botão "Voltar" foi pressionado
                return "back_to_theme"
            word, hint = choose_word_and_hint(theme, difficulty, used_words)
            if word is None:
                draw_no_words_screen()
                return

            used_words.append(word)  # Adicionando a palavra atual à lista de palavras usadas
            guessed_letters = []
            tries = 0
            clock = pygame.time.Clock()
            running = True

            while running:
                screen.blit(background_image1, (0, 0))
                draw_home_button()  # Desenha o botão HOME
                screen.blit(images[tries], (2, 10))
                draw_word_and_hint(word, hint, guessed_letters)
                draw_guessed_letters(guessed_letters)
                draw_attempts(tries)
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if is_home_button_pressed(mouse_pos):  # Verifica se o botão HOME foi pressionado
                            return "home"

                    if event.type == pygame.KEYDOWN:
                        if event.key >= pygame.K_a and event.key <= pygame.K_z:
                            letter = chr(event.key).upper()
                            if normalize_string(letter) not in guessed_letters:
                                guessed_letters.append(normalize_string(letter))
                                if normalize_string(letter) not in normalize_string(word):
                                    tries += 1
                                    incorrect_sound.play()
                                else:
                                    correct_sound.play()

                if tries >= 6:
                    running = False
                    lose_sound.play()
                    draw_lose_frame(word)
                    score = calculate_score(tries)
                    save_score(player_name, score)
                    if not ask_play_again():  # Verifica se o jogador deseja jogar novamente
                        return "game_over"
                    break

                if all(normalize_string(letter) in [normalize_string(l) for l in guessed_letters] for letter in normalize_string(word)):
                    running = False
                    win_sound.play()
                    draw_win_frame(word)
                    score = calculate_score(tries)
                    save_score(player_name, score)
                    if not ask_play_again():  # Verifica se o jogador deseja jogar novamente
                        return "game_over"
                    break


# Execução do jogo
if __name__ == "__main__":
    main()
