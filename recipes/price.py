import pandas as pd
from pathlib import Path
from pint import Quantity, Unit
from base import UREG


class Prices:
    """Class that hold ingredient price per unit"""

    def __init__(self, file: str | Path) -> None:
        self.file = Path(file)
        self.__process()

    def __process(self):
        """Process the prices file"""

        # Read file
        df = pd.read_csv(self.file, keep_default_na=False, index_col="name")
        df["unit_price"] = pd.Series()
        df = df.T

        # Calculate price per unit
        for name, vals in df.items():
            qty = vals["quantity"] * UREG[vals["unit"]]
            unitprice = vals["price"] * UREG.dollar / qty
            df[name]["unit_price"] = unitprice

        # Save
        self.df = df

    def get_price(self, ingredient: str) -> Quantity:
        """Return the price per unit for an ingredient."""
        self.__check_ingredient(ingredient)
        return self.df[ingredient]["unit_price"]

    def get_unit(self, ingredient: str) -> Unit:
        """Return the unit for an ingredient."""
        self.__check_ingredient(ingredient)
        unit_in_file = self.df[ingredient]["unit"]
        if unit_in_file == "":
            return UREG.dimensionless
        n = UREG.get_name(unit_in_file)
        u: Unit = getattr(UREG, n)
        return u

    def compute_price(self, ingredient: str, qty: Quantity) -> Quantity:
        """Compute the price of an ingredient given it's weight"""
        self.__check_ingredient(ingredient)
        new = qty.to(self.get_unit(ingredient))
        price = new * self.get_price(ingredient)
        return price

    def __check_ingredient(self, ingredient):
        if ingredient not in self.df.columns:
            raise KeyError(f"Ingredient '{ingredient}' not present in database.")
