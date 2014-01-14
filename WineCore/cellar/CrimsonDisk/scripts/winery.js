define(["constants", "search"], function(constants, search){
    
    var WineryDetailModel = Backbone.Model.extend({});

    var WineryView = Backbone.View.extend({
        template: Handlebars.compile($("#template-winery-detail").html()),
        el: $("#mainwindow"),
        initialize: function(obj){
            this.router = obj.router;
        },
        load_winery: function(winery){
            var winery_url = constants.TRUTH_LOCATION + "/winery/" + winery;
            var winelist_url = constants.TRUTH_LOCATION + "/winery/" + winery + "/wine";
            var that = this;
            this.winelist_views = [];
            $.getJSON( winery_url, function(data){
                that.model = new WineryDetailModel(data);
                that.render();
            });
            $.getJSON( winelist_url, function(data){
                _.each(data, function(wine){
                    var m = new search.SearchWineResult(wine);
                    var swv = new search.SearchWineView({model:m, router:that.router});
                    that.winelist_views.push(swv);
                });
                that.render();
            });

        },
        render: function(){
            obj = this.model.toJSON();
            this.$el.html(this.template(obj));
            this.$("#winelist").html("");
            var that = this;
            _.each(this.winelist_views, function(wineview){
                wineview.render();
                that.$("#winelist").append(wineview.$el);
            });
        }
    });

    return {
        WineryDetailModel: WineryDetailModel,
        WineryView: WineryView
    }

});
