Ext.define('WineCellar.model.WineCellar', {
	extend: 'Ext.data.Model',
	fields: [
		{name:'name', type:'string'},
		{name:'id', type:'string'}
	],
	proxy: {
		type: 'rest',
		url:"../truth/cellar",
		noCache:false,
		reader: {
			type: 'json',
			root: 'wineries'
		}
	}
});
