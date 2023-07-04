import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500  # Dimensions of the game window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Create the game window
pygame.display.set_caption("Woosh Woosh!")  # Set the window caption

WHITE = (255, 255, 255)  # Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)  # Border line in the middle of the window

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))  # Sound effects
BULLET_HIT_SOUND.set_volume(.1)
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
BULLET_FIRE_SOUND.set_volume(.1)

HEALTH_FONT = pygame.font.SysFont('comicsans', 35)  # Fonts for displaying health and winner
WINNER_FONT = pygame.font.SysFont('comicsans', 65)

FPS = 60  # Frames per second
VEL = 5  # Velocity of the spaceships
BULLETS_VEL = 7  # Velocity of the bullets
MAX_BULLETS = 3  # Maximum number of bullets a spaceship can shoot
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40  # Dimensions of the spaceships

YELLOW_HIT = pygame.USEREVENT + 1  # Custom events
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))  # Spaceship images
YELLOW_SPACESHIP =\
    pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_red.png'))
RED_SPACESHIP =\
    pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))  # Background image


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    """
    Draw the game window with all the game elements.

    :param red: Red spaceship rectangle
    :param yellow: Yellow spaceship rectangle
    :param red_bullets: List of red bullets
    :param yellow_bullets: List of yellow bullets
    :param red_health: Red spaceship health
    :param yellow_health: Yellow spaceship health
    """
    WIN.blit(SPACE, (0, 0))  # Draw the background image
    pygame.draw.rect(WIN, BLACK, BORDER)  # Draw the border line

    red_health_text = HEALTH_FONT.render("Health" + str(red_health), 1, WHITE)  # Render health text for red spaceship
    yellow_health_text = HEALTH_FONT.render("Health" + str(yellow_health), 1, WHITE)  # Render health text for yellow spaceship
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))  # Draw red health text
    WIN.blit(yellow_health_text, (10, 10))  # Draw yellow health text

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))  # Draw yellow spaceship
    WIN.blit(RED_SPACESHIP, (red.x, red.y))  # Draw red spaceship

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)  # Draw red bullets

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)  # Draw yellow bullets

    pygame.display.update()  # Update the game window


def yellow_handle_movement(keys_pressed, yellow):
    """
    Handle the movement of the yellow spaceship based on the keys pressed.

    :param keys_pressed: A list of booleans representing the state of each key
    :param yellow: Yellow spaceship rectangle
    """
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    """
    Handle the movement of the red spaceship based on the keys pressed.

    :param keys_pressed: A list of booleans representing the state of each key
    :param red: Red spaceship rectangle
    """
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    """
    Handle the movement and collisions of the bullets.

    :param yellow_bullets: List of yellow bullets
    :param red_bullets: List of red bullets
    :param yellow: Yellow spaceship rectangle
    :param red: Red spaceship rectangle
    """
    for bullet in yellow_bullets:
        bullet.x += BULLETS_VEL  # Move the yellow bullets horizontally

        if red.colliderect(bullet):  # Check for collision with the red spaceship
            pygame.event.post(pygame.event.Event(RED_HIT))  # Post a custom event for red hit
            yellow_bullets.remove(bullet)  # Remove the bullet
        elif bullet.x > WIDTH:  # If the bullet goes off-screen, remove it
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLETS_VEL  # Move the red bullets horizontally

        if yellow.colliderect(bullet):  # Check for collision with the yellow spaceship
            pygame.event.post(pygame.event.Event(YELLOW_HIT))  # Post a custom event for yellow hit
            red_bullets.remove(bullet)  # Remove the bullet
        elif bullet.x < 0:  # If the bullet goes off-screen, remove it
            red_bullets.remove(bullet)


def draw_winner(text):
    """
    Draw the winner text on the screen.

    :param text: Winner text
    """
    draw_text = WINNER_FONT.render(text, 1, WHITE)  # Render the winner text
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))  # Draw the winner text
    pygame.display.update()  # Update the game window
    pygame.time.delay(2000)  # Delay for 2 seconds


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)  # Initialize the red spaceship rectangle
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)  # Initialize the yellow spaceship rectangle

    red_bullets = []  # Initialize the list of red bullets
    yellow_bullets = []  # Initialize the list of yellow bullets

    red_health = 10  # Initialize the red spaceship health
    yellow_health = 10  # Initialize the yellow spaceship health

    clock = pygame.time.Clock()  # Create a clock object to control the frame rate

    run = True
    while run:
        clock.tick(FPS)  # Control the frame rate
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the close button is clicked, quit the game
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:  # Shoot yellow bullet
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:  # Shoot red bullet
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:  # If red spaceship is hit by a bullet
                red_health -= 1  # Decrease red spaceship health
                BULLET_HIT_SOUND.play()  # Play bullet hit sound

            if event.type == YELLOW_HIT:  # If yellow spaceship is hit by a bullet
                yellow_health -= 1  # Decrease yellow spaceship health
                BULLET_HIT_SOUND.play()  # Play bullet hit sound

        winner_text = ""
        if red_health <= 0:  # If red spaceship health is depleted
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:  # If yellow spaceship health is depleted
            winner_text = "Red Wins!"

        if winner_text != "":  # If there is a winner
            draw_winner(winner_text)  # Draw the winner text
            break

        keys_pressed = pygame.key.get_pressed()  # Get the state of all keys
        yellow_handle_movement(keys_pressed, yellow)  # Handle yellow spaceship movement
        red_handle_movement(keys_pressed, red)  # Handle red spaceship movement

        handle_bullets(yellow_bullets, red_bullets, yellow, red)  # Handle bullets movement and collisions

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)  # Draw the game window

    main()  # Recursive call to start a new game if there is no winner


if __name__ == "__main__":
    main()
