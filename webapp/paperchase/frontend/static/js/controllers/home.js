app.controller("homeController", ['$scope', 'PaperServices', function($scope, PaperServices) {
    $scope.papers = PaperServices.getPapers(function(papers, getResponseHeaders){
      for (var i=0;i<papers.length;i++)
      { 
          papers[i].created = new Date(papers[i].created);
          console.log(papers[i]);
      }
    });
    
    $scope.selectedPaperId = undefined;
    $scope.isActive = function(paperId) {
        return paperId === $scope.selectedPaperId ? 'active' : undefined;
    };
}]);