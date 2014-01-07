Ext.define('WineCellar.store.Locations', {
	extend:"Ext.data.Store",
	storeId:"Locations",
	require:["WineCellar.model.Location"],
	model:"WineCellar.model.Location",
	autoLoad:true
});
