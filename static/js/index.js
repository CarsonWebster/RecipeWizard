// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        // Complete as you see fit.
        ingredientInput: "",    // Holds the data from the pantry input
        pantry: [],             // Holds all items in logged in users pantry
        recipes: [],
        // generated_recipes: [],
        numPantryRows: 5,       // Number of rows to display in the pantry
        pantryExpanded: false,
        displayTrash: -1,       // Which trashcan to display
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => { e._idx = k++; });
        return a;
    };

    app.updatePantryRows = function () {
        app.vue.numPantryRows = Math.max(5, Math.ceil(app.vue.pantry.length / 2));
    }

    app.getPantry = function () {
        axios.get(getPantry_url).then(function (r) {
            app.vue.pantry = r.data.pantry;
            app.updatePantryRows();
            // console.log(app.vue.pantry)
        });
    }

    app.addItemToPantry = function () {
        // adds item from ingredientInput box to database with userID
        if (this.pantry.length > 100) {  // add alert/pop up to tell user here
            alert("You have too many items in your pantry. Please remove some before adding more");
            console.log("You have too many items in your pantry. Please remove some before adding more");
            return;
        }
        item = this.ingredientInput;
        if (item.length == 0) {
            return;
        }
        item = item.charAt(0).toUpperCase() + item.slice(1).toLowerCase();
        fetch(addItemToPantry_url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                item: item,
            }),
        }).then((response) => response.json()).then((data) => {
            if (data.success == true) {
                console.log("Item added!");
                this.ingredientInput = "";
                // app.getPantry();
                app.vue.pantry.push(data.newItem);
                app.updatePantryRows();
            } else {
                console.log("Item already in pantry");
                alert("Item already in pantry");
            }
        });
    }

    app.deleteItem = function (itemID) {
        // removes item from pantry and db
        fetch(deleteItem_url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                itemID: itemID,
            }),
        }).then((response) => response.json()).then((data) => {
            console.log("Item deleted");
            app.getPantry();    // could also just remove item from pantry for more efficiency but less consistency
            app.updatePantryRows();
        });
    }

    app.clearIngredientInput = function () {
        // Clear the search query
        this.ingredientInput = "";
    }

    app.togglePantryExpanded = function () {
        if (app.vue.numPantryRows > 5) {
            app.vue.pantryExpanded = !app.vue.pantryExpanded;
        }
    }

    app.setDisplayTrash = function (n) {
        app.vue.displayTrash = n;
    }

    // app.generateRecipeSuggestion = function () {
    //     console.log("Generated Recipe Suggestion")
    //     axios.get(generateRecipeSuggestion_url).then((response) => {
    //       console.log(response.data)
    //       // Access the recipe from the response data
    //       const recipe = response.data;
    //       // Update the recipes array with the new recipe
    //       app.vue.generated_recipes.push(recipe);
    //     });
    //   }

    app.addRecipe = function () {
        let new_recipe = {}
        new_recipe._idx = app.vue.recipes.length;
        // Push the recipe content to the row
        new_recipe.title = "New Recipe";
        new_recipe.ingredients = [];
        new_recipe.instructions = [];
        new_recipe.show = true;
        new_recipe.loading = false;
        app.vue.recipes.push(new_recipe);
        app.genRecipe(new_recipe._idx);
    }

    app.getRecipes = function () {
        axios.get(getRecipes_url).then((r) => {
            let recipeIndex = 0;
            app.vue.recipes = r.data.recipes.map((recipeObj) => {
                const addedRecipe = {
                    _idx: recipeIndex,
                    dbID: recipeObj.id,
                    content: recipeObj.recipe,
                    show: false,
                    loading: false,
                };
                recipeIndex++;
                return addedRecipe;
            });
        });

    }

    app.genRecipe = function (idx) {
        console.log("genning recipe:")
        // Toggle recipe loading
        app.vue.recipes[idx].loading = true;
        app.vue.recipes[idx].title = "Loading...";
        axios.get(generateRecipeSuggestion_url).then((response) => {
            console.log(response.data)
            app.vue.recipes[idx].title = response.data.recipe.title;
            app.vue.recipes[idx].ingredients = response.data.recipe.ingredients;
            app.vue.recipes[idx].instructions = response.data.recipe.instructions;
            app.vue.recipes[idx].loading = false;
        })
    }

    app.deleteRecipe = function (idx) {
        console.log("Deleting db recipe:", app.vue.recipes[idx])
        fetch(deleteRecipe_url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                recipeID: app.vue.recipes[idx].dbID,
            }),
        }).then((response) => {
            console.log("Item deleted");
            // console.log(response);
            // Remove the recipe from the vue list. Does not refresh the index of recipes in vue list
            // app.vue.recipes.splice(idx, 1);
            // OR, refresh the list. This is more expensive, but more consistent
            app.getRecipes();
        });
    }

    app.toggleRecipe = function (row_idx) {
        app.vue.recipes[row_idx].show = !app.vue.recipes[row_idx].show
    }

    app.testCompletion = function () {
        console.log("Testing completion")
        axios.get(testCompletion_url).then((data) => {
            console.log(data)
        })
    }

    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        addItemToPantry: app.addItemToPantry,
        clearIngredientInput: app.clearIngredientInput,
        deleteItem: app.deleteItem,
        togglePantryExpanded: app.togglePantryExpanded,
        setDisplayTrash: app.setDisplayTrash,

        // generateRecipeSuggestion: app.generateRecipeSuggestion,
        getRecipes: app.getRecipes,
        addRecipe: app.addRecipe,
        genRecipe: app.genRecipe,
        toggleRecipe: app.toggleRecipe,
        deleteRecipe: app.deleteRecipe,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    app.init = () => {
        // Put here any initialization code.
        // Typically this is a server GET call to load the data.
        app.getPantry();
        app.updatePantryRows();
        app.getRecipes();
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
// console.log("Initting vue app! JavaScript is fo sho being loaded");
init(app);
