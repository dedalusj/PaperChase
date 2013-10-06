app.controller("homeController", ['$scope', 'Papers', function($scope, Papers) {
    $scope.papers = new Papers();
    
    $scope.selectedPaperId = undefined;
    $scope.isActive = function(paperId) {
        return paperId === $scope.selectedPaperId ? 'active' : undefined;
    };
    
    $scope.selectedPaper = undefined;
    $scope.showPaper = function($event, paperId) {
        $scope.papers.updateCurrentPaper(paperId);
        $scope.selectedPaperId = paperId;
    };
}]);