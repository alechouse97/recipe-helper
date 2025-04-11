import pandas as pd
from pathlib import Path
from recipe_helper.price import Prices
from pint import Quantity
from recipe_helper.base import UREG


class Recipe:
    """Class that holds information about a single recipe"""

    def __init__(self, basedir: Path, prices: Prices):
        self.__basedir = basedir
        self.__prices = prices
        self.each_price: dict[str, Quantity] = {}
        self.price = 0.0 * UREG.dollar
        self.__process_ingredients()

    def __process_ingredients(self) -> None:
        """Process the ingredients for the recipe"""

        fname = self.__basedir / "ingredients.csv"
        df = pd.read_csv(fname, keep_default_na=False, index_col="name")
        df = df.T

        for name, vals in df.items():
            qty: Quantity = vals["quantity"] * UREG[vals["unit"]]
            price = self.__prices.compute_price(name, qty)
            self.each_price[name] = price
            self.price += price

        self.__df = df

    def __repr__(self) -> str:
        out = []
        out += [f"Recipe: {self.__basedir.name}"]
        out += ["Ingredients:"]
        for n, p in self.each_price.items():
            s = f"    - {n}: {self.__df[n]['quantity']} {self.__df[n]['unit']}"
            s += f" -> ${p.magnitude:0.2f}"
            out += [s]
        out += [f"Total Price: ${self.price.magnitude:0.2f}"]
        return "\n".join(out)
