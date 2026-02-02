import pygame
import random
from pygame.locals import *


# Inicializa o Pygame
pygame.init()


# Define as dimensões da tela
screen_width = 1350
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))


# Define o título do jogo
pygame.display.set_caption("Jogo de Memória")


# Carrega a imagem de fundo do menu
menu_background_image = pygame.image.load('background3.jpeg').convert()
# Redimensiona a imagem de fundo do menu para cobrir a tela
menu_background_image = pygame.transform.scale(menu_background_image, (screen_width, screen_height))


# Carrega a imagem de fundo do jogo
game_background_image = pygame.image.load('game_background1.jpeg').convert()
# Redimensiona a imagem de fundo do jogo para cobrir a tela
game_background_image = pygame.transform.scale(game_background_image, (screen_width, screen_height))


# Carrega a música de menu
pygame.mixer.music.load('menu_music.mp3')
# Ajuste do volume da música de menu (0.0 a 1.0)
pygame.mixer.music.set_volume(0.3)  
# Reproduz a música de menu em loop
pygame.mixer.music.play(-1)


# Define as imagens das cartas
card_images = [
    pygame.image.load('bulbasaur.jpeg').convert_alpha(),
    pygame.image.load('squirtle.jpeg').convert_alpha(),
    pygame.image.load('chamander.jpeg').convert_alpha(),
    pygame.image.load('pikachu.jpeg').convert_alpha(),
    pygame.image.load('lugia.jpeg').convert_alpha(),
    pygame.image.load('rayquaza.jpeg').convert_alpha(),
    pygame.image.load('groudon.jpeg').convert_alpha(),
    pygame.image.load('kyogre.jpeg').convert_alpha(),
    pygame.image.load('mew.jpeg').convert_alpha(),
    pygame.image.load('mewtwo.jpeg').convert_alpha(), 
    pygame.image.load('lunala.jpeg').convert_alpha(),
    pygame.image.load('solgaleo.jpeg').convert_alpha(),
    pygame.image.load('dialga.jpeg').convert_alpha(),
    pygame.image.load('palkia.jpeg').convert_alpha(),
    pygame.image.load('giratina.jpeg').convert_alpha(),
    pygame.image.load('arceus.jpeg').convert_alpha(),
    pygame.image.load('moltres.jpeg').convert_alpha(),
    pygame.image.load('articuno.jpeg').convert_alpha(),
    pygame.image.load('zapdos.jpeg').convert_alpha(),
    pygame.image.load('celebi.jpeg').convert_alpha()
]


# Dobra as cartas para criar 20 pares
pairs = [card for card in card_images for _ in range(2)]
# Embaralha as cartas
random.shuffle(pairs)


# Define a posição das cartas na tela
card_width = 100
card_height = 150
gap = 10
num_rows = 4  # 4 linhas
num_columns = 10  # 10 colunas
# Calculando o espaço total ocupado pelas cartas e seus espaços
total_width = (card_width + gap) * num_columns - gap
total_height = (card_height + gap) * num_rows - gap
# Calculando a posição inicial para centralizar as cartas
start_x = (screen_width - total_width) // 2
start_y = (screen_height - total_height) // 2
card_positions = [(start_x + i * (card_width + gap) + gap, start_y + j * (card_height + gap) + gap) for j in range(num_rows) for i in range(num_columns)]


# Carrega a imagem da carta virada
card_back = pygame.image.load('pokemon_back.jpeg').convert_alpha()


# Carrega os efeitos sonoros
card_flip_sound = pygame.mixer.Sound('card_flip.wav')
card_match_sound = pygame.mixer.Sound('card_match.wav')


# Ajuste do volume dos sons (0.0 a 1.0)
card_flip_sound.set_volume(0.3)  # Volume reduzido para 30%
card_match_sound.set_volume(0.3)  # Volume reduzido


# Define as cartas visíveis na tela
visible_cards = [False] * len(pairs)


# Define as variáveis de controle do jogo
game_over = False
first_card = None
second_card = None
first_card_index = None
second_card_index = None
score = [0, 0]  # Placar para dois jogadores
current_player = 0  # 0 para jogador 1, 1 para jogador 2
start_time = 0
reveal_time = 1000  # Tempo de revelação em milissegundos
waiting = False


