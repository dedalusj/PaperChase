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

app.controller("subscriptionsController", ['$scope', 'CategoryServices', 'SubscriptionAPI', function($scope, CategoryServices, SubscriptionAPI){

    $scope.categories = CategoryServices.getCategories();
    $scope.subcategories = [];
    $scope.journals = [];
    
    $scope.selectedCategoryId = undefined;
    $scope.selectedSubcategoryId = undefined;
    $scope.isActive = function(categoryId, isSubcategory) {
        // Return the class for an element of a list (active.clicked state or not) given an index and a kind
        var selectedId = isSubcategory ? $scope.selectedSubcategoryId : $scope.selectedCategoryId;
        return categoryId === selectedId ? 'active' : undefined;
    };
    
    $scope.updateSubcategories = function($event, categoryId) {
        $scope.subcategories = CategoryServices.getSubcategories(categoryId);
        $scope.journals = [];
        $scope.selectedCategoryId = categoryId;
        $scope.selectedSubcategoryId = -1;
    };
    
    $scope.updateJournals = function($event, categoryId) {
        if (categoryId) $scope.selectedSubcategoryId = categoryId;
        if ($scope.selectedSubcategoryId) $scope.journals = CategoryServices.getJournals($scope.selectedSubcategoryId);
    };
    
    $scope.subscribe = function($event, journalId) {
        var newSubscription = new SubscriptionAPI({journal_id: journalId});
        newSubscription.$save();
        CategoryServices.clearJournals();
        $scope.updateJournals();
    };
    
    $scope.unsubscribe = function($event, journalId) {
        SubscriptionAPI.remove({'journal_id': journalId});
        CategoryServices.clearJournals();
        $scope.updateJournals();
    };
}]);

app.controller("suggestionController", ['$scope', 'CategoryServices', function($scope, CategoryServices){
    
    $scope.categories = CategoryServices.getCategories();
    $scope.category = [];
    
    $scope.subcategories = [];
    $scope.subcategory = [];
    
    $scope.updateSubcategories = function() {
        $scope.subcategories = CategoryServices.getSubcategories($scope.category.id);
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

app.controller("registerController", ['$scope', '$http', '$location', 'UserServices', function($scope, $http, $location, UserServices) {
    $scope.registerPC = function() {
        var postData = {email: $scope.email, 
                        password: $scope.password};
        $http({
            url: 'http://localhost:5000/api/register',
            method: "POST",
            data: angular.toJson(postData),
            headers: {'Content-Type': 'application/json'}
        });
    };
}]);