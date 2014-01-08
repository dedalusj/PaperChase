/*jslint browser: true */

'use strict';

angular.module('paperchaseApp')
    .controller('MainCtrl', ['$scope', 'Papers', 'Journals', '$window', function ($scope, Papers, Journals, $window) {

        $scope.papers = new Papers();
        $scope.journals = Journals;
        $scope.showSubscriptions = false;

        $scope.toggleUnread = function () {
            $scope.papers = new Papers(!$scope.papers.unread,$scope.papers.since);
            $scope.papers.nextPage();
        };

        $scope.markAllRead = function () {
            $scope.papers.markAllRead();
            $scope.papers = new Papers($scope.papers.unread,$scope.papers.since);
            $scope.papers.nextPage();
        };

        $scope.$on('selected_new_item', function (event, message) {
            $scope.scrollInto('paper' + message);
        });

        $scope.scrollInto = function (idOrName) {
            //find element with the give id of name and scroll to the first element it finds
            if (!idOrName) {
                $window.scrollTo(0, 0);
            }
            //check if an element can be found with id attribute
            var el = document.getElementById(idOrName);
            if (!el) {
                //check if an element can be found with name attribute if there is no such id
                el = document.getElementsByName(idOrName);
                if (el && el.length) {
                    el = el[0];
                } else {
                    el = null;
                }
            }
            //if an element is found, scroll to the element
            if (el) {
                el.scrollIntoView(false);
            }
            //otherwise, ignore
        };
        $scope.papersActive = true;
        $scope.$on('keyPress', function (event, kind) {
            switch (kind) {
            case 'up':
                if ($scope.papersActive === true) {
                    $scope.papers.prev();
                }
                break;
            case 'down':
                if ($scope.papersActive === true) {
                    $scope.papers.next();
                }
                break;
            case 'left':
                if ($scope.papersActive === false) {
                    $scope.papersActive = true;
                }
                break;
            case 'right':
                if ($scope.papersActive === true) {
                    $scope.papersActive = false;
                }
                break;
            case 'space':
                //console.log('space');
                break;
            }
        });
    }]);