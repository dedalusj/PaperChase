app.controller("loginController", ['$scope', '$http', '$location', 'UserServices', function($scope, $http, $location, UserServices) {
    $scope.loginPC = function() {
        UserServices.verifyCredentials($scope.email,$scope.password).then(function() { 
            UserServices.setCredentials($scope.email,$scope.password);
            $location.path( "/home" ); 
        });
    };
}]);