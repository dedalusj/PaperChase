'use strict';

describe('Service: Paperapi', function () {

  // load the service's module
  beforeEach(module('paperchaseApp'));

  // instantiate service
  var Paperapi;
  beforeEach(inject(function (_Paperapi_) {
    Paperapi = _Paperapi_;
  }));

  it('should do something', function () {
    expect(!!Paperapi).toBe(true);
  });

});
