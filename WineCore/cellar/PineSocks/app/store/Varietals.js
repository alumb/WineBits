Ext.define('WineCellar.store.Varietals', {
	extend:"Ext.data.Store",
	storeId:"Varietals",
	require:["WineCellar.model.Varietal"],
	model:"WineCellar.model.Varietal",
	autoLoad:true
});
