/*jslint browser: true */
'use strict';

angular.module('paperchaseApp')
    .filter('htmlToPlainText', function () {
        return function (text) {
            return String(text).replace(/<(?:.|\n)*?>/gm, '');
        };
    });