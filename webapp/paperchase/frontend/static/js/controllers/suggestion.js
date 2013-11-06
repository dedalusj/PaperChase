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
    
    $scope.submitted = function() {
        $scope.alert = { type: 'success', msg: 'The developers will review the information in your email, add the journal and contact you. You can now return to the <a href="#/home">home page</a>' };
    };
}]);
