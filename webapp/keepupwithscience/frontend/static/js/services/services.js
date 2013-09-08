app.factory('CategoryAPI', function($http, $resource){
    // Define the resource for the category API to be shared by all other services and controllers
    
    // TODO: this http header line for authentication should be probably moved to its own service
    $http.defaults.headers.common['Authorization'] = 'Basic ' + Base64.encode('dedalusj@gmail.com:idathik');
	
	return $resource('http://localhost\\:5000/api/categories/:categoryId/:resource', {categoryId:'@id', resource: '@res'});
});

app.factory('CategoryServices', function(CategoryAPI) {
    // defines a categories service that can load the list from the backend and can cache it 
    var data;
    var categories = function(callback) {
        data = CategoryAPI.query(callback);
        return data;
    }
    return {
        getCategories: function(callback) {
            if(data) {
                return data;
            } else {
                return categories(callback); 
            }
        }
    };
});

app.factory('SubcategoryServices', function(CategoryAPI) {
    // defines a subcategories service that can load the list from the backend or returned cached data if the id of the category is unchanged 
    var data;
    var categoryId;
    var subcategories = function(parentId, callback) {
        categoryId = parentId;
        data = CategoryAPI.query({categoryId: parentId, resource: 'subcategories'},callback);
        return data;
    }
    return {
        getSubcategories: function(parentId, callback) {
            if (data && parentId === categoryId) {
                return data;
            } else {
                return subcategories(parentId, callback); 
            }
        }
    };
});