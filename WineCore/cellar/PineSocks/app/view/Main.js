Ext.define('WineCellar.view.Main', {
	extend: 'Ext.tab.Panel',
	xtype:"app-main",
	requires:[
		'Ext.tab.Panel',
		'Ext.layout.container.Border',
		'WineCellar.view.WineTruthList',
		'WineCellar.view.Inventory'
	],
	
	layout:"fit",
	activeTab:1,
	items:[{
		xtype:'WineTruthList',
		title: 'Wine Truth List'
	},{
		xtype:'Inventory',
		title: 'Inventory'
	}]
});
