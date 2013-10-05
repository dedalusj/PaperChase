app.factory('CategoryServices', ['CategoryAPI', function(CategoryAPI) {
    // defines a categories service that can load the list from the backend and can cache it 
    var categoriesData;
    var categories = function(callback) {
        categoriesData = CategoryAPI.query(callback);
        return categoriesData;
    }

    var subcategoriesData;
    var mainCategoryId;
    var subcategories = function(parentId, callback) {
        mainCategoryId = parentId;
        subcategoriesData = CategoryAPI.query({categoryId: parentId, resource: 'subcategories'},callback);
        return subcategoriesData;
    }
    
    var journalsData;
    var categoryId;
    var journals = function(catId, callback) {
        categoryId = catId;
        journalsData = CategoryAPI.query({categoryId: catId, resource: 'journals'},callback);
        return journalsData;
    }

    return {
        getCategories: function(callback) {
            if(categoriesData) {
                return categoriesData;
            } else {
                return categories(callback); 
            }
        },
        getSubcategories: function(parentId, callback) {
            if (subcategoriesData && parentId === mainCategoryId) {
                return subcategoriesData;
            } else {
                return subcategories(parentId, callback); 
            }
        },
        getJournals: function(catId, callback) {
            if (journalsData && catId === categoryId) {
                return journalsData;
            } else {
                return journals(catId, callback); 
            }
        },
        clearCategories: function() {
            categoriesData = undefined; 
        },
        clearSubcategories: function() {
            subcategoriesData = undefined;
        },
        clearJournals: function() {
            journalsData = undefined;
        }
    };
}]);