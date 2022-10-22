from classes.level import *
from pytmx.util_pygame import load_pygame


def gen_level(genomes, config) -> Level:
    path = Path('scripts/cart_map2.tmx')

    level_map = load_pygame(path)

    cart = level_map.get_layer_by_name('RacingCart')
    inner: list[tuple] = []
    outer: list[tuple] = []
    money: list[Money] = []
    finish_line: Finish = None

    for obj in cart:
        if obj.name == 'inner':
            inner = [(point.x * XSCALE, point.y * YSCALE) for point in obj.points]
        elif obj.name == 'outer':
            outer = [(point.x * XSCALE, point.y * YSCALE) for point in obj.points]
        elif obj.name == 'finish_line':
            finish_line = Finish(obj.x * XSCALE, obj.y * YSCALE,
                                 obj.height * YSCALE, obj.width * YSCALE)
        elif obj.name == 'money':
            money.append(Money(obj.x * XSCALE, obj.y * YSCALE))
        elif obj.name == 'bad_money':
            money.append(BadMoney(obj.x * XSCALE, obj.y * YSCALE))


    level = Level(inner, outer, money, finish_line, genomes, config)
    return level
