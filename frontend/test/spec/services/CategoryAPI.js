'use strict';

describe('Service: Categoryapi', function () {

  // load the service's module
  beforeEach(module('paperchaseApp'));

  // instantiate service
  var Categoryapi;
  beforeEach(inject(function (_Categoryapi_) {
    Categoryapi = _Categoryapi_;
  }));

  it('should do something', function () {
    expect(!!Categoryapi).toBe(true);
  });

});
