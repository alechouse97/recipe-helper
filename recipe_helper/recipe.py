import pandas as pd
from pathlib import Path
from recipe_helper.prices import Prices
from pint import Quantity
from recipe_helper.base import UREG
from recipe_helper.ingredient import Ingredient

class Recipe:
    """Class that holds information about a single recipe"""

    def __init__(self, basedir: Path, prices: Prices):
        self._basedir = basedir
        self._prices = prices
        self.ingredients: dict[str, Ingredient] = {}
        self.serving_price: dict[str, Quantity] = {}
        self.price: Quantity = 0.0 * UREG["dollar"]
        self._process_ingredients()
        self._process_servings()

    def _process_ingredients(self) -> None:
        """Process the ingredients for the recipe"""

        fname = self._basedir / "ingredients.csv"
        df = pd.read_csv(fname, keep_default_na=False, index_col="name")

        for name, vals in df.iterrows():
            ingredient = Ingredient(name, self._prices, vals["quantity"], vals["unit"])
            self.ingredients[name] = ingredient
            self.price += ingredient.price

        self._ingredients = df

    def _process_servings(self) -> None:
        """Process the servings for the recipe"""
        fname = self._basedir / "servings.csv"
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
        out.append(f"Recipe: {self._basedir.name}")
        out.append("Ingredients:")
        for _, ingred in self.ingredients.items():
            out.append(f"  - {ingred}")
        
        out.append("Servings:")
        for form, price_per_serving in self.serving_price.items():
            size = self._servings.at[form, "size"]
            serves = self._servings.at[form, "serves"]
            qty = self._servings.at[form, "quantity"]
            unit = self._servings.at[form, "unit"]
            out.append(f"  - {form} ({size}, makes {qty}{unit}, serves {serves}): ${price_per_serving:.2f} per serving")
        
        out.append(f"Total Recipe Price: ${self.price.magnitude:.2f}")
        return "\n".join(out) + "\n"
