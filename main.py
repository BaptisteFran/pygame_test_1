import logging

import pygame

#LOGS
logging.basicConfig(level=logging.ERROR, filename="logs/app.log", filemode="a", format='%(asctime)s : %(levelname)s %(message)s')

pygame.init()
clock = pygame.time.Clock() # fps thing, can tick to whatever you want
dt = 0 # deltaTime
screen = pygame.display.set_mode((800, 600))
running = True

"""
PLAYER 1
"""
player_pos = pygame.Vector2(20 , screen.get_height() / 2)
direction1 = pygame.Vector2(0, 0)
speed = 300

"""
PLAYER 2
"""
player2_pos = pygame.Vector2(screen.get_width() - 40 , screen.get_height() / 2)
direction2 = pygame.Vector2(0, 0)


"""
MOVING CIRCLE
"""
circle_position = pygame.Vector2() # init circle at (0,0)
circle_radius = 15
circle_movement = pygame.Vector2(1,1) # init circle movement at (1,1)


def check_collision(circle_pos, circle_radius, rect, circle_movement):
    # Trouver le point le plus proche du centre du cercle sur le rectangle
    closest_x = max(rect.left, min(circle_pos.x, rect.right))
    closest_y = max(rect.top, min(circle_pos.y, rect.bottom))
    # Calculer la distance entre ce point et le centre du cercle
    distance_x = circle_pos.x - closest_x
    distance_y = circle_pos.y - closest_y
    distance_squared = distance_x ** 2 + distance_y ** 2
    # Si le cercle est en collision avec le rectangle
    if distance_squared <= circle_radius ** 2:
        # collision
        # Déterminer le côté de la collision
        if abs(distance_x) > abs(distance_y):
            # Collision sur les côtés gauche ou droit
            circle_movement.x = -circle_movement.x
        else:
            # Collision sur le dessus ou le dessous
            circle_movement.y = -circle_movement.y


# Main loop
while running:
    dt = clock.tick(60) / 1000 # initialize first so its not equals to 0 when we use it
    for event in pygame.event.get():
       if event.type == pygame.QUIT: # pygame.QUIT = cross on the top right corner
                running = False

    screen.fill((201,203,206)) # put some color in the background (grey)

    # draw player1 rect
    rect = pygame.draw.rect(screen, (90, 90, 90, 255), pygame.Rect(player_pos.x, player_pos.y, 20, 150))

    # player2
    rect2 = pygame.draw.rect(screen, (90, 90, 90, 255), pygame.Rect(player2_pos.x, player2_pos.y, 20, 150))

    # draw ball
    circle = pygame.draw.circle(screen, (255,255,255), circle_position, circle_radius)

    circle_position.x += circle_movement.x * speed * dt
    circle_position.y += circle_movement.y * speed * dt

    if circle_position.x > screen.get_width() or circle_position.x < 0:
        circle_movement.x *= -1
    if circle_position.y > screen.get_height() or circle_position.y < 0:
        circle_movement.y *= -1

    check_collision(circle_position, circle_radius, rect, circle_movement)
    check_collision(circle_position, circle_radius, rect2, circle_movement)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False

    # set direction to a new vector2, it should be equal to (0,0)
    direction1 = pygame.Vector2()
    direction2 = pygame.Vector2()

    #logging.debug("Direction : " + str(direction))

    if keys[pygame.K_z]:
        direction1.y -= 1
    if keys[pygame.K_s]:
        direction1.y += 1
    if keys[pygame.K_UP]:
        direction2.y -= 1
    if keys[pygame.K_DOWN]:
        direction2.y += 1

    # if direction is not (0,0)
    if direction1 != pygame.Vector2():
        direction1.normalize_ip() # normalize so it has a constant speed
        # limit player so it doesn't go over the top or bottom
        if rect.top <= 0 and direction1 == pygame.Vector2(0, -1):
            player_pos = player_pos
        elif rect.bottom >= screen.get_height() and direction1 == pygame.Vector2(0, 1):
            player_pos = player_pos
        else:
            player_pos += direction1 * dt * speed # add deltaTime and speed

    # if direction is not (0,0)
    if direction2 != pygame.Vector2():
        direction2.normalize_ip()  # normalize so it has a constant speed
        if rect2.top <= 0 and direction2 == pygame.Vector2(0, -1):
            player2_pos = player2_pos
        elif rect2.bottom >= screen.get_height() and direction2 == pygame.Vector2(0, 1):
            player2_pos = player2_pos
        else:
            player2_pos += direction2 * dt * speed # add deltaTime and speed





    pygame.display.flip()
pygame.quit()
