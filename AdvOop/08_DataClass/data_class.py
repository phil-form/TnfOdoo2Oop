from dataclasses import dataclass

@dataclass
class ExampleDataClass:
    name: str
    age: int

    def __str__(self):
        return f"Name: {self.name}, Age: {self.age}"

# équivaut à cette class

class ExampleDataClass2:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def __str__(self):
        return f"Name: {self.name}, Age: {self.age}"

    def __repr__(self):
        return f"ExampleDataClass2(name={self.name}, age={self.age})"

    def __eq__(self, other):
        return self.name == other.name and self.age == other.age

example = ExampleDataClass("James", 40)
print(example)

# Frozen

# Avec Frozen la class devient immuable.
@dataclass(frozen=True)
class LetItGo:
    name: str
    age: int

    def __str__(self):
        return f"Name: {self.name}, Age: {self.age}"

let_it_go = LetItGo("Anna", 30)
print(let_it_go)
# Celà va raise une exception
try:
    let_it_go.test = 1
    print(let_it_go)
except Exception as e:
    print(e)

# Order
# Order va aussi implémenter les méthodes de comparaison (<, <=, >, >=) en se basant sur les champs de la classe.
@dataclass(order=True)
class Example2:
    name: str
    age: int

    def __str__(self):
        return f"Name: {self.name}, Age: {self.age}"