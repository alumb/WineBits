Ext.define('WineCellar.model.Wine', {
	extend: 'Ext.data.Model',
	requires:['WineCellar.model.Winery'],
	fields: [
		{name:'name', type:'string'},
		{name:'varietal', type:'string'},
		{name:'winetype', type:'string'},
		{name:'year', type:'int'},
		{name:'upc', type:'string'},
		{name:'verified', type:'boolean'},
		{name:'winery_id', type:'int'}
	],
	associations:[{
		type:"hasOne",
		associationKey:"winery", //this is the name in json
		model:"WineCellar.model.Winery",
		name:"winery",
		getterName:"getWinery",
		setterName:"setWinery"

	}],
	proxy: {
		type: 'ajax',
		url:"../truth/search",
		noCache:false,
		reader: {
			type: 'json',
			root: 'wines'
		}
	}
});

