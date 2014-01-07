Ext.define('WineCellar.store.WineTypes', {
	extend:"Ext.data.Store",
	storeId:"WineTypes",
	require:["WineCellar.model.WineType"],
	model:"WineCellar.model.WineType",
	autoLoad:true
});
