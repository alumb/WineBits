requirejs.config({
    waitSeconds:5
});

require(["nav", 
         "search", 
         "wine", 
         "winery", 
         "handlebars"], function(nav, search, wine, winery, handlebars){

    if (nav === undefined || search === undefined || wine === undefined ||
            winery === undefined){
        console.error("module missing.");
        console.log("Nav:");
        console.log(nav);
        console.log("Search:");
        console.log(search);
        console.log("Wine:");
        console.log(wine);
        console.log("Winery:");
        console.log(winery);
    }
    
    
    var MainRouter = Backbone.Router.extend({
        routes: {
            "home":                         "home",
            "search/:query":                "search",
            "winery/:winery":               "winery",
            "winery/:winery/wine/:wine":    "wine"
        },
        initialize: function(){
            this.Nav = new nav.NavView({ router:this });
        },
        home: function(){
            this.App = new search.SearchView({ router:this });
            this.Nav.model.set("navstate", "search");
            this.listenTo(this.App.searchmodel, 'change', this.update_nav);
        },
        search: function(query){
            this.App = new search.SearchView({ router:this });
            this.App.searchmodel.set("searchterm", query);
            this.Nav.model.set("navstate", "search");
            this.listenTo(this.App.searchmodel, 'change', this.update_nav);
        },
        update_nav: function(model){
            app.navigate("search/"+model.get('searchterm'))
        },
        wine: function(winery_id, wine_id){
            this.App = new wine.WineView({ router:this });
            this.Nav.model.set("navstate", "wine");
            this.App.load_wine(winery_id, wine_id);
        },
        winery: function(winery_id){
            this.App = new winery.WineryView({ router:this });
            this.Nav.model.set("navstate", "winery");
            this.App.load_winery(winery_id);
        }

    });

    var app = new MainRouter;
    
    if( !Backbone.history.start() ){
        app.navigate("home", {trigger:true});
    }

});
