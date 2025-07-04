from pathlib import Path
from recipe_helper.prices import Prices
from recipe_helper.recipe import Recipe


hdir = Path("/home/alec/projects/recipes")

price_db = Prices(hdir / "prices.csv")

red_velvet_cake = Recipe(hdir / "db_recipes" / "red-velvet-cake", price_db)
print(red_velvet_cake)

# chocolate_cake = Recipe(hdir / "db_recipes" / "chocolate-cupcakes", ingredient_prices)
# oreo_cake = Recipe(hdir / "db_recipes" / "oreo-cake", ingredient_prices)
# buttercream = Recipe(hdir / "db_recipes" / "vanilla-buttercream-frosting", ingredient_prices)
# cream_cheese = Recipe(hdir / "db_recipes" / "cream-cheese-frosting", ingredient_prices)
# strawberry_frosting = Recipe(hdir / "db_recipes" / "strawberry-buttercream-frosting", ingredient_prices)

# total_cost = (
#     red_velvet_cake.price
#     + chocolate_cake.price
#     + oreo_cake.price
#     + buttercream.price
#     + cream_cheese.price
#     + strawberry_frosting.price
# )

# print(f"Red Velvet Cake: ${red_velvet_cake.price.magnitude:.2f}")
# print(f"Chocolate Cake: ${chocolate_cake.price.magnitude:.2f}")
# print(f"Oreo Cake: ${oreo_cake.price.magnitude:.2f}")
# print(f"Buttercream Frosting: ${buttercream.price.magnitude:.2f}")
# print(f"Cream Cheese Frosting: ${cream_cheese.price.magnitude:.2f}")
# print(f"Strawberry Buttercream Frosting: ${strawberry_frosting.price.magnitude:.2f}")

# print(f"\nTotal cost of all recipes: ${total_cost.magnitude:.2f}")