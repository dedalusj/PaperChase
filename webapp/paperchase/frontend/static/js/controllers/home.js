app.controller("homeController", ['$scope', 'Papers', function($scope, Papers) {
    $scope.papers = new Papers();
}]);