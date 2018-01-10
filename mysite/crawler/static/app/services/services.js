angular.module('myApp.services', ['ngResource'])
    .factory('CrawlRequest', function($resource){
        return $resource('/api/CrawlRequest/'); 	        
    })
    .factory('CrawledImages', function($resource) {
        return $resource('/api/CrawlRequest/get_images'); 
    });