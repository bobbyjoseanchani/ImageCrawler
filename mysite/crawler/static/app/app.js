'use strict';

// Declare app level module which depends on views, and components
angular.module('myApp', [
  'ngRoute',
  'ngResource',
  'myApp.services',
  'myApp.crawl-requests',
  'myApp.crawled-images',
  'myApp.version'
])
.config(['$locationProvider', '$routeProvider', '$resourceProvider', function($locationProvider, $routeProvider, $resourceProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;
  $locationProvider.hashPrefix('!');
  $routeProvider.otherwise({redirectTo: '/crawl-requests'});
}]);
