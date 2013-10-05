app.factory('CSRFService', ['$cookies', function ($cookies) {
    return $cookies['_csrf_token'];
}]);