'use strict';

angular.module('myApp.crawl-requests', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/crawl-requests', {
    templateUrl: '../static/app/crawl-requests/crawl-requests.html',
    controller: 'CrawlRequestsCtrl'
  });
}])

.controller('CrawlRequestsCtrl', ['$scope','CrawlRequest', function($scope, CrawlRequest) {

  $scope.crawlRequests = [];

  $scope.loadCrawlRequests = function(){
    CrawlRequest.query().$promise
    .then(function(response){
      $scope.crawlRequests = response;
    },function(error){
      console.log('error '+error);
    });  
  }

  $scope.loadCrawlRequests(); //Load CrawlRequests on initilizing the controller.

  $scope.expand = function(){
    console.log("expand chosen");
  }

  /**
   * A function to make a crawl request using a seed_url and depth
   * @param {*} seed_url 
   * @param {*} depth 
   */
  $scope.crawl = function(seed_url, depth){
    CrawlRequest.save({'seed_url': seed_url, 'depth': depth}).$promise
    .then(function(response){
      $scope.loadCrawlRequests();
    },function(error){
      console.log('error '+error);
    });      
  }


}]);