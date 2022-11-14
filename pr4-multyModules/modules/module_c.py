from base_module import Base


class C(Base):
    def __init__(self):
        print('init C')

    def __del__(self):
        print('destructor C')

    def handle_string(self, raw_string: str):
        return raw_string.lower()
