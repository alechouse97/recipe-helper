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
        self.ingredient_price: dict[str, Quantity] = {}
        self.serving_price: dict[str, Quantity] = {}
        self.price = 0.0 * UREG.dollar
        self.__process_ingredients()
        self.__process_servings()

    def __process_ingredients(self) -> None:
        """Process the ingredients for the recipe"""

        fname = self.__basedir / "ingredients.csv"
        df = pd.read_csv(fname, keep_default_na=False, index_col="name")

        for name, vals in df.iterrows():
            qty: Quantity = vals["quantity"] * UREG[vals["unit"]]
            price = self.__prices.compute_price(name, qty)
            self.ingredient_price[name] = price
            self.price += price

        self._ingredients = df

    def __process_servings(self) -> None:
        """Process the servings for the recipe"""
        fname = self.__basedir / "servings.csv"
        df = pd.read_csv(fname, keep_default_na=False, index_col="form")

        # Check that no servings are zero
        if df["servings"].eq(0).any():
            raise ValueError(f"Error when reading {fname}, number of servings cannot be zero.")

        # Calculate the price per serving
        for form, row in df.iterrows():
            servings = row["servings"]
            self.serving_price[form] = self.price.magnitude / servings

        self._servings = df

    # def __repr__(self) -> str:
    #     out = []
    #     out += [f"Recipe: {self.__basedir.name}"]
    #     out += ["Ingredients:"]
    #     for n, p in self.ingredient_price.items():
    #         s = f"    - {n}: {self._ingredients.at[n, 'quantity']} {self._ingredients.at[n, 'unit']}"
    #         s += f" -> ${p.magnitude:0.2f}"
    #         out += [s]
    #     out += [f"Total Price: ${self.price.magnitude:0.2f}"]
    #     return "\n".join(out)
