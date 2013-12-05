/*jslint browser: true */
'use strict';

angular.module('paperchaseApp')
    .controller('RegisterCtrl', ['$scope', '$http', function ($scope, $http) {

        $scope.alert = undefined;
        $scope.closeAlert = function () {
            $scope.alert = undefined;
        };
        $scope.registerPC = function () {
            var postData = {email: $scope.email, password: $scope.password};
            $http({
                url: '/api/register',
                method: 'POST',
                data: angular.toJson(postData),
                headers: {'Content-Type': 'application/json'}
            }).success(function () {
                $scope.alert = { type: 'success', msg: 'Congratulations! You will receive a confirmation email shortly. You can login <a href="#/login">here</a>' };
            }).error(function (data, status) {
                if (status === 409) {
                    $scope.alert = { type: 'danger', msg: 'The email address is already registered.' };
                }
            });
        };
    }]);