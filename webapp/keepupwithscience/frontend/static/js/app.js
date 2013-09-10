var app = angular.module('KUWSApp',["ngResource"]).
  config(['$routeProvider', function($routeProvider) {
  $routeProvider.
      when('/home', {templateUrl: 'static/partials/home.html', controller: 'categoryController'}).
      when('/suggestion', {templateUrl: 'static/partials/suggestion.html', controller: 'suggestionController'}).
      when('/login', {templateUrl: 'static/partials/login.html', controller: 'loginController'}).
      otherwise({redirectTo: '/home'});
}]);