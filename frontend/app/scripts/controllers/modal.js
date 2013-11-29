/*jslint browser: true */

'use strict';

angular.module('paperchaseApp')
    .controller('ModalCtrl', ['$scope', '$modalInstance', function ($scope, $modalInstance) {
        $scope.close = function () {
            $modalInstance.close();
        };
    }]);