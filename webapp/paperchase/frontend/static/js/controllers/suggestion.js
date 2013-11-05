app.controller("suggestionController", ['$scope', 'CategoryAPI', '$http', function($scope, CategoryAPI, $http){
    
    $scope.alert = undefined;
    $scope.closeAlert = function() {
        $scope.alert = undefined;
    };
    
    $scope.categories = CategoryAPI.getCategories();
    $scope.category = [];
    
    $scope.subcategories = [];
    $scope.subcategory = [];
    
    $scope.updateSubcategories = function() {
        $scope.subcategories = CategoryAPI.getSubcategories({'category_id' : $scope.category.id});
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
                url: '/api/suggestion',
                method: "POST",
                data: angular.toJson(postData),
                headers: {'Content-Type': 'application/json'}
            }).success(function() {
                $scope.alert = { type: 'success', msg: 'Your journal suggestion has been submitted!' };
            })
        }
    };
}]);
