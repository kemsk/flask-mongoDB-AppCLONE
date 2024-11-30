from flask import Flask, jsonify, render_template
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection string and database setup
client = MongoClient('mongodb+srv://20220024573:T7CmWQ47ed9s8kpv@recipecluster.81ir5.mongodb.net/')
db = client['RecAPI']  # Database name

# Define the collections
recipes_collection = db['Recipes']
ingredients_collection = db['Ingredients']
authors_collection = db['Authors']
dietary_benefits_collection = db['Dietarybenefits']
nutrition_info_collection = db['Nutritioninfo']
pictures_collection = db['Pictures']
users_collection = db['Users']
videos_collection = db['Videos']

@app.route('/')
def home():
    return render_template('index.html')  # Renders the HTML front end

# API endpoint to get all data from Recipes collection
@app.route('/api/recipes', methods=['GET'])
def get_all_recipes():
    try:
        # Fetch all recipes from the Recipes collection
        recipes = recipes_collection.find({})
        response = []

        # Loop through each recipe to fetch its ingredients
        for recipe in recipes:
            recipe_ingredients = []
            # Fetch the ingredients that match the current recipeID from the Ingredients collection
            ingredients = ingredients_collection.find({'recipeID': recipe['recipeID']})
            for ingredient in ingredients:
                recipe_ingredients.append({
                    'name': ingredient.get('name', 'N/A'),
                    'quantity': ingredient.get('quantity', 'N/A')
                })

            # Add the recipe along with its ingredients
            response.append({
                'recipeID': str(recipe['recipeID']),
                'name': recipe.get('name', 'N/A'),
                'instructions': recipe.get('instructions', 'N/A'),
                'category': recipe.get('type', 'N/A'),
                'ingredients': recipe_ingredients
            })

        # Return the recipes and ingredients in JSON format
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return an error response if something goes wrong

if __name__ == '__main__':
    app.run(debug=True)
