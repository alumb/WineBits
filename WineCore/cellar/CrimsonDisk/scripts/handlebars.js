define([], function(){

    Handlebars.registerHelper('capitalize', function(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    });

});
