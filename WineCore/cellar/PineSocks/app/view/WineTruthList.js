Ext.define("WineCellar.view.WineTruthList", {
    extend: 'Ext.grid.Panel',
    xtype:'WineTruthList',
    requires:[
        "Ext.grid.column.Action",
        "Ext.form.field.Number",
        "Ext.grid.plugin.RowEditing"
    ],
    store:"WineTruth",
    columns: [
        {text:"Winery", dataIndex:'winery', flex:1, editor: 'textfield'},
        {text:"Name", dataIndex:'name', flex:1, editor: 'textfield'},
        {text:"Varietal", dataIndex:'varietal', flex:1, editor: 'textfield'},
        {text:"Wine Type", dataIndex:'winetype', editor: 'textfield'},
        {text:"Year", dataIndex:'year', editor: {
                xtype:'numberfield',
                minValue:1700,
                maxValue:2013,
                hideTrigger:false
            }
        },
        {text:"UPC", dataIndex:'upc',width:150, editor: 'numberfield'},
        {text:"Verified", dataIndex:'verified', editor:'checkboxfield'},
        {xtype:"actioncolumn",width:30, items:[{
            icon:"ext/examples/restful/images/delete.png",
            tooltip:"Delete",
            handler:function(grid,rowIndex,colIndex) {
                grid.getStore().removeAt(rowIndex);
            }
        }]}
    ],
    tbar: [{
        text: 'Add Wine',
        handler: function() { this.up("WineTruthList").onAddClick(); }
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
        var rec = Ext.create("WineCellar.model.Wine",{
            "winery":"new"
        });
        
        this.getStore().insert(0, rec);
        this.getPlugin("rowEditing").startEdit(rec,0);
    },
});
