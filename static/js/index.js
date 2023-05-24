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
        test: "TEXT",
    }; 

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.getPantry = function() {
        axios.get(getPantry_url).then(function (r) {
            app.vue.pantry = r.data.pantry;
            // console.log(app.vue.pantry)
        });
    }

    app.addItemToPantry = function() {
        // adds item from ingredientInput box to database with userID
        item = this.ingredientInput.toLowerCase();
        item = item.charAt(0).toUpperCase() + item.slice(1);
        fetch(addItemToPantry_url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                item: item,
            }),
        }).then((response) => response.json()).then((data) => {
            console.log("Item added!");
            this.ingredientInput = "";
            app.getPantry();    // could also just append item to pantry for more efficiency but less consistency 
        });
    }

    app.deleteItem = function(itemID) {
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
        });
    }

    app.clearIngredientInput = function() {
        // Clear the search query
        this.ingredientInput = "";
        console.log("Ingredient Input Box Cleared!");
    }

    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.

        addItemToPantry: app.addItemToPantry,
        clearIngredientInput: app.clearIngredientInput,
        deleteItem: app.deleteItem,
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
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
console.log("Initting vue app! JavaScript is fo sho being loaded");
init(app);
