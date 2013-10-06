app.controller("homeController", ['$scope', 'PaperAPI', function($scope, PaperAPI) {
    $scope.papers = PaperAPI.getPapers(function(papers, getResponseHeaders){
      for (var i=0;i<papers.length;i++)
      { 
          papers[i].created = new Date(papers[i].created);
      }
    });
    
    $scope.selectedPaperId = undefined;
    $scope.isActive = function(paperId) {
        return paperId === $scope.selectedPaperId ? 'active' : undefined;
    };
    
    $scope.selectedPaper = undefined;
    $scope.showPaper = function($event, paperId) {
        $scope.selectedPaper = PaperAPI.getPaper({'paper_id': paperId}, function(paper, getResponseHeaders){
          paper.created = new Date(paper.created);
        });
        $scope.selectedPaperId = paperId;
    };
}]);