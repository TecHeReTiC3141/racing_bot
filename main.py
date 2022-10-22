import neat

from scripts.map_generation import *

display = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT))
pygame.display.set_caption('Racing Game')

clock = pygame.time.Clock()
CUR_GEN = 0

def setup_neat():

    config_path = 'neat-config.txt'
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    pop.add_reporter(neat.StatisticsReporter())

    winner = pop.run(main, MAX_GENS)
    return winner


def main(genomes: list[tuple], config):
    global CUR_GEN
    level = gen_level(genomes, config)

    while True:
        display.fill('white')
        level.draw(display)
        gen_alive = level.game_cycle()

        if not gen_alive:
            break

        display.blit(font.render(f'FPS: {round(clock.get_fps())}',
                                 True, 'red'), (10, 50))
        display.blit(font.render(f'CUR_GEN: {CUR_GEN}',
                                 True, 'red'), (10, 10))
        pygame.display.update()
        clock.tick(60)
    CUR_GEN += 1


if __name__ == '__main__':
    setup_neat()