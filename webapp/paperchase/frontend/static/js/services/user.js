app.factory('UserServices', ['$http', '$cookieStore', 'Base64', '$cookies', function ($http, $cookieStore, Base64, $cookies) {
    
    var user = { isLogged: false };
    authData = $cookieStore.get('authdata');
    
    if (authData) {
        // initialize to whatever is in the cookie, if anything
        $http.defaults.headers.common['Authorization'] = 'Basic ' + authData;
        user.isLogged = true;
    }
    
    $http.defaults.headers.post['X-CSRFToken'] = $cookies['_csrf_token'];
    $http.defaults.headers.delete = { 'X-CSRFToken' : $cookies['_csrf_token'] };
    
    return {
        verifyCredentials: function(username, password) {
            var encoded = Base64.encode(username + ':' + password);
            var escaped_email = encodeURIComponent(username);
            var api_address = 'http://localhost:5000/api/users';
            return $http({method: 'GET', url: api_address, headers: {'Authorization': 'Basic '.concat(encoded)}});
        },
        setCredentials: function (username, password) {
            var encoded = Base64.encode(username + ':' + password);
            $http.defaults.headers.common.Authorization = 'Basic ' + encoded;
            user.isLogged = true;
            $cookieStore.put('authdata', encoded);
        },
        clearCredentials: function () {
            document.execCommand("ClearAuthenticationCache");
            $http.defaults.headers.common.Authorization = 'Basic ';
            user.isLogged = false;
            $cookieStore.remove('authdata');
        },
        isLogged: function() {
            return user.isLogged;
        }
    };
}]);