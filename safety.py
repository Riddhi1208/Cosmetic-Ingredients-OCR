import pandas as pd

# Load CosIng database once when the application starts
df = pd.read_csv("data/cosing.csv")

# Create lookup dictionary
DATABASE = {
    str(row["INCI name"]).strip().lower(): str(row["Function"]).strip()
    for _, row in df.iterrows()
}


def get_functions(ingredient_string):
    results = []

    ingredients = [i.strip() for i in ingredient_string.split(",")]

    for ingredient in ingredients:
        function = DATABASE.get(ingredient.lower(), "Unknown")

        results.append({
            "ingredient": ingredient,
            "function": function
        })

    return results