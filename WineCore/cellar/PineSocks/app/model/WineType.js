Ext.define('WineCellar.model.WineType', {
	extend: 'Ext.data.Model',
	requires:['WineCellar.store.reader.String'],
	fields: [
		{name:'winetype', type:'string'}
	],
	proxy: {
		type: 'rest',
		url:"../truth/winetype",
		noCache:false,
		reader: {
			type: 'string',
			root: '/'
		}
	}
});
