Ext.define('WineCellar.model.Varietal', {
	extend: 'Ext.data.Model',
	requires:['WineCellar.store.reader.String'],
	fields: [
		{name:'varietal', type:'string'}
	],
	proxy: {
		type: 'rest',
		url:"../truth/varietal",
		noCache:false,
		reader: {
			type: 'string',
			root: '/'
		}
	}
});
