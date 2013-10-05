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