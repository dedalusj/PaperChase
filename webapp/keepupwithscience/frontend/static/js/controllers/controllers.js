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

app.controller("mainController", function($scope){

});

app.controller("categoryController", function($scope, CategoryAPI, CategoryServices, SubcategoryServices){

    $scope.categories = CategoryServices.getCategories();
    $scope.subcategories = [];
    $scope.journals = [];
    
    $scope.selectedCategoryId = -1;
    $scope.selectedSubcategoryId = -1;
    $scope.isActive = function(categoryId, isSubcategory) {
        // Return the class for an element of a list (active.clicked state or not) given an index and a kind
        var selectedId = isSubcategory ? $scope.selectedSubcategoryId : $scope.selectedCategoryId;
        return categoryId === selectedId ? 'active' : undefined;
    };
    
    $scope.updateSubcategories = function($event, categoryId) {
        $scope.subcategories = SubcategoryServices.getSubcategories(categoryId);
        $scope.journals = [];
        $scope.selectedCategoryId = categoryId;
        $scope.selectedSubcategoryId = -1;
    };
    
    $scope.updateJournals = function($event, categoryId) {
        $scope.journals = CategoryAPI.query({categoryId: categoryId, resource: 'journals'});
        $scope.selectedSubcategoryId = categoryId;
    };
});

app.controller("suggestionController", function($scope, CategoryAPI, CategoryServices, SubcategoryServices){
    
    $scope.categories = CategoryServices.getCategories();
    $scope.category = [];
    
    $scope.subcategories = [];
    $scope.subcategory = [];
    
    $scope.updateSubcategories = function() {
        $scope.subcategories = SubcategoryServices.getSubcategories($scope.category.id);
    };
    
    $scope.formatAndSubmit = function(suggestion) {
        if (suggestion.$valid) {
            var postData = {name: $scope.name, 
                            url: $scope.url,
                            category: $scope.category.name,
                            subcategory: $scope.subcategory.name,
                            title: $scope.title,
                            authors: $scope.authors,
                            abstract: $scope.abstract};
            $http({
                url: 'http://localhost:5000/api/suggestion',
                method: "POST",
                data: angular.toJson(postData),
                headers: {'Content-Type': 'application/json'}
            }).success(function (data, status, headers, config) {
//            do something with success
            }).error(function (data, status, headers, config) {
//            do we need this?
            });
        }
    };
});