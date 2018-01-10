'use strict';

angular.module('myApp.crawled-images', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/crawled-images/:id', {
    templateUrl: '../static/app/crawled-images/crawled-images.html',
    controller: 'CrawledImagesCtrl'
  });
}])

.controller('CrawledImagesCtrl', ['$scope', '$routeParams', 'CrawledImages', function($scope, $routeParams, CrawledImages) {
  $scope.requestDetails;
  CrawledImages.query({'id': $routeParams.id}).$promise
  .then(function(response){
    console.log(response.length);
    if(response.length > 0){
      $scope.requestDetails = response[0];      
    }
  }, function(error){
    console.log(error);
  });
}]);