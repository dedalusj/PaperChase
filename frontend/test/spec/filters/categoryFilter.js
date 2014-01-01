'use strict';

describe('Filter: categoryFilter', function () {

  // load the filter's module
  beforeEach(module('paperchaseApp'));

  // initialize a new instance of the filter before each test
  var categoryFilter;
  beforeEach(inject(function ($filter) {
    categoryFilter = $filter('categoryFilter');
  }));

  it('should return the input prefixed with "categoryFilter filter:"', function () {
    var text = 'angularjs';
    expect(categoryFilter(text)).toBe('categoryFilter filter: ' + text);
  });

});
