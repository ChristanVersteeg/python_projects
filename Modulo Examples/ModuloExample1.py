import pygame

pygame.init()
clock = pygame.time.Clock()

resolution = pygame.math.Vector2(800, 600)
sprite_position = resolution / 2 + pygame.math.Vector2(0, -250)
screen = pygame.display.set_mode((resolution.x, resolution.y))

sprites = [pygame.image.load(f"{i}.png") for i in range(4)]
sprites_length = len(sprites)

sprite_index = 0

while True:
    screen.fill((0, 0, 0))
    
    screen.blit(sprites[sprite_index % sprites_length], sprite_position)
    
    sprite_index += 1
    
    pygame.display.flip()
    
    clock.tick(1)