/*jslint browser: true */
'use strict';

angular.module('paperchaseApp')
    .controller('RegisterCtrl', ['$scope', '$http', 'UserServices', function ($scope, $http, UserServices) {

        $scope.alert = undefined;
        $scope.closeAlert = function () {
            $scope.alert = undefined;
        };
        $scope.registerPC = function () {
            UserServices.register($scope.email, $scope.password)
            .success(function () {
                $scope.alert = { type: 'success', msg: 'Congratulations! You will receive a confirmation email shortly. You can login <a href="#/login">here</a>' };
            }).error(function (data, status) {
                if (status === 409) {
                    $scope.alert = { type: 'danger', msg: 'The email address is already registered.' };
                }
            });
        };
    }]);