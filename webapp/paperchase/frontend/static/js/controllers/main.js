app.controller("mainController", ['$scope', '$location', 'UserServices', function($scope, $location, UserServices) {
    $scope.isLogged = function() {
        return UserServices.isLogged();
    };
    $scope.logoutPC = function() {
        UserServices.clearCredentials();
        $location.path( "/login" );
    };
    $scope.isActive = function(route) {
        return route === $location.path();
    };
    $scope.keyPressed = function(kind) {
        $scope.$broadcast('keyPress',kind);
    };
}]);