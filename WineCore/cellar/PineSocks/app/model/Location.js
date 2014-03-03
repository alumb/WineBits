Ext.define('WineCellar.model.Location', {
	extend: 'Ext.data.Model',
	fields: [
		{name:'location', type:'string'}
	],
	proxy: {
		type: 'rest',
		url:"../truth/location",
		reader: {
			type: 'json',
			root: '/'
		}
	}
});
