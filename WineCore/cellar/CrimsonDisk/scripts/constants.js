define([], function(){

    var DEV_LOCATION = "http://localhost:8081";
    var PROD_LOCATION = "https://winebits.appspot.com";

    var SERVER_LOCATION = DEV_LOCATION;
    var TRUTH_LOCATION = SERVER_LOCATION + "/truth";

    var VARIETAL_LOCATION = TRUTH_LOCATION + "/varietal";
    var WINETYPE_LOCATION = TRUTH_LOCATION + "/winetype";

    VARIETALS = localStorage.getItem('varietals');
    WINETYPES = localStorage.getItem('winetypes');

    if( VARIETALS === null ){
        console.log("Loading varietals from server.");
        $.getJSON( VARIETAL_LOCATION, function(data){
            VARIETALS = data;
            localStorage.setItem('varietals', VARIETALS);
        });
    }
    else{
        console.log("Loading varietals from memory.");
        VARIETALS = VARIETALS.split(",");
    }

    var varietals = function(){
        return VARIETALS;
    }
    
    if( WINETYPES === null ){
        console.log("Loading winetypes from server.");
        $.getJSON( WINETYPE_LOCATION, function(data){
            WINETYPES = data;
            localStorage.setItem('winetypes', WINETYPES);
        });
    }
    else{
        console.log("Loading winetypes from memory.");
        WINETYPES = WINETYPES.split(",");
    }

    var varietals = function(){
        return VARIETALS;
    }

    var winetypes = function(){
        return WINETYPES;
    }
    
    return {
        SERVER_LOCATION: SERVER_LOCATION,
        TRUTH_LOCATION: TRUTH_LOCATION,
        varietals: varietals,
        winetypes: winetypes
    };

});
