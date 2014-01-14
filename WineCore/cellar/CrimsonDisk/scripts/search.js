define(["constants"], function(constants){

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
        initialize: function(obj){
            this.router = obj.router;
        },
        render: function(){
            this.$el.html(this.template(this.model.toJSON()));
        },
        events: {
            "click": "clicked"
        },
        clicked: function(){
            this.router.navigate(this.model.get('url'), {trigger:true})
        }
    });

    var SearchWineryView = Backbone.View.extend({
        tagName: "a",
        className: "winery list-group-item",
        template: Handlebars.compile($("#template-winery").html()),
        initialize: function(obj){
            this.router = obj.router;
        },
        render: function(){
            this.$el.html(this.template(this.model.toJSON()));
        },
        events: {
            "click": "clicked"
        },
        clicked: function(){
            this.router.navigate(this.model.get('url'), {trigger:true})
        }
    });

    var SearchResultsView = Backbone.View.extend({
        winery_views: [], 
        wine_views: [],
        last_results: 1,
        initialize: function(obj){
            this.router = obj.router;
            this.listenTo(this.model, 'change', this.results);
        },
        results: function(){
            var searchterm = this.model.get("searchterm");
            var url = constants.TRUTH_LOCATION + "/search?q=" + searchterm;
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
                        model: wine_model,
                        router: that.router
                    });
                    that.wine_views.push(wine_view);
                });
                _.each(data['wineries'], function(winery){
                    var winery_model = new SearchWineryResult(winery);
                    var winery_view = new SearchWineryView({
                        model: winery_model,
                        router: that.router
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
        initialize: function(obj){
            this.render();
            this.searchmodel = new SearchModel;
            var searchmodel = this.searchmodel;
            var sbv = new SearchBarView({ model: searchmodel, router:obj.router });
            sbv.setElement(this.$("#searchbar"));
            sbv.render();
            var results = new SearchResultsView({ model: searchmodel, router:obj.router });
            results.setElement(this.$("#searchresults"));
            results.render();
        },
        render: function(){
            this.$el.html(this.template({}));
            return this;
        }
    });

    return {
        SearchModel: SearchModel,
        SearchWineResult: SearchWineResult,
        SearchWineryResult: SearchWineryResult,
        
        SearchBarView: SearchBarView,
        SearchWineView: SearchWineView, 
        SearchWineryView: SearchWineryView,
        SearchResultsView: SearchResultsView,
        SearchView: SearchView
    };

});
