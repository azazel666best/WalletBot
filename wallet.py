class Wallet:
    def __init__(self, name='', description=''):
        self.name = name
        self.description = description

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError
        self.__name = name

    @description.setter
    def description(self, description):
        if not isinstance(description, str):
            raise TypeError
        self.__description = description

    def __str__(self):
        return f'{self.name}, {self.description}'
