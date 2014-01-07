Ext.define('WineCellar.model.Varietal', {
	extend: 'Ext.data.Model',
	fields: [
		{name:'varietal', type:'string'}
	],
	proxy: {
		type: 'ajax',
		url:"../truth/varietal",
		noCache:false,
		reader: {
			type: 'json',
			root: '/'
		}
	}
});
