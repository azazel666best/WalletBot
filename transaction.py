from re import fullmatch


class Transaction:
    def __init__(self, income_or_expense=True, sum_of_money='', category='', date='', description=''):
        self.income_or_expense = income_or_expense
        self.sum_of_money = sum_of_money
        self.category = category
        self.date = date
        self.description = description

    @property
    def income_or_expense(self):
        return self.__income_or_expense

    @property
    def sum_of_money(self):
        return self.__sum_of_money

    @property
    def category(self):
        return self.__category

    @property
    def date(self):
        return self.__date

    @property
    def description(self):
        return self.__description

    @income_or_expense.setter
    def income_or_expense(self, income_or_expense):
        if not isinstance(income_or_expense, bool):
            raise TypeError()
        self.__income_or_expense = income_or_expense

    @sum_of_money.setter
    def sum_of_money(self, sum_of_money):
        if not fullmatch(r'[\d]+([.,][\d]{2})*', sum_of_money):
            raise TypeError
        self.__sum_of_money = sum_of_money

    @category.setter
    def category(self, category):
        if not isinstance(category, str):
            raise TypeError
        self.__category = category

    @date.setter
    def date(self, date):
        if not isinstance(date, str):
            raise TypeError
        lst = list(map(int, date.split('.')))
        if 1 > lst[1] or lst[1] > 12:
            raise ValueError('moth')
        if lst[0] < 1:
            raise ValueError('day<0')
        if lst[1] in [1, 3, 5, 7, 8, 10, 12] and lst[0] > 31:
            raise ValueError('day>31')
        if lst[1] in [4, 6, 9, 11] and lst[0] > 30:
            raise ValueError("day>30")
        if lst[1] == 2:
            if lst[0] > 29:
                raise ValueError('>29')
            elif not (lst[2] % 400 == 0 or (lst[2] % 4 == 0 and lst[2] % 100 == 0)) and lst[0] > 28:
                raise ValueError('>28')
        self.__date = date

    @description.setter
    def description(self, description):
        if not isinstance(description, str):
            raise TypeError
        self.__description = description

    def __str__(self):
        return f'{"-" if not self.income_or_expense else ""}{self.sum_of_money}, {self.category}, {self.date}, ' \
               f'{self.description}'
