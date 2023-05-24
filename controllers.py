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
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email

import openai
from dotenv import dotenv_values
secrets = dotenv_values(".env")

url_signer = URLSigner(session)


@action('index')
@action.uses('index.html', db, auth.user, url_signer)
def index():
    return dict(
        # COMPLETE: return here any signed URLs you need.
        getPantry_url=URL('getPantry', signer=url_signer),
        addItemToPantry_url=URL('addItemToPantry', signer=url_signer),
        deleteItem_url=URL('deleteItem', signer=url_signer),
    )


@action('getPantry', method="GET")
@action.uses(db, auth.user, url_signer)
def getPantry():
    userID = auth.current_user.get("id")
    pantry = db(db.pantry.userID == userID).select().as_list()
    return dict(pantry=pantry)


@action('addItemToPantry', method="POST")
@action.uses(db, auth.user, url_signer)
def addItemToPantry():
    userID = auth.current_user.get("id")
    item = request.json.get("item")
    if db(db.pantry.item == item).select().first():
        return dict(success=False)
    db.pantry.insert(
        userID=userID,
        item=item,
    )
    newItem = db(db.pantry.item == item).select().first()
    return dict(success=True, newItem=newItem)

# probably need to add security to this


@action('deleteItem', method="POST")
@action.uses(db, auth.user, url_signer)
def deleteItem():
    itemID = request.json.get("itemID")
    db(db.pantry.id == itemID).delete()
    return dict()


@action('testCompletion', method="GET")
@action.uses()
def testCompletion():
    print("Calling a test completion!")
    openai.api_key = secrets["OPENAI_KEY"]
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Say the test has been completed sucessfully in shakespearean",
        max_tokens=15,
        temperature=0.3,
    )
    print(response)
    print(response.choices[0].text)
