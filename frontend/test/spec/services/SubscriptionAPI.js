'use strict';

describe('Service: Subscriptionapi', function () {

  // load the service's module
  beforeEach(module('paperchaseApp'));

  // instantiate service
  var Subscriptionapi;
  beforeEach(inject(function (_Subscriptionapi_) {
    Subscriptionapi = _Subscriptionapi_;
  }));

  it('should do something', function () {
    expect(!!Subscriptionapi).toBe(true);
  });

});
