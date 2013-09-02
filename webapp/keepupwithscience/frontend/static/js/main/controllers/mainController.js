app.controller("mainController", function($scope, $http, $resource){
 
    $http.defaults.headers.common['Authorization'] = 'Basic ' + Base64.encode('dedalusj@gmail.com:idathik');
    
    $scope.categories = [];
    $scope.subcategories = [];
    $scope.journals = [];
    var Category = $resource('http://localhost\\:5000/api/categories/:categoryId/:resource', {categoryId:'@id', resource: '@res'});
    
    $scope.selectedCategoryIndex = -1;
    $scope.categoryClass = function(categoryId) {
        return categoryId === $scope.selectedCategoryIndex ? 'active' : undefined;
    };
    $scope.updateSubcategories = function($event, categoryId) {
        $scope.subcategories = Category.query({categoryId: categoryId, resource: 'subcategories'});
        $scope.journals = [];
        $scope.selectedCategoryIndex = categoryId;
        $scope.selectedSubcategoryIndex = -1;
    };
    
    $scope.selectedSubcategoryIndex = -1;
    $scope.subcategoryClass = function(categoryId) {
        return categoryId === $scope.selectedSubcategoryIndex ? 'active' : undefined;
    };
    $scope.updateJournals = function($event, categoryId) {
        $scope.journals = Category.query({categoryId: categoryId, resource: 'journals'});
        $scope.selectedSubcategoryIndex = categoryId;
    };
    
    $scope.init = function() {
        $scope.categories = Category.query();
    };
});