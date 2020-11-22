from abc import ABCMeta, abstractmethod


class Animal(metaclass=ABCMeta):

    @property
    @abstractmethod
    def type(self):
        pass

    @property
    @abstractmethod
    def size(self):
        pass

    @property
    @abstractmethod
    def disposition(self):
        pass

    @property
    @abstractmethod
    def is_fierce_animal(self):
        pass


class SomeAnimal(Animal):
    call = ''

    def __init__(self, name, type, size, disposition):
        self._name = name
        self._type = type
        self._size = size
        self._disposition = disposition

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        if self._type == '食肉':
            _type = 1
        else:
            _type = 0
        return _type

    @property
    def size(self):
        if self._size == '小':
            size = 1
        elif self._size == '中等':
            size = 2
        elif self._size == '大':
            size = 3
        else:
            size = 0
        return size

    @property
    def disposition(self):
        if self._disposition == '凶猛':
            disposition = 1
        else:
            disposition = 0
        return disposition

    @property
    def is_fierce_animal(self):
        if self.size >= 2 and self.type == 1 and self.disposition == 1:
            return True
        return False

    @property
    def is_pet(self):
        if self.disposition == 1:
            return False
        return True


class Cat(SomeAnimal):
    call = '喵喵喵'


class Dog(SomeAnimal):
    call = '汪汪汪'


class Zoo(object):

    def __init__(self, name):
        self._name = name

    def __getattr__(self, item):
        try:
            self.__getattribute__(item)
        except AttributeError:
            return None
        return self.__getattribute__(item)

    @property
    def name(self):
        return self._name

    def add_animal(self, animal):
        if not self.__getattr__(animal.__class__.__name__) and isinstance(animal, Animal):
            self.__setattr__(animal.__class__.__name__, animal)


if __name__ == '__main__':
    # 动物园
    z = Zoo('时间动物园')

    # 实例化猫和狗（添加属性）
    cat1 = Cat('大花猫1', '食肉', '小', '温顺')
    dog1 = Dog('大狼狗', '食肉', '大', '凶猛')

    # 将动物添加到动物园类
    z.add_animal(cat1)
    z.add_animal(dog1)

    # 判断
    have_cat = hasattr(z, 'Cat')
    have_dog = hasattr(z, 'Dog')

    print(f'动物园有猫吗? -> {have_cat} {z.Cat.name}')
    print(f'猫：{z.Cat.call}')
    print(f'动物园有狗吗? -> {have_dog} {z.Dog.name}')
    print(f'狗：{z.Dog.call}')

    print(f'{z.Cat.name} 是凶猛动物? {z.Cat.is_fierce_animal}')
    print(f'{z.Cat.name} 是宠物 {z.Cat.is_pet}')
    print(f'{z.Dog.name} 是凶猛动物 {z.Dog.is_fierce_animal}')
    print(f'{z.Dog.name} 是宠物 {z.Dog.is_pet}')