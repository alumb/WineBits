Ext.define('WineCellar.store.Wineries', {
	extend:"Ext.data.Store",
	storeId:"Wineries",
	require:["WineCellar.model.Winery"],
	model:"WineCellar.model.Winery",
	autoLoad:true
});




