app.controller("subscriptionsController", ['$scope', 'CategoryAPI', 'SubscriptionAPI', '$cacheFactory', function($scope, CategoryAPI, SubscriptionAPI, $cacheFactory){

    $scope.categories = CategoryAPI.getCategories();
    $scope.subcategories = [];
    $scope.journals = [];
    
    $scope.selectedCategoryId = undefined;
    $scope.selectedSubcategoryId = undefined;
    $scope.isActive = function(categoryId, isSubcategory) {
        // Return the class for an element of a list (active.clicked state or not) given an index and a kind
        var selectedId = isSubcategory ? $scope.selectedSubcategoryId : $scope.selectedCategoryId;
        return categoryId === selectedId ? 'active' : undefined;
    };
    
    $scope.updateSubcategories = function($event, categoryId) {
        $scope.subcategories = CategoryAPI.getSubcategories({'category_id': categoryId});
        $scope.journals = [];
        $scope.selectedCategoryId = categoryId;
        $scope.selectedSubcategoryId = -1;
    };
    
    $scope.updateJournals = function($event, categoryId) {
        if (categoryId) $scope.selectedSubcategoryId = categoryId;
        if ($scope.selectedSubcategoryId) $scope.journals = CategoryAPI.getJournals({'category_id': $scope.selectedSubcategoryId});
    };
    
    $scope.subscribe = function($event, journalId) {
        var newSubscription = new SubscriptionAPI({'journal_id': journalId});
        newSubscription.$save();
        // This is less than ideal. We should only remove the cache of the journals request
        $cacheFactory.get('$http').removeAll();
        $scope.updateJournals();
    };
    
    $scope.unsubscribe = function($event, journalId) {
        SubscriptionAPI.remove({'journal_id': journalId});
        // This is less than ideal. We should only remove the cache of the journals request
        $cacheFactory.get('$http').removeAll();
        $scope.updateJournals();
    };
}]);