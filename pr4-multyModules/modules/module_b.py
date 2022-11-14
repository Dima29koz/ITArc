from base_module import Base


class B(Base):
    def __init__(self):
        print('init B')

    def __del__(self):
        print('destructor B')

    def handle_string(self, raw_string: str):
        return raw_string.upper()
