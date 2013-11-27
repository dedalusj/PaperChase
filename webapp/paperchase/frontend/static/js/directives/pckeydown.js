/*global app */
/*jslint browser: true */

app.directive('pcKeydown', function () {
    "use strict";
    
    return function (scope, elm, attr) {
        elm.bind('keydown', function (e) {
            switch (e.keyCode) {
            case 34: // PgDn
            case 39: // right arrow
                return scope.$apply(attr.pcRight);

            case 40: // down arrow
                return scope.$apply(attr.pcDown);

            case 32: // Space
                e.preventDefault();
                return scope.$apply(attr.pcSpace);

            case 33: // PgUp
            case 37: // left arrow
                return scope.$apply(attr.pcLeft);

            case 38: // up arrow
                return scope.$apply(attr.pcUp);

            case 85: // U

            }
        });
    };
});