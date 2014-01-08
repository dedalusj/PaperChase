/*jslint browser: true */
'use strict';

angular.module('paperchaseApp')
    .factory('UserServices', ['$http', 'localStorageService', '$base64', '$cookies', function ($http, localStorageService, $base64, $cookies) {
        var user = {isLogged: false },
            authData = localStorageService.get('authData');

        if (authData) {
            // initialize to whatever is in the cookie, if anything
            $http.defaults.headers.common.Authorization = 'Basic ' + authData;
            user.isLogged = true;
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
                    encoded = $base64.encode(data.token + ':unused');
                    $http.defaults.headers.common.Authorization = 'Basic ' + encoded;
                    user.isLogged = true;
                    localStorageService.set('authData', encoded);
                    localStorageService.set('authExpire', data.duration);
                }).
                error();
            },
            clearCredentials: function () {
                document.execCommand('ClearAuthenticationCache');
                $http.defaults.headers.common.Authorization = 'Basic ';
                user.isLogged = false;
                localStorageService.remove('authData');
            },
            isLogged: function () {
                return user.isLogged;
            },
            register: function (username, password) {
                var postData = {email: username, password: password};
                return $http({
                    url: '/api/register',
                    method: 'POST',
                    data: angular.toJson(postData),
                    headers: {'Content-Type': 'application/json'}
                });
            }
        };
    }]);