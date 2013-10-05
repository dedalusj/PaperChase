app.controller("subscriptionsController", ['$scope', 'CategoryServices', 'SubscriptionAPI', function($scope, CategoryServices, SubscriptionAPI){

    $scope.categories = CategoryServices.getCategories();
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
        $scope.subcategories = CategoryServices.getSubcategories(categoryId);
        $scope.journals = [];
        $scope.selectedCategoryId = categoryId;
        $scope.selectedSubcategoryId = -1;
    };
    
    $scope.updateJournals = function($event, categoryId) {
        if (categoryId) $scope.selectedSubcategoryId = categoryId;
        if ($scope.selectedSubcategoryId) $scope.journals = CategoryServices.getJournals($scope.selectedSubcategoryId);
    };
    
    $scope.subscribe = function($event, journalId) {
        var newSubscription = new SubscriptionAPI({journal_id: journalId});
        newSubscription.$save();
        CategoryServices.clearJournals();
        $scope.updateJournals();
    };
    
    $scope.unsubscribe = function($event, journalId) {
        SubscriptionAPI.remove({'journal_id': journalId});
        CategoryServices.clearJournals();
        $scope.updateJournals();
    };
}]);