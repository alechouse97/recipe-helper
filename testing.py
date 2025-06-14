from recipe_helper.prices import Prices
from recipe_helper.ingredient import Ingredient

prices = Prices("prices.csv")
sugar1 = Ingredient("sugar", prices, 4, "lb")
sugar2 = Ingredient("sugar", prices, 1814.37, "g")
print(sugar1)
print(sugar2)
print(sugar1 + sugar2)