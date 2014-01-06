Ext.define('WineCellar.store.Wines', {
	extend:"Ext.data.Store",
	storeId:"Wines",
	require:["WineCellar.model.Wine"],
	model:"WineCellar.model.Wine",
	autoLoad:false,
	proxy: {
		type: 'ajax',
		reader: {
			type: 'json',
			root: '/'
		}
	}
});
