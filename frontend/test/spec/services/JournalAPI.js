'use strict';

describe('Service: Journalapi', function () {

  // load the service's module
  beforeEach(module('paperchaseApp'));

  // instantiate service
  var Journalapi;
  beforeEach(inject(function (_Journalapi_) {
    Journalapi = _Journalapi_;
  }));

  it('should do something', function () {
    expect(!!Journalapi).toBe(true);
  });

});
