from pathlib import Path
from recipes.price import Prices
from recipes.recipe import Recipe


hdir = Path("/home/alec/projects/recipes")

ingredient_prices = Prices(hdir / "prices.csv")
frosting = Recipe(hdir / "recipes" / "vanilla-buttercream-frosting", ingredient_prices)
cake = Recipe(hdir / "recipes" / "chocolate-cake", ingredient_prices)

print(cake)
print(frosting)
