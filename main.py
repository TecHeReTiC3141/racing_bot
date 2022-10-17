from scripts.map_generation import *

display = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT), 0, 42)
pygame.display.set_caption('Racing Game')

clock = pygame.time.Clock()
level = gen_level()

while True:
    display.fill('white')
    level.draw(display)
    level.game_cycle()

    display.blit(font.render(f'FPS: {round(clock.get_fps())}',
                             True, 'red'), (10, 50))
    pygame.display.update()
    clock.tick(60)
