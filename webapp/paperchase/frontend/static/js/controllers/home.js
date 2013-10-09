app.controller("homeController", ['$scope', 'Papers', function($scope, Papers) {
    $scope.papers = new Papers();
    
    $scope.unreadFilter = true;
    $scope.toggleUnread = function() {
        $scope.unreadFilter = !$scope.unreadFilter;
        if ($scope.unreadFilter == true) $scope.papers.showUnread();
        else $scope.papers.showAll();
    };
}]);