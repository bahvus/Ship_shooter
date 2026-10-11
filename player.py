import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS,LINE_WIDTH,PLAYER_TURN_SPEED,PLAYER_SPEED,PLAYER_SHOOT_SPEED,PLAYER_SHOOT_COOLDOWN_SECONDS
from shot import Shot


class Player(CircleShape):

    def __init__(self,x,y):
        super().__init__(x,y,PLAYER_RADIUS)
        self.rotation = 0
        self.cool_down = 0

    # in the Player class
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self,screen):
        pygame.draw.polygon(screen,"white",self.triangle(),LINE_WIDTH)

    def rotate(self,dt: float) -> None:
        self.rotation += PLAYER_TURN_SPEED*dt

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            if self.cool_down > 0:
                self.cool_down -= dt
            else:
                self.shoot()
                self.cool_down = PLAYER_SHOOT_COOLDOWN_SECONDS

    def shoot(self) -> None:
        unit_vector = pygame.Vector2(0, 1).rotate(self.rotation)
        shot = Shot(self.position[0],self.position[1])
        shot.velocity = unit_vector*PLAYER_SHOOT_SPEED

    def move(self,dt:float) -> None:
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector
