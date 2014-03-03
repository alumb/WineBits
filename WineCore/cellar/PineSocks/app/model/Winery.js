Ext.define('WineCellar.model.Winery', {
	extend: 'Ext.data.Model',
	fields: [
		{name:'name', type:'string'},
		{name:'location', type:'string'},
		{name:'verified', type:'string'},
		{name:'url', type:'string'},
		{name:'key', type:'string'}
	],
	proxy: {
		type: 'rest',
		url:"../truth/winery",
		noCache:false,
		extraParams:{extended_listing:"true"},
		reader: {
			type: 'json',
			root: 'wineries'
		}
	}
});
