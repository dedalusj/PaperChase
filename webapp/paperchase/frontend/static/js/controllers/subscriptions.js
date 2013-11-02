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
        journal = $scope.findJournal(journalId);
        if (journal) journal.subscribed = true;
    };
    
    $scope.unsubscribe = function($event, journalId) {
        SubscriptionAPI.remove({'journal_id': journalId});
        journal = $scope.findJournal(journalId);
        if (journal) journal.subscribed = false;
    };
    
    $scope.findJournal = function(journalId) {
        var i = 0;
        var journal = undefined;
        while (i < $scope.journals.length) {
        	if ($scope.journals[i].id === journalId) {
        	    journal = $scope.journals[i];
        	    break;
        	}
            i++;
        }
        return journal;
    };
}]);