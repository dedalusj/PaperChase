'use strict';

describe('Filter: htmlToPlainText', function () {

  // load the filter's module
  beforeEach(module('paperchaseApp'));

  // initialize a new instance of the filter before each test
  var htmlToPlainText;
  beforeEach(inject(function ($filter) {
    htmlToPlainText = $filter('htmlToPlainText');
  }));

  it('should return the input prefixed with "htmlToPlainText filter:"', function () {
    var text = 'angularjs';
    expect(htmlToPlainText(text)).toBe('htmlToPlainText filter: ' + text);
  });

});
