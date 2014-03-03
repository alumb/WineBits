Ext.define('WineCellar.model.WineType', {
	extend: 'Ext.data.Model',
	fields: [
		{name:'winetype', type:'string'}
	],
	proxy: {
		type: 'rest',
		url:"../truth/winetype",
		noCache:false,
		reader: {
			type: 'json',
			root: '/'
		}
	}
});
