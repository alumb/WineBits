
var DEV_LOCATION = "http://localhost:8081";
var PROD_LOCATION = "https://winebits.appspot.com";

var SERVER_LOCATION = DEV_LOCATION;
var TRUTH_LOCATION = SERVER_LOCATION + "/truth";

$(function(){

    var SearchModel = Backbone.Model.extend({});

    var SearchWineResult = Backbone.Model.extend({});

    var SearchWineryResult = Backbone.Model.extend({});

    var WineDetailModel = Backbone.Model.extend({});
    
    var WineryDetailModel = Backbone.Model.extend({});

    var SearchBarView = Backbone.View.extend({
        template: Handlebars.compile($("#template-search").html()),
        render: function(){
            this.$el.html(this.template({}));
            return this;
        },
        events: {
            "keyup #search":    "change",
            "paste #search":    "change"
        },
        change: function(){
            this.model.set("searchterm", this.$("#search").val() );
        }
    });

    var SearchWineView = Backbone.View.extend({
        tagName: "a",
        className: "wine list-group-item",
        template: Handlebars.compile($("#template-wine").html()),
        render: function(){
            this.$el.html(this.template(this.model.toJSON()));
        },
        events: {
            "click": "clicked"
        },
        clicked: function(){
            app.navigate(this.model.get('url'), {trigger:true})
        }
    });

    var SearchWineryView = Backbone.View.extend({
        tagName: "a",
        className: "winery list-group-item",
        template: Handlebars.compile($("#template-winery").html()),
        render: function(){
            this.$el.html(this.template(this.model.toJSON()));
        },
        events: {
            "click": "clicked"
        },
        clicked: function(){
            app.navigate(this.model.get('url'), {trigger:true})
        }
    });

    var SearchResultsView = Backbone.View.extend({
        winery_views: [], 
        wine_views: [],
        last_results: 1,
        initialize: function(){
            this.listenTo(this.model, 'change', this.results);
        },
        results: function(){
            var searchterm = this.model.get("searchterm");
            var url = TRUTH_LOCATION + "/search?q=" + searchterm;
            var that = this;
            this.last_results = this.last_results + 1;
            var this_results = this.last_results;
            $.getJSON( url, function(data){
                if( ! that.last_results == this_results ){
                    return;
                }
                that.wine_views = [];
                that.winery_views = [];
                _.each(data['wines'], function(wine){
                    var wine_model = new SearchWineResult(wine);
                    var wine_view = new SearchWineView({
                        model: wine_model
                    });
                    that.wine_views.push(wine_view);
                });
                _.each(data['wineries'], function(winery){
                    var winery_model = new SearchWineryResult(winery);
                    var winery_view = new SearchWineryView({
                        model: winery_model
                    });
                    that.winery_views.push(winery_view);
                });
                that.wines = data['wines'];
                that.wineries = data['wineries'];
                that.render();
            });
        },
        render: function(){
            this.$el.html("");
            var that = this;
            _.each(this.winery_views, function(wineryview){
                wineryview.render();
                that.$el.append(wineryview.$el);
            });
            _.each(this.wine_views, function(wineview){
                wineview.render();
                that.$el.append(wineview.$el);
            });
        }
    });

    var SearchView = Backbone.View.extend({
        template: Handlebars.compile($("#template-main").html()),
        el: $("#mainwindow"),
        initialize: function(){
            this.render();
            this.searchmodel = new SearchModel;
            var searchmodel = this.searchmodel;
            var sbv = new SearchBarView({ model: searchmodel });
            sbv.setElement(this.$("#searchbar"));
            sbv.render();
            var results = new SearchResultsView({ model: searchmodel });
            results.setElement(this.$("#searchresults"));
            results.render();
        },
        render: function(){
            this.$el.html(this.template({}));
            return this;
        }
    });

    var NavModel = Backbone.Model.extend({});

    var NavView = Backbone.View.extend({
        template: Handlebars.compile($("#template-nav").html()),
        el: $("#nav"),
        initialize: function(){
            this.model = new NavModel;
            this.render();
            this.listenTo(this.model, 'change', this.render);
        },
        render: function(){
            obj = this.model.toJSON();
            obj['search'] = (obj['navstate'] === 'search');
            obj['cellar'] = (obj['navstate'] === 'cellar');
            this.$el.html(this.template(obj));
            return this;
        },
        events: {
            "click .search": "search", 
            "click .cellar": "cellar"
        },
        search: function(){
            app.navigate("home", {trigger:true});
        },
        cellar: function(){
        }
    });

    var WineryView = Backbone.View.extend({
        template: Handlebars.compile($("#template-winery-detail").html()),
        el: $("#mainwindow"),
        load_winery: function(winery){
            var winery_url = TRUTH_LOCATION + "/winery/" + winery;
            var winelist_url = TRUTH_LOCATION + "/winery/" + winery + "/wine";
            var that = this;
            $.getJSON( winery_url, function(data){
                that.model = new WineryDetailModel(data);
                that.render();
            });
            $.getJSON( winelist_url, function(data){
                //winelist
            });

        },
        render: function(){
            obj = this.model.toJSON();
            this.$el.html(this.template(obj));
        }
    });

    var WineView = Backbone.View.extend({
        template: Handlebars.compile($("#template-wine-detail").html()), 
        el: $("#mainwindow"),
        load_wine: function(winery, wine){
            var winery_url = TRUTH_LOCATION + "/winery/" + winery
            var wine_url = TRUTH_LOCATION + "/winery/" + winery + "/wine/" + wine;
            var that = this;
            $.getJSON( winery_url, function(data){
                that.winery_model = new WineryDetailModel(data);
                that.render();
            });
            $.getJSON( wine_url, function(data){
                that.model = new WineDetailModel(data);
                that.render();
            });
        },
        render: function(){
            obj = this.model.toJSON();
            obj['winery'] = this.winery_model.get('name');
            this.$el.html(this.template(obj));
        }
    });

    var MainRouter = Backbone.Router.extend({
        routes: {
            "home":                         "home",
            "search/:query":                "search",
            "winery/:winery":               "winery",
            "winery/:winery/wine/:wine":    "wine"
        },
        initialize: function(){
            this.Nav = new NavView;
        },
        home: function(){
            this.App = new SearchView;
            this.Nav.model.set("navstate", "search");
            this.listenTo(this.App.searchmodel, 'change', this.update_nav);
        },
        search: function(query){
            this.App = new SearchView;
            this.App.searchmodel.set("searchterm", query);
            this.Nav.model.set("navstate", "search");
            this.listenTo(this.App.searchmodel, 'change', this.update_nav);
        },
        update_nav: function(model){
            app.navigate("search/"+model.get('searchterm'))
        },
        wine: function(winery, wine){
            this.App = new WineView();
            this.Nav.model.set("navstate", "wine");
            this.App.load_wine(winery, wine);
        },
        winery: function(winery){
            this.App = new WineryView();
            this.Nav.model.set("navstate", "winery");
            this.App.load_winery(winery);
        }

    });

    var app = new MainRouter;
    
    if( !Backbone.history.start() ){
        app.navigate("home", {trigger:true});
    }

});
