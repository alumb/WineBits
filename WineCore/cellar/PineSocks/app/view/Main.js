Ext.define('WineCellar.view.Main', {
	extend: 'Ext.panel.Panel',
	xtype:"app-main",
	requires:[
		'Ext.tab.Panel',
		'Ext.layout.container.Border',
		'WineCellar.view.WineTruthList',
		'WineCellar.view.Inventory',
		"Ext.toolbar.TextItem"
	],
	
	layout:"fit",

	dockedItems:[{
		xtype:"toolbar",
		cls:"TitleBar",
		dock:"top",
		items:[{
			xtype:'tbtext',
			cls:"title",
			text:"WineBits - Cellar Admin"
		},"->",{
			xtype:'tbtext',
			text:"Login"
		}]
	}],


	items:[{
		xtype:"tabpanel",

		activeTab:1,
		items:[{
			xtype:'WineTruthList',
			title: 'Wine Truth List'
		},{
			xtype:'Inventory',
			title: 'Inventory'
		}]
	}]
});
