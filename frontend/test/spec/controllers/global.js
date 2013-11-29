'use strict';

describe('Controller: GlobalCtrl', function () {

  // load the controller's module
  beforeEach(module('paperchaseApp'));

  var GlobalCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    GlobalCtrl = $controller('GlobalCtrl', {
      $scope: scope
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(scope.awesomeThings.length).toBe(3);
  });
});
