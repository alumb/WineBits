Ext.define('WineCellar.store.WineInventory', {
	extend:"Ext.data.Store",
	storeId:"WineInventory",
	require:[
		"WineCellar.model.Wine",
		'WineCellar.model.Winery'
	],
	model:"WineCellar.model.WineBottle",
	autoLoad:true
});




