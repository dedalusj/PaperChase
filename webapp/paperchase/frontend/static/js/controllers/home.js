app.controller("homeController", ['$scope', 'Papers', function($scope, Papers) {
    $scope.papers = new Papers();
    
    $scope.unreadFilter = true;
    $scope.toggleUnread = function() {
        $scope.unreadFilter = !$scope.unreadFilter;
        if ($scope.unreadFilter == true) $scope.papers.showUnread();
        else $scope.papers.showAll();
    };
    
    $scope.markAllRead = function() {
        $scope.papers.markAllRead();
    };
    
    $scope.papersActive = true;
    
    $scope.$on('keyPress', function(event, kind) {
        switch (kind) {
          case 'up':
            if ($scope.papersActive === true) $scope.papers.prev();
            break;
          case 'down':
            if ($scope.papersActive === true) $scope.papers.next();
            break;
          case 'left':
            if ($scope.papersActive === false) $scope.papersActive = true;
            break;
          case 'right':
            if ($scope.papersActive === true) $scope.papersActive = false;
            break;
          case 'space':
            console.log('space');
            break;
        }
    });
}]);