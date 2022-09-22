from abc import ABC, abstractmethod


class Storage(ABC):
    @property
    @abstractmethod
    def items(self):
        pass

    @property
    @abstractmethod
    def capacity(self):
        pass

    @abstractmethod
    def add(self, name: str, quantity: int):
        """
        Увеличивает запас items
        """
        pass

    @abstractmethod
    def remove(self, name: str, quantity: int):
        """
        Уменьшает запас items
        """
        pass

    @abstractmethod
    def get_free_space(self):
        """
        Возвращает количество свободных мест
        """
        pass

    @abstractmethod
    def get_items(self):
        """
        Возвращает содержание склада в словаре {товар: количество}
        """
        pass

    @abstractmethod
    def get_unique_items_count(self):
        """
        Возвращает количество уникальных товаров
        """
        pass


class Store(Storage):
    def __init__(self):
        self._items = {'фикусы': 14, 'монстеры': 15, 'алоэ': 10, 'фиалки': 12, 'розы': 14, 'пионы': 4}
        self._capacity = 100

    @property
    def items(self):
        return self._items

    @property
    def capacity(self):
        return self._capacity

    def add(self, name: str, quantity: int) -> bool:
        is_ok = False
        if self.get_free_space() >= quantity:
            if name not in self._items.keys():
                self._items.update({name: quantity})
                is_ok = True
            else:
                self._items[name] += quantity
                is_ok = True
        else:
            print('Места недостаточно.')
        return is_ok

    def remove(self, name: str, quantity: int) -> bool:
        is_ok = False
        if name not in self._items.keys():
            print('Такого товара нет.')
        else:
            if self._items[name] - quantity >= 0:
                print('Нужное количество есть на складе.')
                self._items[name] -= quantity
                is_ok = True
            else:
                print('Товара недостаточно.')

        return is_ok

    def get_free_space(self) -> int:
        occupied = sum(v for v in self._items.values())
        free_space = self._capacity - occupied
        return free_space

    def get_items(self) -> dict:
        return self._items

    def get_unique_items_count(self) -> int:
        return len(self._items)


class Shop(Store):
    def __init__(self):
        super().__init__()
        self._items = {'фикусы': 1, 'монстеры': 1}
        self._capacity = 20

    def add(self, name: str, quantity: int) -> bool:
        is_ok = False
        if self.get_free_space() >= quantity:
            if name not in self._items.keys() and self.get_unique_items_count() < 5:
                self._items.update({name: quantity})
                is_ok = True
            elif name not in self._items.keys() and self.get_unique_items_count() == 5:
                print('В магазине уже есть 5 видов товаров. Нельзя добавить новый товар.')
            else:
                self._items[name] += quantity
                is_ok = True
        else:
            print('Места недостаточно.')
        return is_ok


class Request():
    def __init__(self, fromm: str, to: str, amount: int, product: str):
        self.fromm = fromm
        self.to = to
        self.amount = amount
        self.product = product

    def __repr__(self):
        return f'Доставить {self.amount} {self.product} из {self.fromm} в {self.to}.'


def main():
    store = Store()
    shop = Shop()

    while True:
        user_fromm = input('Введите, откуда вы хотите переместить товар: ')
        user_to = input('Введите, куда вы хотите переместить товар: ')
        user_product = input('Введите товар, который хотите переместить: ')
        user_amount = int(input('Введите количество товара: '))

        request = Request(user_fromm, user_to, user_amount, user_product)
        print(request)

        if user_fromm.lower() == 'склад':
            place_1, place_2 = store, shop

        else:
            place_2, place_1 = store, shop

        is_real = place_1.remove(user_product, user_amount)
        if is_real:
            print(f'Курьер забрал {user_amount} {user_product} из {user_fromm}.')
        else:
            continue

        is_real = place_2.add(user_product, user_amount)
        if is_real:
            print(f'Курьер доставил {user_amount} {user_product} в {user_to}.')
        else:
            place_1.add(user_product, user_amount)
            continue

        print(f'В {user_fromm} хранится:')
        for item, quantity in place_1.get_items().items():
            print(f'{quantity} {item}')

        print(f'В {user_to} хранится:')
        for item, quantity in place_2.get_items().items():
            print(f'{quantity} {item}')

if __name__ == '__main__':
    main()