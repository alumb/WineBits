Ext.define('WineCellar.store.Wines', {
	extend:"Ext.data.Store",
	storeId:"Wines",
	require:["WineCellar.model.Wine"],
	model:"WineCellar.model.Wine",
	autoLoad:false,
	proxy: {
		type: 'ajax',
		url:"../truth/winery/4782875580825600/wine",
		reader: {
			type: 'json',
			root: '/'
		}
	}
});
