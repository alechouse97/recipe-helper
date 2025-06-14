import pandas as pd
from pathlib import Path
from recipe_helper.prices import Prices
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
        if df["serves"].eq(0).any():
            raise ValueError(f"Error when reading {fname}, 'serves' cannot be zero.")
        if df["quantity"].eq(0).any():
            raise ValueError(f"Error when reading {fname}, 'quantity' cannot be zero.")

        # Calculate the price per serving
        for form, row in df.iterrows():
            servings = row["serves"]
            self.serving_price[form] = self.price.magnitude / servings

        self._servings = df

    def __repr__(self) -> str:
        """Return a nicely formatted string representation of the recipe."""
        out = []
        out.append(f"Recipe: {self.__basedir.name}")
        out.append("Ingredients:")
        for name, price in self.ingredient_price.items():
            quantity = self._ingredients.at[name, "quantity"]
            unit = self._ingredients.at[name, "unit"]
            out.append(f"  - {name}: {quantity} {unit} -> ${price.magnitude:.2f}")
        
        out.append("Servings:")
        for form, price_per_serving in self.serving_price.items():
            size = self._servings.at[form, "size"]
            serves = self._servings.at[form, "serves"]
            qty = self._servings.at[form, "quantity"]
            unit = self._servings.at[form, "unit"]
            out.append(f"  - {form} ({size}, makes {qty}{unit}, serves {serves}): ${price_per_serving:.2f} per serving")
        
        out.append(f"Total Recipe Price: ${self.price.magnitude:.2f}")
        return "\n".join(out) + "\n"
