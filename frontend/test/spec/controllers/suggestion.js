'use strict';

describe('Controller: SuggestionCtrl', function () {

  // load the controller's module
  beforeEach(module('paperchaseApp'));

  var SuggestionCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    SuggestionCtrl = $controller('SuggestionCtrl', {
      $scope: scope
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(scope.awesomeThings.length).toBe(3);
  });
});
