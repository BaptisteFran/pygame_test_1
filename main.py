import logging
import sys

import pygame

from scripts.player import Player


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
        self.player = Player(game=self, name="player_1", x=20, y=(self.screen.get_height() // 2) - 75, speed=300)


        """
        PLAYER 2
        """
        self.player_2 = Player(game=self, name="player_2", x=self.screen.get_width() - 40, y=(self.screen.get_height() // 2) - 75, speed=300)

        """
        MOVING CIRCLE
        """
        self.speed = 300
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

            # draw ball
            circle = pygame.draw.circle(self.screen, (255, 255, 255), self.circle_position, self.circle_radius)

            self.circle_position.x += self.circle_movement.x * self.speed * dt
            self.circle_position.y += self.circle_movement.y * self.speed * dt

            if self.circle_position.x > self.screen.get_width() or self.circle_position.x < 0:
                self.circle_movement.x *= -1
            if self.circle_position.y > self.screen.get_height() or self.circle_position.y < 0:
                self.circle_movement.y *= -1

            self.check_collision(self.circle_position, self.circle_radius, self.player.rect, self.circle_movement)
            self.check_collision(self.circle_position, self.circle_radius, self.player_2.rect, self.circle_movement)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

            self.player.draw(self.screen)
            self.player.move(keys, dt)

            self.player_2.draw(self.screen)
            self.player_2.move(keys, dt)

            # logging.debug("Direction : " + str(direction))

            pygame.display.update()

Game().run()


