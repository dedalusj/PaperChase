app.factory('Base64', function() {
    var keyStr = 'ABCDEFGHIJKLMNOP' +
        'QRSTUVWXYZabcdef' +
        'ghijklmnopqrstuv' +
        'wxyz0123456789+/' +
        '=';
    return {
        encode: function (input) {
            var output = "";
            var chr1, chr2, chr3 = "";
            var enc1, enc2, enc3, enc4 = "";
            var i = 0;
 
            do {
                chr1 = input.charCodeAt(i++);
                chr2 = input.charCodeAt(i++);
                chr3 = input.charCodeAt(i++);
 
                enc1 = chr1 >> 2;
                enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
                enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
                enc4 = chr3 & 63;
 
                if (isNaN(chr2)) {
                    enc3 = enc4 = 64;
                } else if (isNaN(chr3)) {
                    enc4 = 64;
                }
 
                output = output +
                    keyStr.charAt(enc1) +
                    keyStr.charAt(enc2) +
                    keyStr.charAt(enc3) +
                    keyStr.charAt(enc4);
                chr1 = chr2 = chr3 = "";
                enc1 = enc2 = enc3 = enc4 = "";
            } while (i < input.length);
 
            return output;
        },
 
        decode: function (input) {
            var output = "";
            var chr1, chr2, chr3 = "";
            var enc1, enc2, enc3, enc4 = "";
            var i = 0;
 
            // remove all characters that are not A-Z, a-z, 0-9, +, /, or =
            var base64test = /[^A-Za-z0-9\+\/\=]/g;
            if (base64test.exec(input)) {
                alert("There were invalid base64 characters in the input text.\n" +
                    "Valid base64 characters are A-Z, a-z, 0-9, '+', '/',and '='\n" +
                    "Expect errors in decoding.");
            }
            input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");
 
            do {
                enc1 = keyStr.indexOf(input.charAt(i++));
                enc2 = keyStr.indexOf(input.charAt(i++));
                enc3 = keyStr.indexOf(input.charAt(i++));
                enc4 = keyStr.indexOf(input.charAt(i++));
 
                chr1 = (enc1 << 2) | (enc2 >> 4);
                chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
                chr3 = ((enc3 & 3) << 6) | enc4;
 
                output = output + String.fromCharCode(chr1);
 
                if (enc3 != 64) {
                    output = output + String.fromCharCode(chr2);
                }
                if (enc4 != 64) {
                    output = output + String.fromCharCode(chr3);
                }
 
                chr1 = chr2 = chr3 = "";
                enc1 = enc2 = enc3 = enc4 = "";
 
            } while (i < input.length);
 
            return output;
        }
    };
});

app.factory('UserServices', ['$http', '$cookieStore', 'Base64', function ($http, $cookieStore, Base64) {
    
    var user = { isLogged: false };
    authData = $cookieStore.get('authdata');
    
    if (authData) {
        // initialize to whatever is in the cookie, if anything
        $http.defaults.headers.common['Authorization'] = 'Basic ' + authData;
        user.isLogged = true;
    }
    
    return {
        verifyCredentials: function(username, password) {
            var encoded = Base64.encode(username + ':' + password);
            var escaped_email = encodeURIComponent(username);
            var api_address = 'http://localhost:5000/api/users/'.concat(escaped_email);
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

app.factory('CategoryAPI', ['$http', '$resource', function($http, $resource) {
    // Define the resource for the category API to be shared by all other services and controllers
    return $resource('http://localhost\\:5000/api/categories/:categoryId/:resource',{categoryId:'@id', resource: '@res'});
}]);

app.factory('CategoryServices', ['CategoryAPI', function(CategoryAPI) {
    // defines a categories service that can load the list from the backend and can cache it 
    var categoriesData;
    var categories = function(callback) {
        categoriesData = CategoryAPI.query(callback);
        return categoriesData;
    }

    var subcategoriesData;
    var mainCategoryId;
    var subcategories = function(parentId, callback) {
        mainCategoryId = parentId;
        subcategoriesData = CategoryAPI.query({categoryId: parentId, resource: 'subcategories'},callback);
        return subcategoriesData;
    }
    
    var journalsData;
    var categoryId;
    var journals = function(catId, callback) {
        categoryId = catId;
        journalsData = CategoryAPI.query({categoryId: catId, resource: 'journals'},callback);
        return journalsData;
    }

    return {
        getCategories: function(callback) {
            if(categoriesData) {
                return categoriesData;
            } else {
                return categories(callback); 
            }
        },
        getSubcategories: function(parentId, callback) {
            if (subcategoriesData && parentId === mainCategoryId) {
                return subcategoriesData;
            } else {
                return subcategories(parentId, callback); 
            }
        },
        getJournals: function(catId, callback) {
            if (journalsData && catId === categoryId) {
                return journalsData;
            } else {
                return journals(catId, callback); 
            }
        },
        clearCategories: function() {
            categforiesData = undefined; 
        },
        clearSubcategories: function() {
            subcategoriesData = undefined;
        },
        clearJournals: function() {
            journalsData = undefined;
        }
    };
}]);

app.factory('SubscriptionAPI', ['$http', '$resource', function($http, $resource) {
    // Define the resource for the category API to be shared by all other services and controllers
    return $resource('http://localhost\\:5000/api/subscriptions/:journal_id',{journal_id:'@id'});
}]);