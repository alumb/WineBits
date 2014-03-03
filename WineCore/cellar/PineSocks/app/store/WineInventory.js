Ext.define('WineCellar.store.WineInventory', {
	extend:"Ext.data.Store",
	storeId:"WineInventory",
	requires:[
		"WineCellar.model.Wine",
		'WineCellar.model.Winery',
		'WineCellar.model.WineCellar'
	],
	model:"WineCellar.model.WineBottle"
});




