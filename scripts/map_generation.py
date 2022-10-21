from classes.level import *
from pytmx.util_pygame import load_pygame


def gen_level() -> Level:
    path = Path('scripts/cart_map2.tmx')

    level_map = load_pygame(path)

    cart = level_map.get_layer_by_name('RacingCart')
    inner: list[tuple] = []
    outer: list[tuple] = []
    for obj in cart:
        if obj.name == 'inner':
            inner = [(point.x * XSCALE, point.y * YSCALE) for point in obj.points]
        elif obj.name == 'outer':
            outer = [(point.x * XSCALE, point.y * YSCALE) for point in obj.points]

    level = Level(inner, outer)
    return level
