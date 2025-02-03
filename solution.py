import pygame  # Importa el módulo pygame para crear juegos
pygame.init()  # Inicializa todos los módulos de pygame

# Configuración de la ventana principal
WIDTH, HEIGHT = 700, 500  # Define el ancho y alto de la ventana
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Crea la ventana con las dimensiones especificadas
pygame.display.set_caption("Pong")  # Establece el título de la ventana

FPS = 60  # Define la cantidad de cuadros por segundo (frames per second)

# Definición de colores en formato RGB
WHITE = (255, 255, 255)  # Color blanco
BLACK = (0, 0, 0)  # Color negro

# Dimensiones de las paletas y la pelota
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100  # Ancho y alto de las paletas
BALL_RADIUS = 7  # Radio de la pelota

# Fuente y puntuación ganadora
SCORE_FONT = pygame.font.SysFont("comicsans", 50)  # Fuente para mostrar la puntuación
WINNING_SCORE = 10  # Puntuación necesaria para ganar

class Paddle:
    COLOR = WHITE  # Color de la paleta
    VEL = 4  # Velocidad de movimiento de la paleta

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x  # Posición x inicial y actual de la paleta
        self.y = self.original_y = y  # Posición y inicial y actual de la paleta
        self.width = width  # Ancho de la paleta
        self.height = height  # Alto de la paleta

    def draw(self, win):
        # Dibuja un rectángulo en la ventana con las coordenadas y dimensiones de la paleta
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        # Mueve la paleta hacia arriba o hacia abajo
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        # Restablece la posición de la paleta a su posición original
        self.x = self.original_x
        self.y = self.original_y

class Ball:
    MAX_VEL = 5  # Velocidad máxima de la pelota
    COLOR = WHITE  # Color de la pelota

    def __init__(self, x, y, radius):
        self.x = self.original_x = x  # Posición x inicial y actual de la pelota
        self.y = self.original_y = y  # Posición y inicial y actual de la pelota
        self.radius = radius  # Radio de la pelota
        self.x_vel = self.MAX_VEL  # Velocidad en el eje x
        self.y_vel = 0  # Velocidad en el eje y

    def draw(self, win):
        # Dibuja un círculo en la ventana con las coordenadas y el radio de la pelota
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        # Mueve la pelota según sus velocidades en los ejes x e y
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        # Restablece la posición y velocidad de la pelota a sus valores originales
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1  # Invierte la dirección de la velocidad en el eje x

def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)  # Rellena la ventana con el color negro

    # Renderiza y muestra las puntuaciones de los jugadores
    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width()//2, 20))

    # Dibuja las paletas en la ventana
    for paddle in paddles:
        paddle.draw(win)

    # Dibuja la línea central de la cancha
    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))

    ball.draw(win)  # Dibuja la pelota en la ventana
    pygame.display.update()  # Actualiza la pantalla para reflejar los cambios

def handle_collision(ball, left_paddle, right_paddle):
    # Maneja las colisiones de la pelota con las paredes superior e inferior
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    # Maneja las colisiones de la pelota con las paletas
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

def handle_paddle_movement(keys, left_paddle, right_paddle):
    # Maneja el movimiento de las paletas según las teclas presionadas
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)

def main():
    run = True  # Variable para controlar el bucle principal
    clock = pygame.time.Clock()  # Crea un objeto para controlar el tiempo y mantener una tasa de FPS constante

    # Crea las paletas y la pelota en sus posiciones iniciales
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    left_score = 0  # Puntuación inicial del jugador izquierdo
    right_score = 0  # Puntuación inicial del jugador derecho

    while run:
        clock.tick(FPS)  # Controla la cantidad de cuadros por segundo
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)  # Dibuja las paletas y la pelota en la ventana

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Verifica si se ha cerrado la ventana
                run = False  # Termina el bucle principal
                break

        keys = pygame.key.get_pressed()  # Obtiene el estado de todas las teclas
        handle_paddle_movement(keys, left_paddle, right_paddle)  # Maneja el movimiento de las paletas

        ball.move()  # Mueve la pelota
        handle_collision(ball, left_paddle, right_paddle)  # Maneja las colisiones de la pelota

        # Actualiza la puntuación si la pelota sale de los límites
        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()

        # Verifica si algún jugador ha ganado
        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Left Player Won!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right Player Won!"

        if won:
            # Muestra el texto de victoria y reinicia el juego después de una pausa
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_width() // 2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()  # Cierra pygame

if __name__ == '__main__':
    main()  # Ejecuta la función principal si el archivo se ejecuta directamente