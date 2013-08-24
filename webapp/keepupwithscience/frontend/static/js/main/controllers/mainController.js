app.controller("mainController", function($scope, $http){
 
    $http.defaults.headers.common['Authorization'] = 'Basic ' + Base64.encode('dedalusj@gmail.com:idathik');
    $scope.categories = [];
    $scope.init = function() {
        var q = {order_by: [{field: "name", direction: "asc"}]};
        $http.jsonp('http://localhost:5000/api/categories?q=' + angular.toJson(q) + '&callback=JSON_CALLBACK').success(function(data, status, headers, config) {
//            console.log(headers);
//            console.log(status);
//            console.log(data);
//            console.log(config);
        
            //As we are getting our data from an external source, we need to format the data so we can use it to our desired affect
            //For each day get all the episodes
            angular.forEach(data.objects, function(category, index){
                $scope.categories.push(category);
            });
        }).error(function(data, status, headers, config) {
            console.log(headers);
            console.log(status);
            console.log(data);
            console.log(config);
        });
    };
});