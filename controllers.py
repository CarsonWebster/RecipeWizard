"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import (
    db,
    session,
    T,
    cache,
    auth,
    logger,
    authenticated,
    unauthenticated,
    flash,
)
from datetime import datetime
from py4web.utils.url_signer import URLSigner
from .models import get_user_email

import openai
from dotenv import dotenv_values

secrets = dotenv_values("apps/RecipeWizard/.env")

url_signer = URLSigner(session)


@action("index")
@action.uses("index.html", db, auth.user, url_signer)
def index():
    return dict(
        # COMPLETE: return here any signed URLs you need.
        getPantry_url=URL("getPantry", signer=url_signer),
        addItemToPantry_url=URL("addItemToPantry", signer=url_signer),
        deleteItem_url=URL("deleteItem", signer=url_signer),
        generateRecipeSuggestion_url=URL("generateRecipeSuggestion"),
        getRecipes_url=URL("getRecipes", signer=url_signer),
        deleteRecipe_url=URL("deleteRecipe", signer=url_signer),
        favRecipe_url=URL("favRecipe", signer=url_signer),
        getFavs_url=URL("getFavs", signer=url_signer),
    )


@action("getPantry", method="GET")
@action.uses(db, auth.user, url_signer)
def getPantry():
    userID = auth.current_user.get("id")
    pantry = db(db.pantry.userID == userID).select().as_list()
    return dict(pantry=pantry)


@action("addItemToPantry", method="POST")
@action.uses(db, auth.user, url_signer)
def addItemToPantry():
    userID = auth.current_user.get("id")
    item = request.json.get("item")
    if db((db.pantry.userID == userID) & (db.pantry.item == item)).select().first():
        return dict(success=False)
    db.pantry.insert(
        userID=userID,
        item=item,
    )
    newItem = db((db.pantry.userID == userID) & (
        db.pantry.item == item)).select().first()
    return dict(success=True, newItem=newItem)

# probably need to add security to this
@action("deleteItem", method="POST")
@action.uses(db, auth.user, url_signer)
def deleteItem():
    itemID = request.json.get("itemID")
    db(db.pantry.id == itemID).delete()
    return dict()


defaultPrompt = """
Instructions:
Given a list of ingredients and user preferences, generate a recipe suggestion that meets all the following criteria:
    1.  Utilize the provided ingredients exclusively to reduce food waste and maximize resourcefulness.
    2.  Exclude recipes that contain restricted ingredients based on dietary restrictions. 
        For example, for vegetarian recipes, do not include any animal-based ingredients, including meat like beef, chicken, fish, lamb, etc. Additionally, consider other common dietary restrictions such as vegan, gluten-free, nut allergies, etc. Exclude specific ingredients based on the stated dietary preferences, unless "NONE" is specified.
    3.  Offer a variety of recipe options, including breakfast, lunch, dinner, snacks, and desserts, to cater to different meal preferences.
    4.  Optionally, consider recipes that are quick and easy to prepare, perfect for busy individuals or those with limited cooking time.
    5.  Optionally, provide recipes with a balanced nutritional profile, considering macronutrients and minimizing sugar content.

    Please tap into your culinary expertise and creativity to generate diverse, delicious, and practical recipe suggestions. 
    Assume the provided ingredients are available in sufficient quantities.
    If necessary, you can make reasonable assumptions about ingredient preparation techniques (e.g., chopping, cooking methods).

Examples:
Ingredients: [List the ingredients]
Dietary Preferences: [Specify the dietary preferences and restrictions, e.g., Vegetarian, Vegan, Gluten-free, Nut allergies, NONE]
Number of People: [Specify the number of people the user is cooking for]

Please generate a single recipe based on the provided information.

User input: [Provide the list of ingredients and specify the dietary preferences and restrictions, as well as the number of people cooking for.]

RULE : meat-based options should be included when "NONE" is specified as the dietary preference, the recipe suggestions will be more inclusive and diverse.
"""


@action("generateRecipeSuggestion", method="GET")
@action.uses(db, auth.user)
def generateRecipeSuggestion():
    print("Calling a recipe suggestion generation!")
    # print("Here are the secrets" + str(secrets))
    # openai.api_key = secrets["OPENAI_KEY"]

    userID = auth.current_user.get("id")
    # ingredients = db(db.pantry.userID == userID).select().as_list()
    # dietaryPreferences = ["vegetarian"]  # TODO in future want to pull from URL
    # numberOfPeople = 3  # TODO in future want to pull from URL

    testString = """Basil-Garlic Beef Burgers

Ingredients:
1 pound ground beef
2 cloves garlic, minced
2 tablespoons fresh basil, chopped
1 tablespoon avocado oil
4 burger patties
Salt and pepper to taste"""

    # response = openai.Completion.create(
    #     model="text-davinci-003",
    #     prompt=f"{defaultPrompt} Ingredients : {str(ingredients)}, Dietary Restrictions : {str(dietaryPreferences)}, Number of People : {numberOfPeople}",
    #     max_tokens=200,
    #     temperature=0.3,
    # )
    # print(response)
    userID = auth.current_user.get("id")
    db.recipes.insert(
        created_by=userID,
        # recipe=response.choices[0].text,
        recipe=testString,
    )
    # print(response.choices[0].text)
    # return response.choices[0].text
    return testString


@action("getRecipes", method="GET")
@action.uses(db, auth.user, url_signer)
def getRecipes():
    userID = auth.current_user.get("id")
    recipes = db(db.recipes.created_by == userID).select(
        db.recipes.id, db.recipes.recipe).as_list()
    # print(recipes)
    return dict(recipes=recipes)


@action("deleteRecipe", method="POST")
@action.uses(db, auth.user, url_signer)
def deleteRecipe():
    recipeID = request.json.get("recipeID")
    # print(f"Deleting recipe with ID {recipeID}")
    status = db(db.recipes.id == recipeID).delete()
    # print("status:", status)
    return dict(status = status)

@action("favRecipe", method="POST")
@action.uses(db, auth.user, url_signer)
def favRecipe():
    userID = auth.current_user.get("id")
    # recipeID = request.json.get("recipeID")
    recipe = request.json.get("recipeContent")
    # if db(db.favorites.recipe_id == recipeID).select().first():
    #     print("Failed")
    #     return dict(success=False)
    db.favorites.insert(
        user_id=userID,
        recipe=recipe,
    )
    print("Success")
    return dict(success=True)

@action("getFavs", method="GET")
@action.uses(db, auth.user, url_signer)
def getRecipes():
    userID = auth.current_user.get("id")
    favorites = db(db.favorites.user_id == userID).select(db.favorites.recipe).as_list()
    # print(recipes)
    return dict(favorites=favorites)
