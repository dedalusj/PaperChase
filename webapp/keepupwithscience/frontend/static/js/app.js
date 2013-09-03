var app = angular.module('KUWSApp',["ngResource"]).
  config(['$routeProvider', function($routeProvider) {
  $routeProvider.
      when('/home', {templateUrl: 'static/partials/home.html', controller: 'categoryController'}).
      when('/suggestion', {templateUrl: 'static/partials/suggestion.html', controller: 'suggestionController'}).
      otherwise({redirectTo: '/home'});
}]);