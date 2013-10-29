app.controller("modalController", ['$scope', '$modalInstance', function($scope, $modalInstance) {

  $scope.close = function () {
    $modalInstance.close();
  };

}]);