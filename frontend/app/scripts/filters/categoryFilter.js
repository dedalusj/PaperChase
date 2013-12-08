'use strict';

var belongsTo = function (a, b) {
    var bIndex;
    for (bIndex = 0; bIndex < b.length; bIndex += 1) {
        if (a === b[bIndex]) {
            return true;
        }
    }
    return false;
};

angular.module('paperchaseApp')
.filter('categoryFilter', function () {
        return function (journals, category, subcategory) {
            // if category is undefined then simply don't filter
            if (!category.id) {
                return journals;
            }

            var filteredJournals = [];
            angular.forEach(journals, function (journal) {
                if (subcategory) {
                    // if subcategory is defined then we filter on that and forget everything else
                    if (belongsTo(subcategory.id, journal.categories)) {
                        filteredJournals.push(journal);
                    }
                } else {
                    journal.categories.sort(function(a, b) {
                            return a - b;
                        });

                    if (belongsTo(category.id, journal.categories)) {
                        // direct filter on category
                        filteredJournals.push(journal);
                    } else {

                        // check for parent child relationship
                        category.subcategories.sort(function(a, b) {
                            return a.id - b.id;
                        });

                        var journalIndex=0,
                            categoryIndex=0;

                        while( journalIndex < journal.categories.length && categoryIndex < category.subcategories.length ) {
                            if (journal.categories[journalIndex] < category.subcategories[categoryIndex].id) {
                                journalIndex += 1;
                            } else if (journal.categories[journalIndex] > category.subcategories[categoryIndex].id) {
                                categoryIndex += 1;
                            } else {
                                filteredJournals.push(journal);
                                journalIndex += 1;
                                categoryIndex += 1;
                            }
                        }
                    }
                }
            });

            return filteredJournals;
        };
    });
