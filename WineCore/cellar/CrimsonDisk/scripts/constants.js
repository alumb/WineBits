define([], function(){

var DEV_LOCATION = "http://localhost:8081";
var PROD_LOCATION = "https://winebits.appspot.com";

var SERVER_LOCATION = DEV_LOCATION;
var TRUTH_LOCATION = SERVER_LOCATION + "/truth";
    
    return {
        SERVER_LOCATION: SERVER_LOCATION,
        TRUTH_LOCATION: TRUTH_LOCATION
    };

});
