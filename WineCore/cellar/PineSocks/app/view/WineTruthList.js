Ext.define("WineCellar.view.WineTruthList", {
	extend: 'Ext.panel.Panel',
	xtype:'WineTruthList',
	requires:[
		"Ext.grid.Panel",
		"Ext.grid.column.Action",
		"Ext.form.field.Number"
	],
	layout:{
		type:'vbox',
		align:'stretch',
		pack:'start'
	},
	bodyPadding:5,
	defaults: {
		frame: true
	},
	items:[{
		xtype:"grid",
		title:"Wineries",
		flex:1,
		margin: '0 0 5 0',
		store:"Wineries",
		columns: [
			{text:"Name", dataIndex:'name', flex:1, editor: 'textfield'},
			{text:"location", dataIndex:'location', flex:1, editor: 'textfield'}
		],
		listeners:{
			'itemclick':function(grid, record, item, index, e, eOpts) {
				var id = record.get("id");
				var store = Ext.getStore("Wines");
				store.load({
					params:{
						q:"winery_id:" + id
					}
				})
			}
		}
	},{
		xtype:"grid",
		title:"Wines",
		flex:1,
		store:"Wines",
		columns: [
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
			{text:"Verified", dataIndex:'verified', editor:'checkboxfield'}
		]
		
	}]
});
