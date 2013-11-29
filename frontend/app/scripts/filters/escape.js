/*jslint browser: true */
'use strict';

angular.module('paperchaseApp')
    .filter('escape', function () {
        return window.encodeURIComponent;
    });