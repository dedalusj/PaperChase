'use strict';

describe('Service: Journals', function () {

  // load the service's module
  beforeEach(module('paperchaseApp'));

  // instantiate service
  var Journals;
  beforeEach(inject(function (_Journals_) {
    Journals = _Journals_;
  }));

  it('should do something', function () {
    expect(!!Journals).toBe(true);
  });

});
