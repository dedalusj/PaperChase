'use strict';

describe('Service: Base64', function () {

  // load the service's module
  beforeEach(module('paperchaseApp'));

  // instantiate service
  var Base64;
  beforeEach(inject(function (_Base64_) {
    Base64 = _Base64_;
  }));

  it('should do something', function () {
    expect(!!Base64).toBe(true);
  });

});
