import pandas as pd
import redis

df = pd.read_csv("data/cosing.csv")
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

default_exp=3600

# Create lookup dictionary
DATABASE = {
    str(row["INCI name"]).strip().lower(): str(row["Function"]).strip()
    for _, row in df.iterrows()
}


def get_functions(ingredient_string):
    results = []
    function=''
    ingredients = [i.strip() for i in ingredient_string.split(",")]

    for ingredient in ingredients:
        
        function = r.get(ingredient.lower())
        
        if function == None:
            function = DATABASE.get(ingredient.lower(), "Unknown")
            r.setex(ingredient.lower(), default_exp, function)
        
        results.append({
            "ingredient": ingredient,
            "function": function
        })
        
        
    return results