'use strict';

angular.module('paperchaseApp', [
    'ngCookies',
    'ngResource',
    'ngSanitize',
    'ngRoute',
    'infinite-scroll',
    'ui.bootstrap'
])
    .config(['$routeProvider', '$locationProvider', '$httpProvider', '$compileProvider',
            function ($routeProvider, $locationProvider, $httpProvider, $compileProvider) {
            $routeProvider
                .when('/', {
                    templateUrl: 'views/main.html',
                    controller: 'MainCtrl'
                })
                .when('/subscriptions', {
                    templateUrl: 'views/subscriptions.html',
                    controller: 'SubscriptionsCtrl'
                })
                .when('/login', {
                    templateUrl: 'views/login.html',
                    controller: 'LoginCtrl'
                })
                .when('/register', {
                    templateUrl: 'views/register.html',
                    controller: 'RegisterCtrl'
                })
                .when('/suggestion', {
                    templateUrl: 'views/suggestion.html',
                    controller: 'SuggestionCtrl'
                })
                .otherwise({
                    redirectTo: '/'
                });

            var interceptor = ['$location', '$q', function ($location, $q) {
                    function success(response) {
                        return response;
                    }
                    function error(response) {
                        if (response.status === 401) {
                            $location.path('/login');
                            return $q.reject(response);
                        }
                        return $q.reject(response);
                    }
                    return function (promise) {
                        return promise.then(success, error);
                    };
                }];
            $httpProvider.responseInterceptors.push(interceptor);
            $compileProvider.aHrefSanitizationWhitelist(/^\s*(https?|ftp|mailto|file|papers):/);
        }]);