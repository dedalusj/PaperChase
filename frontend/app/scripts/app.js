'use strict';

angular.module('paperchaseApp', [
    'ngCookies',
    'ngResource',
    'ngSanitize',
    'ngRoute',
    'infinite-scroll',
    'ui.bootstrap',
    'ngBase64',
    'LocalStorageModule'
])
.config(['localStorageServiceProvider', function(localStorageServiceProvider){
    localStorageServiceProvider.setPrefix('paperchase');
}])
.config(['$routeProvider', '$locationProvider', '$httpProvider', '$compileProvider',
    function ($routeProvider, $locationProvider, $httpProvider, $compileProvider) {
        $routeProvider
        .when('/', {
            templateUrl: 'views/main.html',
            controller: 'MainCtrl'
        })
        .when('/subscriptions', {
            templateUrl: 'views/subscriptions.html',
            controller: 'SubscriptionpageCtrl'
        })
        .when('/login', {
            templateUrl: 'views/login.html',
            controller: 'LoginCtrl'
        })
        .when('/register', {
            templateUrl: 'views/register.html',
            controller: 'RegisterCtrl'
        })
        .otherwise({
            redirectTo: '/'
        });

        $httpProvider.interceptors.push(['$q', '$location', function($q, $location) {
            return {
                'request': function (config) {
                    config.headers['X-StatusOnLoginFail'] = '403';
                    return config;
                },
                'responseError': function (rejection) {
                    if (rejection.status === 403) {
                        $location.path('/login');
                        return $q.reject(rejection);
                    }
                    return $q.reject(rejection);
                }
            };
        }]);


        $compileProvider.aHrefSanitizationWhitelist(/^\s*(https?|ftp|mailto|file|papers):/);
    }]);