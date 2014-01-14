define(["constants"], function(constants){
    
    var WineryDetailModel = Backbone.Model.extend({});
    var WineDetailModel = Backbone.Model.extend({});
    
    var WineView = Backbone.View.extend({
        template: Handlebars.compile($("#template-wine-detail").html()), 
        el: $("#mainwindow"),
        initialize: function(obj){
            this.router = obj.router;
            this.model = new WineDetailModel({});
        },
        load_wine: function(winery, wine){
            var winery_url = constants.TRUTH_LOCATION + "/winery/" + winery
            var wine_url = constants.TRUTH_LOCATION + "/winery/" + winery + "/wine/" + wine;
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
            if( this.winery_model !== undefined){
              obj['winery'] = this.winery_model.get('name');
            }
            this.$el.html(this.template(obj));
        },
        events: {
            'click .winery':    'winery_click'
        },
        winery_click: function(){
            this.router.navigate( "/winery/"+this.winery_model.get('id'), {trigger:true})
        }
    });

    return {
        WineDetailModel:  WineDetailModel, 
        WineView: WineView
    };

});
