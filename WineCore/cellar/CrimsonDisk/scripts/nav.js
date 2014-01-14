define([], function(){
    
    var NavModel = Backbone.Model.extend({});

    var NavView = Backbone.View.extend({
        template: Handlebars.compile($("#template-nav").html()),
        el: $("#nav"),
        initialize: function(obj){
            this.model = new NavModel;
            this.router = obj.router;
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
            this.router.navigate("home", {trigger:true});
        },
        cellar: function(){
        }
    });

    return {
        NavModel: NavModel, 
        NavView: NavView
    };

});
