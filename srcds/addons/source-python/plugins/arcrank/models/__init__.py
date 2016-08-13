from path import Path


def parse_models(dir_):
    models = []
    for path in Path(dir_).files():
        if path.ext != '.py':
            continue

        if path.name.startswith('__') and path.namebase.endswith('__'):
            continue

        models.append(path.namebase)

    return models


__all__ = parse_models(Path(__file__).parent)

from . import *
