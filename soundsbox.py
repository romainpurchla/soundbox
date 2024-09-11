import pygame
import os

# Initialiser Pygame
pygame.init()

# Dimensions de la fenêtre
window_width, window_height = 480, 320
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Lecteur de Sons")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (100, 150, 250)
HOVER_COLOR = (150, 200, 255)
SCROLL_BUTTON_COLOR = (200, 100, 100)

# Initialiser le mixer pour les sons
pygame.mixer.init()

# Dossier contenant les fichiers sons
SOUNDS_DIR = "./sounds/"
sounds = [f for f in os.listdir(SOUNDS_DIR) if f.endswith('.mp3') or f.endswith('.wav')]

# Taille des cartes
card_width, card_height = 240, 100
scroll_speed = 10  # Augmenter la vitesse du défilement

# Taille des boutons de défilement
scroll_button_width, scroll_button_height = 100, 100

# Fonction pour dessiner une carte
def draw_card(text, rect, hover=False):
    color = HOVER_COLOR if hover else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=10)
    # Dessiner le texte sur la carte
    font = pygame.font.SysFont(None, 24)
    lines = [text[i:i+20] for i in range(0, len(text), 20)]  # Diviser le texte en lignes
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, WHITE)
        text_rect = text_surface.get_rect(center=(rect.centerx, rect.top + 10 + i * 24))
        screen.blit(text_surface, text_rect)

# Fonction pour dessiner un bouton
def draw_button(text, rect, color, hover=False):
    button_color = HOVER_COLOR if hover else color
    pygame.draw.rect(screen, button_color, rect, border_radius=10)
    font = pygame.font.SysFont(None, 24)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

# Fonction pour jouer le son
def play_sound(sound_file):
    try:
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {sound_file}\n{e}")

# Position de départ des cartes pour le défilement
scroll_x = 0

# Fonction pour dessiner les boutons de défilement
def draw_scroll_buttons():
    # Bouton gauche
    left_button = pygame.Rect(10, window_height // 2 - scroll_button_height // 2  + 50, scroll_button_width, scroll_button_height)
    draw_button("<", left_button, SCROLL_BUTTON_COLOR)

    # Bouton droit
    right_button = pygame.Rect(window_width - 10 - scroll_button_width, window_height // 2 - scroll_button_height // 2 + 50, scroll_button_width, scroll_button_height)
    draw_button(">", right_button, SCROLL_BUTTON_COLOR)

    return left_button, right_button

# Variables pour maintenir le défilement
scrolling_left = False
scrolling_right = False

# Boucle principale de l'application
running = True
while running:
    screen.fill(WHITE)

    # Dessiner les cartes avec défilement horizontal
    y = 50
    for i, sound in enumerate(sounds):
        rect = pygame.Rect(scroll_x + i * (card_width + 20), y, card_width, card_height)
        mouse_pos = pygame.mouse.get_pos()
        hover = rect.collidepoint(mouse_pos)
        draw_card(sound, rect, hover)

        # Vérifier les clics sur les cartes
        if hover and pygame.mouse.get_pressed()[0]:
            play_sound(os.path.join(SOUNDS_DIR, sound))

    # Dessiner les boutons de défilement
    left_button, right_button = draw_scroll_buttons()

    # Gérer les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                scrolling_left = True
            elif event.key == pygame.K_RIGHT:
                scrolling_right = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scrolling_left = False
            elif event.key == pygame.K_RIGHT:
                scrolling_right = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if left_button.collidepoint(event.pos):
                scrolling_left = True
            elif right_button.collidepoint(event.pos):
                scrolling_right = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if left_button.collidepoint(event.pos):
                scrolling_left = False
            elif right_button.collidepoint(event.pos):
                scrolling_right = False

    # Mettre à jour la position de défilement
    if scrolling_left:
        scroll_x += scroll_speed
    if scrolling_right:
        scroll_x -= scroll_speed

    # Limiter le défilement pour ne pas aller au-delà des limites
    max_scroll_x = -len(sounds) * (card_width + 20) + window_width
    if scroll_x > 0:
        scroll_x = 0
    elif scroll_x < max_scroll_x:
        scroll_x = max_scroll_x

    pygame.display.flip()

# Quitter Pygame
pygame.quit()
