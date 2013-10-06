var app = angular.module('PCApp',["ngResource","ngCookies","ngRoute","ngSanitize"]).
  config(['$routeProvider', '$locationProvider', '$httpProvider',
          function($routeProvider, $locationProvider, $httpProvider) {
              $routeProvider.
                  when('/home', {templateUrl: 'static/partials/home.html', controller: 'homeController'}).
                  when('/subscriptions', {templateUrl: 'static/partials/subscriptions.html', controller: 'subscriptionsController'}).
                  when('/suggestion', {templateUrl: 'static/partials/suggestion.html', controller: 'suggestionController'}).
                  when('/login', {templateUrl: 'static/partials/login.html', controller: 'loginController'}).
                  when('/register', {templateUrl: 'static/partials/register.html', controller: 'registerController'}).
                  otherwise({redirectTo: '/home'});
              
              var interceptor = ['$location', '$q', function($location, $q) {
                  function success(response) {
                      return response;
                  }
                  function error(response) {
                      if(response.status === 401) {
                          $location.path('/login');
                          return $q.reject(response);
                      } else {
                          return $q.reject(response);
                      }
                  }
                  return function(promise) {
                      return promise.then(success, error);
                  }
              }];
              $httpProvider.responseInterceptors.push(interceptor);
}]);