# Recipe Organizer

Recipe Organizer is a Python project I built using Firebase Firestore to store and manage recipes in a cloud database.

I wanted the application to do more than just store recipes. It allows me to add, view, update, and delete recipes, as well as manage the ingredients within each recipe.

## What It Can Do

- Add a new recipe
- View saved recipes
- Update a recipe name
- Add an ingredient to an existing recipe
- Edit an existing ingredient
- Delete an ingredient
- Delete a recipe

## Built With

- Python
- Firebase Firestore
- Firebase Admin SDK

## How the Database Is Organized

The project uses two Firestore collections:

### categories

This collection stores recipe categories.

Each category has:

- Name
- Description

### recipes

This collection stores the actual recipes.

Each recipe has:

- Name
- Ingredients
- Instructions
- Category ID

The `category_id` connects a recipe to its category in the `categories` collection.

## Running the Project

After cloning the project, install the required packages:

    pip install -r requirements.txt

Then run the application with:

    py src\main.py

The project requires a Firebase service account key to connect the application to Firestore.

## Security

The Firebase service account key contains private credentials, so it is excluded from the repository using `.gitignore`.

## What I Learned

This project helped me practice working with a cloud database from Python. I worked with Firestore collections and documents and learned how to create, retrieve, update, and delete data.

I also learned how to work with lists and dictionaries inside Firestore documents while building the ingredient management features.