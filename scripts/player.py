import pygame

class Player:
    def __init__(self, game, name, x, y, speed):
        self.image = pygame.image.load("data/assets/player/player.png")
        self.game = game
        self.name = name
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.speed = speed

    def move(self, keys, delta_time):
        direction = pygame.Vector2()
        if self.name == "player_1":
            if keys[pygame.K_z]:
                direction.y += -1
            if keys[pygame.K_s]:
                direction.y += 1
        else:
            if keys[pygame.K_UP]:
                direction.y += -1
            if keys[pygame.K_DOWN]:
                direction.y += 1

        if direction != pygame.Vector2():
            direction.normalize_ip()  # normalize so it has a constant speed
            if self.rect.top <= 0 and direction == pygame.Vector2(0, -1):
                self.rect.y = self.rect.y
            elif self.rect.bottom >= self.game.screen.get_height() and direction == pygame.Vector2(0, 1):
                self.rect.y = self.rect.y
            else:
                self.rect.y += direction.y * self.speed * delta_time  # add deltaTime and speed


    def draw(self, screen):
        screen.blit(self.image, self.rect)

    """
    Should use AABB collisions which are better to check for rects collisions
    AABB (Axis-Aligned Bounding Box)
    Simple & fast
    Enough precision
    """
    def check_collision(self, other_rect):
        #colliderect(other_rect)
        pass