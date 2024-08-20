import pygame
import random

# Inicializar Pygame y el mezclador de música
pygame.init()
pygame.mixer.init()

# Cargar y reproducir la música de fondo
pygame.mixer.music.load('sound/musica.mp3')
pygame.mixer.music.set_volume(0.5)  # Ajusta el volumen (0.0 a 1.0)
pygame.mixer.music.play(-1)  # -1 para reproducir en bucle

# Cargar efectos de sonido
collision_sound = pygame.mixer.Sound('sound/choque.mp3')

# Configuración de la ventana
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Carreras con Obstáculos")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# FPS
CLOCK = pygame.time.Clock()
FPS = 60

# Cargar imágenes
TRACK_IMAGE = pygame.image.load('images/pista.png')
TRACK_IMAGE = pygame.transform.scale(TRACK_IMAGE, (WIDTH, HEIGHT))

VEHICLE_IMAGE = pygame.image.load('images/carrito.png')
VEHICLE_IMAGE = pygame.transform.scale(VEHICLE_IMAGE, (60, 110))

OBSTACLE_IMAGE = pygame.image.load('images/obstaculo.png')
OBSTACLE_IMAGE = pygame.transform.scale(OBSTACLE_IMAGE, (60, 110))  # Ajusta el tamaño según sea necesario

# Clase para el Vehículo
class Vehicle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = VEHICLE_IMAGE
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed

        # Limitar el movimiento del vehículo a la ventana
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

# Clase para los Obstáculos
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = OBSTACLE_IMAGE
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-150, -self.rect.height)
        self.speed = random.randint(2, 6)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.kill()

# Crear instancias y grupos de sprites
vehicle = Vehicle()
all_sprites = pygame.sprite.Group()
all_sprites.add(vehicle)

obstacles = pygame.sprite.Group()

def spawn_obstacle():
    if random.random() < 0.02:
        obstacle = Obstacle()
        all_sprites.add(obstacle)
        obstacles.add(obstacle)

# Función para verificar colisiones
def check_collisions():
    if pygame.sprite.spritecollideany(vehicle, obstacles):
        collision_sound.play()  # Reproducir sonido de colisión
        return True
    return False

# Función para dibujar la puntuación
score = 0
def draw_score():
    global score
    font = pygame.font.SysFont(None, 36)
    text = font.render(f'PUNTAJE: {score}', True, BLACK)
    WIN.blit(text, (10, 10))

# Pantalla de fin del juego
def game_over_screen():
    font = pygame.font.SysFont(None, 74)
    text = font.render('PERDISTE EL JUEGO', True, RED)
    WIN.blit(text, (WIDTH // 4, HEIGHT // 3))
    score_font = pygame.font.SysFont(None, 36)
    score_text = score_font.render(f'PUNTUACION FINAL: {score}', True, BLACK)
    WIN.blit(score_text, (WIDTH // 3, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(2000)  # Esperar 2 segundos para que el jugador vea el mensaje

def reset_game():
    global score
    score = 0
    all_sprites.empty()
    obstacles.empty()
    all_sprites.add(vehicle)

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Actualizar
    all_sprites.update()
    spawn_obstacle()

    # Verificar colisiones
    if check_collisions():
        game_over_screen()
        reset_game()  # Reiniciar el juego

    # Incrementar puntuación
    score += 1

    # Dibujar
    WIN.blit(TRACK_IMAGE, (0, 0))  # Dibujar la pista en el fondo
    all_sprites.draw(WIN)
    draw_score()

    pygame.display.flip()
    CLOCK.tick(FPS)

pygame.quit()
