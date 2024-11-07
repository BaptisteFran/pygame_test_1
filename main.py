import logging
import sys

import pygame


class Game:
    def __init__(self):
        # LOGS
        logging.basicConfig(level=logging.ERROR, filename="logs/app.log", filemode="a",
                            format='%(asctime)s : %(levelname)s %(message)s')

        pygame.init()
        pygame.display.set_caption('Pong Test')
        self.clock = pygame.time.Clock()  # fps thing, can tick to whatever you want
        self.dt = 0  # deltaTime
        self.screen = pygame.display.set_mode((800, 600))
        self.display = pygame.Surface((320, 240), pygame.SRCALPHA)  # set viewport to half the resolution (pixel art)
        self.running = True

        """
        PLAYER 1
        """
        self.player_pos = pygame.Vector2(20, self.screen.get_height() / 2)
        self.direction1 = pygame.Vector2(0, 0)
        self.speed = 300

        """
        PLAYER 2
        """
        self.player2_pos = pygame.Vector2(self.screen.get_width() - 40, self.screen.get_height() / 2)
        self.direction2 = pygame.Vector2(0, 0)

        """
        MOVING CIRCLE
        """
        self.circle_position = pygame.Vector2()  # init circle at (0,0)
        self.circle_radius = 15
        self.circle_movement = pygame.Vector2(1, 1)  # init circle movement at (1,1)

    def check_collision(self, circle_pos, circle_radius, rect, circle_movement):
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

    def run(self):
        # Main loop
        while True:
            self.display.fill((0, 0, 0, 0))
            dt = self.clock.tick(60) / 1000  # initialize first so its not equals to 0 when we use it
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # pygame.QUIT = cross on the top right corner
                    pygame.quit()
                    sys.exit()

            self.screen.fill((201, 203, 206))  # put some color in the background (grey)

            # draw player1 rect
            rect = pygame.draw.rect(self.screen, (90, 90, 90, 255), pygame.Rect(self.player_pos.x, self.player_pos.y, 20, 150))

            # player2
            rect2 = pygame.draw.rect(self.screen, (90, 90, 90, 255), pygame.Rect(self.player2_pos.x, self.player2_pos.y, 20, 150))

            # draw ball
            circle = pygame.draw.circle(self.screen, (255, 255, 255), self.circle_position, self.circle_radius)

            self.circle_position.x += self.circle_movement.x * self.speed * dt
            self.circle_position.y += self.circle_movement.y * self.speed * dt

            if self.circle_position.x > self.screen.get_width() or self.circle_position.x < 0:
                self.circle_movement.x *= -1
            if self.circle_position.y > self.screen.get_height() or self.circle_position.y < 0:
                self.circle_movement.y *= -1

            self.check_collision(self.circle_position, self.circle_radius, rect, self.circle_movement)
            self.check_collision(self.circle_position, self.circle_radius, rect2, self.circle_movement)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

            # set direction to a new vector2, it should be equal to (0,0)
            direction1 = pygame.Vector2()
            direction2 = pygame.Vector2()

            # logging.debug("Direction : " + str(direction))

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
                direction1.normalize_ip()  # normalize so it has a constant speed
                if rect.top <= 0 and direction1 == pygame.Vector2(0, -1):
                    self.player_pos = self.player_pos
                elif rect.bottom >= self.screen.get_height() and direction1 == pygame.Vector2(0, 1):
                    self.player_pos = self.player_pos
                else:
                    self.player_pos += direction1 * dt * self.speed  # add deltaTime and speed

            # if direction is not (0,0)
            if direction2 != pygame.Vector2():
                direction2.normalize_ip()  # normalize so it has a constant speed
                if rect2.top <= 0 and direction2 == pygame.Vector2(0, -1):
                    self.player2_pos = self.player2_pos
                elif rect2.bottom >= self.screen.get_height() and direction2 == pygame.Vector2(0, 1):
                    self.player2_pos = self.player2_pos
                else:
                    self.player2_pos += direction2 * dt * self.speed  # add deltaTime and speed

            pygame.display.update()

Game().run()


