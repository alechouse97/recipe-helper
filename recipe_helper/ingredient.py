from typing import Self
from pint import Quantity
from recipe_helper.base import UREG

from recipe_helper.prices import Prices


class Ingredient:
    def __init__(self, name: str, prices: Prices, quantity: float, unit: str) -> None:
        self.name: str = name
        self.__price_db: Prices = prices
        self.price: Quantity = prices.compute_price(name, quantity * UREG[unit])
        self.quantity: float = quantity
        self.unit: str = unit

    def __repr__(self) -> str:
        return f"Ingredient(name='{self.name}', quantity={self.quantity} {self.unit}, price=${self.price.magnitude:.2f})"

    def __str__(self) -> str:
        return f"{self.quantity:4.2f} {self.unit} {self.name} - ${self.price.magnitude:.2f}"

    def __add__(self, other: Self) -> Self:
        # Check both are the same ingredient
        if self.name != other.name:
            raise ValueError(f"Cannot add ingredients with different names: '{self.name}' and '{other.name}'")
        
        # Sum the quantities and prices
        total_quantity = self.quantity * UREG[self.unit] + other.quantity * UREG[other.unit]
        total_price = self.price + other.price
        
        # Create a new Ingredient with the summed values
        new_ingredient = Ingredient(self.name, self.__price_db, total_quantity.magnitude, self.unit)
        new_ingredient.price = total_price
        return new_ingredient

