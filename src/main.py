import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path


# Connect to Firebase
key_path = (
    Path(__file__).resolve().parent.parent
    / "cloud-recipe-organizer-firebase-adminsdk-fbsvc-f313fee71c.json"
)

cred = credentials.Certificate(key_path)
firebase_admin.initialize_app(cred)

db = firestore.client()


# Add a category to Firestore
def add_category(category_id, name, description):
    category = {
        "name": name,
        "description": description
    }

    db.collection("categories").document(category_id).set(category)

    print("Category added successfully!")


# Add a recipe to Firestore
def add_recipe(recipe):
    recipe_ref = db.collection("recipes").add(recipe)

    recipe_id = recipe_ref[1].id

    print("Recipe added successfully!")
    print(f"Recipe ID: {recipe_id}")

    return recipe_id


# Retrieve recipes from Firestore
def get_recipes():
    recipes = db.collection("recipes").stream()

    print("\nRecipes in the database:")

    found_recipe = False

    for recipe in recipes:
        found_recipe = True

        print("ID:", recipe.id)
        print("Name:", recipe.to_dict().get("name"))
        print("Ingredients:")

        ingredients = recipe.to_dict().get("ingredients", [])

        for ingredient in ingredients:
            print(
                f"  - {ingredient['name']}: "
                f"{ingredient['quantity']} {ingredient['unit']}"
            )

        print("Instructions:", recipe.to_dict().get("instructions"))
        print("Category ID:", recipe.to_dict().get("category_id"))
        print()

    if not found_recipe:
        print("No recipes found.")


# Update a recipe in Firestore
def update_recipe(recipe_id):
    recipe_ref = db.collection("recipes").document(recipe_id)

    recipe_snapshot = recipe_ref.get()

    if not recipe_snapshot.exists:
        print("Recipe not found.")
        return

    new_name = input("Enter the new recipe name: ")

    recipe_ref.update({
        "name": new_name
    })

    print("Recipe updated successfully!")


# Add an ingredient to an existing recipe
def add_ingredient(recipe_id):
    recipe_ref = db.collection("recipes").document(recipe_id)

    recipe_snapshot = recipe_ref.get()

    if not recipe_snapshot.exists:
        print("Recipe not found.")
        return

    recipe_data = recipe_snapshot.to_dict()

    ingredients = recipe_data.get("ingredients", [])

    ingredient_name = input("Ingredient name: ")
    quantity = input("Quantity: ")
    unit = input("Unit: ")

    new_ingredient = {
        "name": ingredient_name,
        "quantity": quantity,
        "unit": unit
    }

    ingredients.append(new_ingredient)

    recipe_ref.update({
        "ingredients": ingredients
    })

    print("Ingredient added successfully!")


# Edit an ingredient in an existing recipe
def edit_ingredient(recipe_id):
    recipe_ref = db.collection("recipes").document(recipe_id)

    recipe_snapshot = recipe_ref.get()

    if not recipe_snapshot.exists:
        print("Recipe not found.")
        return

    recipe_data = recipe_snapshot.to_dict()
    ingredients = recipe_data.get("ingredients", [])

    if not ingredients:
        print("This recipe has no ingredients.")
        return

    print("\nIngredients:")

    for index, ingredient in enumerate(ingredients, start=1):
        print(
            f"{index}. {ingredient['name']} - "
            f"{ingredient['quantity']} {ingredient['unit']}"
        )

    choice = input("Enter the number of the ingredient to edit: ")

    if not choice.isdigit():
        print("Invalid ingredient number.")
        return

    ingredient_index = int(choice) - 1

    if ingredient_index < 0 or ingredient_index >= len(ingredients):
        print("Invalid ingredient number.")
        return

    print("\nEnter the new ingredient details.")

    new_name = input("Ingredient name: ")
    new_quantity = input("Quantity: ")
    new_unit = input("Unit: ")

    ingredients[ingredient_index] = {
        "name": new_name,
        "quantity": new_quantity,
        "unit": new_unit
    }

    recipe_ref.update({
        "ingredients": ingredients
    })

    print("Ingredient updated successfully!")


# Delete an ingredient from an existing recipe
def delete_ingredient(recipe_id):
    recipe_ref = db.collection("recipes").document(recipe_id)

    recipe_snapshot = recipe_ref.get()

    if not recipe_snapshot.exists:
        print("Recipe not found.")
        return

    recipe_data = recipe_snapshot.to_dict()
    ingredients = recipe_data.get("ingredients", [])

    if not ingredients:
        print("This recipe has no ingredients.")
        return

    print("\nIngredients:")

    for index, ingredient in enumerate(ingredients, start=1):
        print(
            f"{index}. {ingredient['name']} - "
            f"{ingredient['quantity']} {ingredient['unit']}"
        )

    choice = input("Enter the number of the ingredient to delete: ")

    if not choice.isdigit():
        print("Invalid ingredient number.")
        return

    ingredient_index = int(choice) - 1

    if ingredient_index < 0 or ingredient_index >= len(ingredients):
        print("Invalid ingredient number.")
        return

    deleted_ingredient = ingredients.pop(ingredient_index)

    recipe_ref.update({
        "ingredients": ingredients
    })

    print(f"{deleted_ingredient['name']} deleted successfully!")


# Delete a recipe from Firestore
def delete_recipe(recipe_id):
    recipe_ref = db.collection("recipes").document(recipe_id)

    recipe_snapshot = recipe_ref.get()

    if not recipe_snapshot.exists:
        print("Recipe not found.")
        return

    recipe_ref.delete()

    print("Recipe deleted successfully!")


# Run the program
def main():
    # Create the Cake category
    add_category(
        "cake",
        "Cake",
        "Cake and baked dessert recipes"
    )

    while True:
        print("\nRecipe Organizer")
        print("1. Add Recipe")
        print("2. View Recipes")
        print("3. Update Recipe")
        print("4. Add Ingredient")
        print("5. Edit Ingredient")
        print("6. Delete Ingredient")
        print("7. Delete Recipe")
        print("8. Exit")

        choice = input("Choose an option: ")

        # Add a recipe
        if choice == "1":
            recipe_name = input("Recipe name: ")

            ingredients = []

            print("\nEnter ingredients.")
            print("Press Enter without typing an ingredient name when you are finished.")

            while True:
                ingredient_name = input("Ingredient name: ")

                if ingredient_name == "":
                    break

                quantity = input("Quantity: ")
                unit = input("Unit: ")

                ingredients.append({
                    "name": ingredient_name,
                    "quantity": quantity,
                    "unit": unit
                })

            instructions = input("\nInstructions: ")

            recipe = {
                "name": recipe_name,
                "ingredients": ingredients,
                "instructions": instructions,
                "category_id": "cake"
            }

            add_recipe(recipe)

        # View recipes
        elif choice == "2":
            get_recipes()

        # Update a recipe
        elif choice == "3":
            recipe_id = input("Enter the recipe ID to update: ")
            update_recipe(recipe_id)

        # Add an ingredient
        elif choice == "4":
            recipe_id = input("Enter the recipe ID: ")
            add_ingredient(recipe_id)

        # Edit an ingredient
        elif choice == "5":
            recipe_id = input("Enter the recipe ID: ")
            edit_ingredient(recipe_id)

        # Delete an ingredient
        elif choice == "6":
            recipe_id = input("Enter the recipe ID: ")
            delete_ingredient(recipe_id)

        # Delete a recipe
        elif choice == "7":
            recipe_id = input("Enter the recipe ID to delete: ")
            delete_recipe(recipe_id)

        # Exit
        elif choice == "8":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()