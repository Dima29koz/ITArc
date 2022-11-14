from base_module import Base


class A(Base):
    def __init__(self):
        print('init A')

    def __del__(self):
        print('destructor A')

    def handle_string(self, raw_string: str):
        return raw_string.capitalize()
