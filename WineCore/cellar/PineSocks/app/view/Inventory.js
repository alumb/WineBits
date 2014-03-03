Ext.define("WineCellar.view.Inventory", {
	extend: 'Ext.panel.Panel',
	xtype:'Inventory',
	requires:[
		'WineCellar.view.InventoryList',
		'WineCellar.view.WineBottleEdit'
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
		title:"Inventory List",
		xtype:"InventoryList",
		flex:1,
		margin: '0 0 10 0'
	},{
		xtype:"WineBottleEdit",
		title:"Edit",
		collapsible:true
	}]
});
