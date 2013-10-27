app.controller("registerController", ['$scope', '$http', '$location', 'UserServices', function($scope, $http, $location, UserServices) {
    $scope.alert = undefined;
    $scope.closeAlert = function() {
        $scope.alert = undefined;
    };
    $scope.registerPC = function() {
        var postData = {email: $scope.email, 
                        password: $scope.password};
        $http({
            url: 'http://localhost:5000/api/register',
            method: "POST",
            data: angular.toJson(postData),
            headers: {'Content-Type': 'application/json'}
        }).success(function() {
            $scope.alert = { type: 'success', msg: 'Congratulations! You will receive a confirmation email shortly. <a href="#/login">Login here</a>' };
        }).error(function(data, status, headers, config) {
            if (status == 409) {
                $scope.alert = { type: 'danger', msg: 'The email address is already registered.' };
            }
        });
    };
}]);