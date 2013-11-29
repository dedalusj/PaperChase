/*jslint browser: true */
'use strict';

angular.module('paperchaseApp')
    .controller('GlobalCtrl', ['$scope', '$location', 'UserServices', '$modal', function ($scope, $location, UserServices, $modal) {
        $scope.isLogged = function () {
            return UserServices.isLogged();
        };
        $scope.logoutPC = function () {
            UserServices.clearCredentials();
            $location.path('/login');
        };
        $scope.isActive = function (route) {
            return route === $location.path();
        };
        $scope.keyPressed = function (kind) {
            $scope.$broadcast('keyPress', kind);
        };

        $scope.firstLogin = function () {
            var modalInstance = $modal.open({
                templateUrl: 'views/firstlogin.html',
                controller: 'ModalCtrl',
                resolve: {}
            });
            modalInstance.result.then(function () {
                //console.log("I'm done");
                $location.path('/subscriptions');
            }, function () {
                //console.log("Dismissed");
            });
        };
    }]);