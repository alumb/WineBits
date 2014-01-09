Ext.define('WineCellar.model.Winery', {
	extend: 'Ext.data.Model',
	fields: [
		{name:'name', type:'string'},
		{name:'location', type:'string'},
		{name:'verified', type:'string'},
		{name:'id', type:'string'},
		{name:'url', type:'string'},
		{name:'key', type:'string'}
	],
	proxy: {
		type: 'ajax',
		url:"../truth/search",
		noCache:false,
		reader: {
			type: 'json',
			root: 'wineries'
		}
	}
});
