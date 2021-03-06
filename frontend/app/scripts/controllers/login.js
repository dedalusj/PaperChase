/*jslint browser: true */

'use strict';

angular.module('paperchaseApp')
    .controller('LoginCtrl', ['$scope', '$http', '$location', 'UserServices', function ($scope, $http, $location, UserServices) {

        $scope.alert = undefined;

        $scope.closeAlert = function () {
            $scope.alert = undefined;
        };

        $scope.loginPC = function () {
            UserServices.verifyCredentials($scope.email, $scope.password).
                success(function () {
                    UserServices.setCredentials($scope.email, $scope.password);
                    $location.path('/home');
                }).
                error(function () {
                    $scope.alert = { type: 'danger', msg: 'Username or password incorrect.' };
                });
        };
    }]);