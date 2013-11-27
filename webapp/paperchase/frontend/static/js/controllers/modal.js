/*global app */
/*jslint browser: true */

app.controller("modalController", ['$scope', '$modalInstance', function ($scope, $modalInstance) {
    "use strict";
    $scope.close = function () {
        $modalInstance.close();
    };
}]);