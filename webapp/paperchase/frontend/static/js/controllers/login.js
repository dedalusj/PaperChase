app.controller("loginController", ['$scope', '$http', '$location', 'UserServices', function($scope, $http, $location, UserServices) {
    $scope.alert = undefined;
    
    $scope.closeAlert = function() {
        $scope.alert = undefined;
    };
    
    $scope.loginPC = function() {
        UserServices.verifyCredentials($scope.email,$scope.password).
        success(function() {
            UserServices.setCredentials($scope.email,$scope.password);
            if (UserServices.hasLoggedInBefore()) {
                $location.path( "/home" );
            } else {
                $location.path( "/subscriptions" );
            }
        }).
        error(function(data, status, headers, config) {
            $scope.alert = { type: 'danger', msg: 'Username or password incorrect.' };
        });  
    };
}]);