# Variáveis para a tela inicial
start_screen = True
game_mode = None
button_width = 350
button_height = 70
button_spacing = 20
single_player_button_x = (screen_width - button_width) // 2
single_player_button_y = (screen_height // 2) - button_height - button_spacing
multiplayer_button_x = (screen_width - button_width) // 2
multiplayer_button_y = (screen_height // 2) + button_spacing


# Variáveis para controlar se o mouse está sobre os botões
mouse_over_single_player = False
mouse_over_multiplayer = False


# Cores
menu_bg_color = (100, 100, 200)  # Cor de fundo do menu
button_color_single = (0, 200, 0)  # Cor do botão single player
button_color_multi = (200, 200, 0)  # Cor do botão multiplayer
text_color = (255, 255, 255)  # Cor do texto
border_color = (0, 0, 0)  # Cor da borda das cartas


# Fonte para o título e botões
title_font = pygame.font.Font('arial.ttf', 72)  
button_font = pygame.font.Font('arial.ttf', 48)


# Fonte para o placar
score_font = pygame.font.Font('comicsansms.ttf', 36)


# Variáveis para a transição
transition = False
transition_alpha = 255  # Opacidade inicial (totalmente opaco)
transition_direction = 1  # 1 para fade in, -1 para fade out


# Loop principal do jogo
clock = pygame.time.Clock()
while not game_over:
    if start_screen:
        screen.fill(menu_bg_color)
        # Desenha a imagem de fundo do menu
        screen.blit(menu_background_image, (0, 0))
        # Desenha o título do jogo com borda
        title_text = title_font.render("Jogo de Memória", True, border_color)
        title_text_shadow = title_font.render("Jogo de Memória", True, text_color)
        title_x = (screen_width - title_text.get_width()) // 2
        title_y = (screen_height // 4)
        # Desenha o título com a borda
        screen.blit(title_text, (title_x - 3, title_y - 3))
        screen.blit(title_text, (title_x + 3, title_y - 3))
        screen.blit(title_text, (title_x - 3, title_y + 3))
        screen.blit(title_text, (title_x + 3, title_y + 3))
        screen.blit(title_text_shadow, (title_x, title_y))
        
        # Processa eventos da tela inicial
        for event in pygame.event.get():
            if event.type == QUIT:
                game_over = True
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if single_player_button_x <= mouse_x <= single_player_button_x + button_width and single_player_button_y <= mouse_y <= single_player_button_y + button_height:
                    game_mode = "single"
                    start_screen = False
                    transition = True  # Inicia a transição
                    transition_direction = -1  # Fade out
                    pygame.mixer.music.stop()  # Para a música de menu
                    pygame.mixer.music.load('background_music.mp3')  # Carrega a música de fundo do jogo
                    pygame.mixer.music.play(-1)  # Inicia a música de fundo do jogo
                elif multiplayer_button_x <= mouse_x <= multiplayer_button_x + button_width and multiplayer_button_y <= mouse_y <= multiplayer_button_y + button_height:
                    game_mode = "multiplayer"
                    start_screen = False
                    transition = True  # Inicia a transição
                    transition_direction = -1  # Fade out
                    pygame.mixer.music.stop()  # Para a música de menu
                    pygame.mixer.music.load('background_music.mp3')  # Carrega a música de fundo do jogo
                    pygame.mixer.music.play(-1)  # Inicia a música de fundo do jogo
            elif event.type == MOUSEMOTION:  # Adicionando esta verificação para detectar movimento do mouse
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if single_player_button_x <= mouse_x <= single_player_button_x + button_width and single_player_button_y <= mouse_y <= single_player_button_y + button_height:
                    mouse_over_single_player = True
                else:
                    mouse_over_single_player = False
                if multiplayer_button_x <= mouse_x <= multiplayer_button_x + button_width and multiplayer_button_y <= mouse_y <= multiplayer_button_y + button_height:
                    mouse_over_multiplayer = True
                else:
                    mouse_over_multiplayer = False
        
        # Adiciona sombra ao botão do modo single player
        shadow_color = (0, 0, 0, 50)  # Cor da sombra (com transparência)
        shadow_offset = 5  # Deslocamento da sombra
        shadow_rect = pygame.Rect(single_player_button_x + shadow_offset, single_player_button_y + shadow_offset, button_width, button_height)
        pygame.draw.rect(screen, shadow_color, shadow_rect)

        # Decide a cor e o tamanho do botão com base se o mouse está sobre ele ou não
        if mouse_over_single_player:
            button_color = (0, 255, 0)  # Nova cor quando o mouse está sobre o botão
            button_width_effect = button_width + 10  # Aumenta o tamanho horizontal
            button_height_effect = button_height + 10  # Aumenta o tamanho vertical
        else:
            button_color = button_color_single
            button_width_effect = button_width
            button_height_effect = button_height

        # Desenha o botão do modo single player com borda
        pygame.draw.rect(screen, border_color, (single_player_button_x - 2, single_player_button_y - 2, button_width_effect + 4, button_height_effect + 4), 2)
        pygame.draw.rect(screen, button_color, (single_player_button_x, single_player_button_y, button_width_effect, button_height_effect))
        single_player_text = button_font.render("Single Player", True, text_color)
        single_player_text_x = single_player_button_x + (button_width_effect - single_player_text.get_width()) // 2
        single_player_text_y = single_player_button_y + (button_height_effect - single_player_text.get_height()) // 2
        screen.blit(single_player_text, (single_player_text_x, single_player_text_y))
        
        # Adiciona sombra ao botão do modo multiplayer
        shadow_rect_multi = pygame.Rect(multiplayer_button_x + shadow_offset, multiplayer_button_y + shadow_offset, button_width, button_height)
        pygame.draw.rect(screen, shadow_color, shadow_rect_multi)

        # Decide a cor e o tamanho do botão com base se o mouse está sobre ele ou não
        if mouse_over_multiplayer:
            button_color = (255, 255, 0)  # Nova cor quando o mouse está sobre o botão
            button_width_effect = button_width + 10  # Aumenta o tamanho horizontal
            button_height_effect = button_height + 10  # Aumenta o tamanho vertical
        else:
            button_color = button_color_multi
            button_width_effect = button_width
            button_height_effect = button_height

        # Desenha o botão do modo multiplayer com borda
        pygame.draw.rect(screen, border_color, (multiplayer_button_x - 2, multiplayer_button_y - 2, button_width_effect + 4, button_height_effect + 4), 2)
        pygame.draw.rect(screen, button_color, (multiplayer_button_x, multiplayer_button_y, button_width_effect, button_height_effect))
        multiplayer_text = button_font.render("Multiplayer", True, text_color)
        multiplayer_text_x = multiplayer_button_x + (button_width_effect - multiplayer_text.get_width()) // 2
        multiplayer_text_y = multiplayer_button_y + (button_height_effect - multiplayer_text.get_height()) // 2
        screen.blit(multiplayer_text, (multiplayer_text_x, multiplayer_text_y))
    else:
        # Desenha a imagem de fundo do jogo
        screen.blit(game_background_image, (0, 0))
        # Processa eventos do jogo
        for event in pygame.event.get():
            if event.type == QUIT:
                game_over = True
            elif event.type == MOUSEBUTTONDOWN and not waiting:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, (x, y) in enumerate(card_positions):
                    if x <= mouse_x <= x + card_width and y <= mouse_y <= y + card_height:
                        if not visible_cards[i]:
                            visible_cards[i] = True
                            card = pairs[i]
                            if first_card is None:
                                first_card = card
                                first_card_index = i
                                card_flip_sound.play()  # Toca o som de flip da carta
                            elif second_card is None:
                                second_card = card
                                second_card_index = i
                                card_flip_sound.play()  # Toca o som de flip da carta
                                waiting = True
                                start_time = pygame.time.get_ticks()


        # Verifica se é hora de esconder as cartas não combinadas
        if waiting and pygame.time.get_ticks() - start_time > reveal_time:
            if first_card!= second_card:
                visible_cards[first_card_index] = False
                visible_cards[second_card_index] = False
                # Troca o jogador apenas se errar
                if game_mode == "multiplayer":
                    current_player = 1 - current_player
                first_card = None
                second_card = None
                first_card_index = None
                second_card_index = None
            else:
                card_match_sound.play()  # Toca o som de match
                visible_cards[first_card_index] = True
                visible_cards[second_card_index] = True
                if game_mode == "multiplayer":
                    score[current_player] += 1  # Incrementa o placar do jogador atual
                first_card = None
                second_card = None
                first_card_index = None
                second_card_index = None
            waiting = False


        # Desenha as cartas na tela
        for i, card in enumerate(pairs):
            x, y = card_positions[i]
            if visible_cards[i]:
                # Redimensiona a imagem para caber na carta
                card = pygame.transform.scale(card, (card_width, card_height))
                screen.blit(card, (x, y))
                # Desenha a borda escura
                pygame.draw.rect(screen, border_color, (x - 2, y - 2, card_width + 4, card_height + 4), 2)
            else:
                # Usa a imagem da carta virada
                card_back = pygame.transform.scale(card_back, (card_width, card_height))
                screen.blit(card_back, (x, y) )
                # Desenha a borda escura
                pygame.draw.rect(screen, border_color, (x - 2, y - 2, card_width + 4, card_height + 4), 2)


        # Desenha o placar apenas no modo multiplayer
        if game_mode == "multiplayer":
            score_text = score_font.render(f'Jogador 1: {score[0]} | Jogador 2: {score[1]}', True, (0, 0, 0))
            score_text_shadow = score_font.render(f'Jogador 1: {score[0]} | Jogador 2: {score[1]}', True, (50, 50, 50))  # Texto de sombra
            score_rect = score_text.get_rect()
            score_rect.topleft = (10, 10)
            score_rect_shadow = score_text_shadow.get_rect()
            score_rect_shadow.topleft = (12, 12)  # Deslocamento da sombra

            # Desenha um retângulo com bordas arredondadas atrás do placar
            pygame.draw.rect(screen, (200, 200, 200), score_rect.inflate(20, 10), border_radius=10)  # Retângulo com bordas arredondadas
            screen.blit(score_text_shadow, score_rect_shadow)  # Desenha a sombra do texto
            screen.blit(score_text, score_rect)  # Desenha o texto do placar


        # Verifica se o jogo acabou (todos os pares foram encontrados)
        pairs_found = sum([1 for visible in visible_cards if visible]) // 2
        if pairs_found == len(card_images):
            # Mostra a mensagem de fim de jogo
            end_font = pygame.font.SysFont(None, 72)
            if game_mode == "multiplayer":
                if score[0] > score[1]:
                    end_text = end_font.render("Jogador 1 Venceu! Pressione R para reiniciar ou Q para sair", True, (0, 0, 0) )
                elif score[1] > score[0]:
                    end_text = end_font.render("Jogador 2 Venceu! Pressione R para reiniciar ou Q para sair", True, (0, 0, 0) )
                else:
                    end_text = end_font.render("Empate! Pressione R para reiniciar ou Q para sair", True, (0, 0, 0) )
            else:
                end_text = end_font.render("O jogador venceu! Pressione R para reiniciar ou Q para sair", True, (0, 0, 0) )
            screen.blit(end_text, (screen_width // 2 - end_text.get_width() // 2, screen_height // 2 - end_text.get_height() // 2) )


        # Verifica se o jogador quer reiniciar ou sair
        if pairs_found == len(card_images):
            if event.type == KEYDOWN:
                if event.key == K_r:
                    # Reinicia as variáveis do jogo
                    pairs = [card for card in card_images for _ in range(2)]
                    random.shuffle(pairs)
                    visible_cards = [False] * len(pairs)
                    score = [0, 0]
                    first_card = None
                    second_card = None
                    first_card_index = None
                    second_card_index = None
                    waiting = False
                    if game_mode == "multiplayer":
                        current_player = 0
                elif event.key == K_q:
                    game_over = True


    # Transição
    if transition:
        transition_surface = pygame.Surface((screen_width, screen_height))
        transition_surface.fill((0, 0, 0))  # Pode ser outra cor se preferir
        transition_surface.set_alpha(transition_alpha)
        screen.blit(transition_surface, (0, 0))
        transition_alpha += 5 * transition_direction
        if transition_alpha <= 0:
            transition = False
            transition_alpha = 0
        elif transition_alpha >= 255:
            transition = False
            transition_alpha = 255


    # Atualiza a tela
    pygame.display.flip()


    # Controla a taxa de atualização
    clock.tick(30)


# Sai do Pygame
pygame.quit()