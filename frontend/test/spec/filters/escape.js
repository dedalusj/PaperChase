'use strict';

describe('Filter: escape', function () {

  // load the filter's module
  beforeEach(module('paperchaseApp'));

  // initialize a new instance of the filter before each test
  var escape;
  beforeEach(inject(function ($filter) {
    escape = $filter('escape');
  }));

  it('should return the input prefixed with "escape filter:"', function () {
    var text = 'angularjs';
    expect(escape(text)).toBe('escape filter: ' + text);
  });

});
