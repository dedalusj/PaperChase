/*global app */
/*jslint browser: true */

app.filter('htmlToPlainText', function () {
    "use strict";
    
    return function (text) {
        return String(text).replace(/<(?:.|\n)*?>/gm, '');
    };
});