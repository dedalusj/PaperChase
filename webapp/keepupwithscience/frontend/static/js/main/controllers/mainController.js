app.controller("mainController", function($scope, $http, $resource){
 
    $http.defaults.headers.common['Authorization'] = 'Basic ' + Base64.encode('dedalusj@gmail.com:idathik');
    
    $scope.categories = [];
    $scope.subcategories = [];
    $scope.journals = [];
    var Category = $resource('http://localhost\\:5000/api/categories/:categoryId/:resource', {categoryId:'@id', resource: '@res'});
    
    $scope.updateSubcategories = function($event, categoryId) {
        $scope.subcategories = Category.query({categoryId: categoryId, resource: 'subcategories'})
    }
    
    $scope.updateJournals = function($event, categoryId) {
        $scope.journals = Category.query({categoryId: categoryId, resource: 'journals'})
    }
    
    $scope.init = function() {
        $scope.categories = Category.query();
    };
});