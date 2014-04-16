Ext.define('WineCellar.model.Location', {
	extend: 'Ext.data.Model',
	requires:['WineCellar.store.reader.String'],
	fields: [
		{name:'location', type:'string'}
	],
	proxy: {
		type: 'rest',
		url:"../truth/location",
		reader: {
			type: 'string',
			root: '/'
		}
	}
});
