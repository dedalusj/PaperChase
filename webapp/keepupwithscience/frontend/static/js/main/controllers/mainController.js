app.controller("mainController", function($scope, $http, $resource){
 
    $http.defaults.headers.common['Authorization'] = 'Basic ' + Base64.encode('dedalusj@gmail.com:idathik');
    
    $scope.categories = [];
    var Category = $resource('http://localhost:port/api/categories/:categoryId', {categoryId:'@id', port: ':5000'});
    
    $scope.init = function() {
        $scope.categories = Category.query();
    };
});