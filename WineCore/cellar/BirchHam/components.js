angular.module('components', [] )

.directive('wineryselect', function(){
    return {
        restrict: "E", 
        transclude: false, 
        scope:{ 
        }, 
        template: ''+
        '<div class="input-group">'+
            '<input type="text" ng-model="thing" ng-keyup="winery()" placeholder="Winery" name="winery"></input>'+
            '<input type="text" placeholder="Canada - British Columbia: Okanagan Valley"></input>'+
        '</div>', 
        controller: function($scope, $element){
            $scope.thing = "" 
            $scope.winery = function(){
                console.log($scope.thing);
            }
        },
        replace: true

    }
})
