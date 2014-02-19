require([], function(){

    function main(){

    }

    if (navigator.userAgent.match(/(iPhone|iPod|iPad|Android|BlackBerry)/)) {
        document.addEventListener("deviceready", main, false);
    } else {
        main();
    }

});
