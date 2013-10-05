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
