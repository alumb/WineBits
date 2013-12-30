Ext.define("WineCellar.view.Inventory", {
    extend: 'Ext.grid.Panel',
    xtype:'Inventory',
    requires:[
        "Ext.grid.column.Action",
        "Ext.form.field.Number",
        "Ext.grid.plugin.RowEditing",
        'WineCellar.view.AssociationColumn'
    ],
    store:"WineInventory",
    columns: [
        {xtype:"associationcolumn", text:"Winery", dataIndex:'Wine.winery', flex:1, editor: 'textfield'},
        {xtype:"associationcolumn", text:"Name", dataIndex:'Wine.name', flex:1, editor: 'textfield'},
        {xtype:"associationcolumn", text:"Varietal", dataIndex:'Wine.varietal', flex:1, editor: 'textfield'},
        {xtype:"associationcolumn", text:"Wine Type", dataIndex:'Wine.winetype', editor: 'textfield'},
        {xtype:"associationcolumn", text:"Year", dataIndex:'Wine.year', editor: {
                xtype:'numberfield',
                minValue:1700,
                maxValue:2013,
                hideTrigger:false
            }
        },
        {text:"Year Bought", dataIndex:'yearBought', editor: {
                xtype:'numberfield',
                minValue:1700,
                maxValue:2013,
                hideTrigger:false
            }
        },
        {text:"Drink Before", dataIndex:'drinkBefor', editor: {
                xtype:'numberfield',
                minValue:1700,
                maxValue:2013,
                hideTrigger:false
            }
        },
        {text:"Drink On", dataIndex:'drunkOn', editor: {
                xtype:'datefield'                
            }
        },
        {xtype:"actioncolumn",width:30, items:[{
            icon:"ext/examples/restful/images/edit.png",
            tooltip:"Edit",
            handler:function(grid,rowIndex,colIndex) {
                debugger;
            }
        }]}
    ],
    tbar: [{
        text: 'Add Wine Bottle',
        handler: function() { this.up("WineInventory").onAddClick(); }
    }],
    plugins: [
        {   
            ptype:"rowediting",
            pluginId:"rowEditing",
            clicksToEdit: 2
        }
    ],
    onAddClick: function(){
        // Create a model instance
        var rec = Ext.create("WineCellar.model.WineBottle",{
            "winery":"new"
        });
        
        this.getStore().insert(0, rec);
        this.getPlugin("rowEditing").startEdit(rec,0);
    },
});
