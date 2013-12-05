/*jslint browser: true */
'use strict';

angular.module('paperchaseApp')
    .factory('UserServices', ['$http', '$cookieStore', '$base64', '$cookies', function ($http, $cookieStore, $base64, $cookies) {
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
                var encoded = $base64.encode(username + ':' + password),
                    apiAddress = '/api/users';
                return $http({method: 'GET', url: apiAddress, headers: {'Authorization': 'Basic '.concat(encoded)}});
            },
            setCredentials: function (username, password) {
                var encoded = $base64.encode(username + ':' + password),
                    apiAddress = '/api/users/token';
                $http({method: 'GET', url: apiAddress, headers: {'Authorization': 'Basic '.concat(encoded)}}).
                success(function (data) {
                    encoded = $base64.encode(data.token + ':unused')
                    $http.defaults.headers.common.Authorization = 'Basic ' + encoded;
                    user.isLogged = true;
                    $cookieStore.put('authdata', encoded);
                    $cookieStore.put('authexpire', data.duration);
                    if (user.firstLogin === true) {
                        $cookieStore.put('firstLogin', false);
                    }
                }).
                error();
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