app.controller("mainController", ['$scope', '$location', 'UserServices', function($scope, $location, UserServices) {
    $scope.isLogged = function() {
        return UserServices.isLogged();
    };
    $scope.logoutPC = function() {
        UserServices.clearCredentials();
        $location.path( "/login" );
    };
    $scope.isActive = function(route) {
        return route === $location.path();
    };
}]);

app.controller("homeController", ['$scope', function($scope) {

}]);

app.controller("subscriptionsController", ['$scope', 'CategoryAPI', 'CategoryServices', 'SubcategoryServices', function($scope, CategoryAPI, CategoryServices, SubcategoryServices){

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
}]);

app.controller("suggestionController", ['$scope', 'CategoryAPI', 'CategoryServices', 'SubcategoryServices', function($scope, CategoryAPI, CategoryServices, SubcategoryServices){
    
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
            });
        }
    };
}]);

app.controller("loginController", ['$scope', '$http', '$location', 'UserServices', function($scope, $http, $location, UserServices) {
    $scope.loginPC = function() {
        UserServices.verifyCredentials($scope.email,$scope.password).then(function() { 
            UserServices.setCredentials($scope.email,$scope.password);
            $location.path( "/home" ); 
        });
    };
}]);