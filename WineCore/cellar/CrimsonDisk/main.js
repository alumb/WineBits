
var DEV_LOCATION = "http://localhost:8081";
var PROD_LOCATION = "https://winebits.appspot.com";

var SERVER_LOCATION = DEV_LOCATION;
var TRUTH_LOCATION = SERVER_LOCATION + "/truth";

$(function(){

    var SearchModel = Backbone.Model.extend({});

    var SearchWineResult = Backbone.Model.extend({});

    var SearchWineryResult = Backbone.Model.extend({});

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
            alert("Wine Description! [Add this wine to my collection]");
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
            alert("Winery Description!");
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
            //this.last_results = this.last_results + 1;
            //var this_results = this.last_results;
            $.getJSON( url, function(data){
            //    if( ! that.last_results == this_results ){
            //        return;
            //    }
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
        el: $("#wineapp"),
        initialize: function(){
            this.render();
            searchmodel = new SearchModel;
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

    var App = new SearchView;
});
