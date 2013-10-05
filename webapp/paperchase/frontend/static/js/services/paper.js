app.factory('PaperServices', ['PaperAPI', function(PaperAPI) {
    var papersData;
    var papers = function(callback) {
        papersData = PaperAPI.query(callback);
        return papersData;
    }

    return {
        getPapers: function(callback) {
            if(papersData) {
                return papersData;
            } else {
                return papers(callback); 
            }
        },
        clearCategories: function() {
            papersData = undefined; 
        }
    };
}]);