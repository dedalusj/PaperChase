'use strict';

describe('Service: Papers', function () {

  // load the service's module
  beforeEach(module('paperchaseApp'));

  // instantiate service
  var Papers;
  beforeEach(inject(function (_Papers_) {
    Papers = _Papers_;
  }));

  it('should do something', function () {
    expect(!!Papers).toBe(true);
  });

});
