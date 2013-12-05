/*jslint browser: true */

'use strict';

angular.module('paperchaseApp')
    .controller('MainCtrl', ['$scope', 'Papers', '$window', function ($scope, Papers, $window) {

        $scope.papers = new Papers();

        $scope.unreadFilter = true;
        $scope.toggleUnread = function () {
            $scope.unreadFilter = !$scope.unreadFilter;
            if ($scope.unreadFilter === true) {
                $scope.papers.showUnread();
            } else {
                $scope.papers.showAll();
            }
        };

        $scope.markAllRead = function () {
            $scope.papers.markAllRead();
            $scope.papers.resetPapers();
        };

        $scope.toggleReadSelected = function () {
            $scope.papers.toggleRead();
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