import inspect
import pkgutil
from typing import Type

from modules.base_module import Base


def load_modules(path: str):
    objects = []
    for module_finder, name, ispkg in pkgutil.iter_modules(path=[path]):
        if ispkg or name == __name__:
            continue
        mod = module_finder.find_module(name).load_module(name)
        cls = next((cls for class_name, cls in inspect.getmembers(mod, inspect.isclass) if class_name != "Base"), None)
        if cls is None:
            continue
        else:
            objects.append(cls)
    return objects


def main():
    objects: list[Type[Base]] = load_modules('modules')

    input_string = 'TesT StRing'
    print('input string:', input_string, '\n')
    for obj in objects:
        m = obj()
        print(f'res by {m.__module__}:', m.handle_string(input_string))


if __name__ == '__main__':
    main()
