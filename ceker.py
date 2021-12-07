from re import fullmatch


def money_chek(sum_of_money):
    if not fullmatch(r'[\d]+([.,][\d]{2})*', sum_of_money):
        raise TypeError


def date_check(date):
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
