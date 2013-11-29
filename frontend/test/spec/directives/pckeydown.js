'use strict';

describe('Directive: pckeydown', function () {

  // load the directive's module
  beforeEach(module('paperchaseApp'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<pckeydown></pckeydown>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the pckeydown directive');
  }));
});
