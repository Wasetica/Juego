import pygame
import random
import sys
import os

# Configurar el directorio de trabajo para evitar problemas con rutas
os.chdir(os.path.dirname(__file__))

# Inicializar PyGame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Ruta base del proyecto
BASE_PATH = os.path.dirname(__file__)

# Imágenes
def load_image(filename):
    filepath = os.path.join(BASE_PATH, filename)
    if not os.path.exists(filepath):
        print(f"Error: No se encontró el archivo '{filename}' en '{BASE_PATH}'")
        sys.exit()
    return pygame.image.load(filepath)

try:
    player_img = load_image("player.jpg.jpg")
    asteroid_img = load_image("asteroid.jpg.jpg")
    background = load_image("background.jpg.jpeg")
    print("Imágenes cargadas correctamente.")
except Exception as e:
    print(f"Error al cargar imágenes: {e}")
    sys.exit()

# Escalar imágenes
player_img = pygame.transform.scale(player_img, (50, 50))
asteroid_img = pygame.transform.scale(asteroid_img, (50, 50))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Clases
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 60
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, 50, 50)

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - 50:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < HEIGHT - 50:
            self.y += self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        screen.blit(player_img, (self.x, self.y))


class Asteroid:
    def __init__(self, speed):
        self.x = random.randint(0, WIDTH - 50)
        self.y = random.randint(-100, -40)
        self.speed = speed
        self.rect = pygame.Rect(self.x, self.y, 50, 50)

    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = random.randint(-100, -40)
            self.x = random.randint(0, WIDTH - 50)
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        screen.blit(asteroid_img, (self.x, self.y))


# Función para mostrar texto en la pantalla
def draw_text(text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)


# Función para mostrar el menú de dificultad
def show_difficulty_menu():
    screen.blit(background, (0, 0))
    draw_text("Selecciona la dificultad", 64, WIDTH // 2, HEIGHT // 2 - 100)
    draw_text("1 - Fácil", 36, WIDTH // 2, HEIGHT // 2 - 20)
    draw_text("2 - Medio", 36, WIDTH // 2, HEIGHT // 2 + 20)
    draw_text("3 - Difícil", 36, WIDTH // 2, HEIGHT // 2 + 60)
    pygame.display.update()


# Función principal
def main():
    run = True
    clock = pygame.time.Clock()
    player = Player()
    asteroids = []
    score = 0
    game_over = False
    paused = False
    in_menu = True  # Variable para controlar el menú de dificultad
    difficulty = 1  # Dificultad por defecto

    while run:
        clock.tick(30)
        screen.blit(background, (0, 0))

        # Menú de dificultad
        if in_menu:
            show_difficulty_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        difficulty = 1
                        in_menu = False
                    if event.key == pygame.K_2:
                        difficulty = 2
                        in_menu = False
                    if event.key == pygame.K_3:
                        difficulty = 3
                        in_menu = False
            continue

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Pausar/reanudar con la tecla P
                    paused = not paused

        if not game_over and not paused:
            keys = pygame.key.get_pressed()
            player.move(keys)
            player.draw()

            # Crear asteroides según la dificultad
            if len(asteroids) < 5 + difficulty * 2:
                asteroids.append(Asteroid(difficulty + random.randint(1, 3)))

            for asteroid in asteroids:
                asteroid.move()
                asteroid.draw()

                # Detectar colisiones
                if player.rect.colliderect(asteroid.rect):
                    game_over = True

            # Actualizar puntuación
            score += 1
            draw_text(f"Puntuación: {score}", 36, WIDTH // 2, 10)

        elif game_over:
            draw_text("Game Over", 64, WIDTH // 2, HEIGHT // 2 - 50)
            draw_text(f"Puntuación final: {score}", 36, WIDTH // 2, HEIGHT // 2 + 20)
            draw_text("Presiona R para reiniciar", 24, WIDTH // 2, HEIGHT // 2 + 80)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                game_over = False
                player = Player()
                asteroids = []
                score = 0
                in_menu = True  # Volver al menú de dificultad

        elif paused:  # Mostrar menú de pausa
            draw_text("Pausa", 64, WIDTH // 2, HEIGHT // 2 - 50)
            draw_text("Presiona P para reanudar", 24, WIDTH // 2, HEIGHT // 2 + 20)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    print("Iniciando el juego...")
    main()
    print("Juego terminado.")