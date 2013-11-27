/*global app */
/*jslint browser: true */

app.factory('UserServices', ['$http', '$cookieStore', 'Base64', '$cookies', function ($http, $cookieStore, Base64, $cookies) {
    "use strict";
    
    var user = {isLogged: false, firstLogin: true },
        authData = $cookieStore.get('authdata'),
        firstLogin = $cookieStore.get('firstLogin');
    
    if (authData) {
        // initialize to whatever is in the cookie, if anything
        $http.defaults.headers.common['Authorization'] = 'Basic ' + authData;
        user.isLogged = true;
    }
    
    if (firstLogin !== undefined) {
        user.firstLogin = false;
    }
    
    $http.defaults.headers.post['X-CSRFToken'] = $cookies['_csrf_token'];
    $http.defaults.headers.delete = { 'X-CSRFToken' : $cookies['_csrf_token'] };
    
    return {
        verifyCredentials: function (username, password) {
            var encoded = Base64.encode(username + ':' + password),
                escaped_email = encodeURIComponent(username),
                api_address = '/api/users';
            return $http({method: 'GET', url: api_address, headers: {'Authorization': 'Basic '.concat(encoded)}});
        },
        setCredentials: function (username, password) {
            var encoded = Base64.encode(username + ':' + password);
            $http.defaults.headers.common.Authorization = 'Basic ' + encoded;
            user.isLogged = true;
            $cookieStore.put('authdata', encoded);
            if (user.firstLogin === true) {
                $cookieStore.put('firstLogin', false);
            }
        },
        clearCredentials: function () {
            document.execCommand("ClearAuthenticationCache");
            $http.defaults.headers.common.Authorization = 'Basic ';
            user.isLogged = false;
            $cookieStore.remove('authdata');
        },
        isLogged: function () {
            return user.isLogged;
        },
        hasLoggedInBefore: function () {
            return !user.firstLogin;
        }
    };
}]);