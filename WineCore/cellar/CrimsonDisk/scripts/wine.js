define(["constants"], function(constants){

    var special_fields = [
        "id",
        "year",
        "name",
        "type", 
        "varietal", 
        "upc",
        "verified",
        "verified_by", 
        "url", 
        "winetype"
    ];
    
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
            var winery_returned = false;
            var wine_returned = false;
            $.getJSON( winery_url, function(data){
                that.winery_model = new WineryDetailModel(data);
                winery_returned = true;
                if(winery_returned && wine_returned){
                    that.render();
                }
            });
            $.getJSON( wine_url, function(data){
                that.model = new WineDetailModel(data);
                wine_returned = true;
                if(winery_returned && wine_returned){
                    that.render();
                }
            });
        },
        render: function(){
            obj = this.model.toJSON();
            /* TODO: this is a debug line. */
            //obj = {};
            extra_keys = _.filter(Object.keys(obj), function(key){
                return !_.contains(special_fields, key); 
            });
            obj['extra_keys'] = []
            _.each( extra_keys, function(key){
                obj['extra_keys'].push( {'key':key, 'value':obj[key]} );
            });
            console.log(obj);

            if( obj['varietal'] === undefined ){
                obj['varietal_options'] = constants.varietals();
            }
            if( obj['winetype'] === undefined ){
                obj['winetype_options'] = constants.winetypes();
            }
            console.log(obj['varietal_options']);

            obj['winery'] = this.winery_model.get('name');

            this.$el.html(this.template(obj));
            $("#varietal").select2({
                placeholder: "Select a varietal",
            });
            $("#winetype").select2({
                placeholder: "Select a winetype",
            });
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
