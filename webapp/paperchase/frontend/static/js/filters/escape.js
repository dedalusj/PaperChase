/*global app */
/*jslint browser: true */

app.filter('escape', function () {
    "use strict";
    
    return window.encodeURIComponent;
});