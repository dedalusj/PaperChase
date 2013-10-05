app.controller("homeController", ['$scope', 'PaperServices', function($scope, PaperServices) {
    $scope.papers = PaperServices.getPapers();
    
    $scope.selectedPaperId = undefined;
    $scope.isActive = function(paperId) {
        return paperId === $scope.selectedPaperId ? 'active' : undefined;
    };
}]);