/*jslint browser: true */
'use strict';

angular.module('paperchaseApp')
    .directive('pwCheck', function () {
        return {
            require: 'ngModel',
            link: function (scope, elem, attrs, ctrl) {
                var otherInput = elem.inheritedData('$formController')[attrs.pwCheck];
                ctrl.$parsers.push(function (value) {
                    if (value === otherInput.$viewValue) {
                        ctrl.$setValidity('pwmatch', true);
                        return value;
                    }
                    ctrl.$setValidity('pwmatch', false);
                });
                otherInput.$parsers.push(function (value) {
                    ctrl.$setValidity('pwmatch', value === ctrl.$viewValue);
                    return value;
                });
            }
        };
    });