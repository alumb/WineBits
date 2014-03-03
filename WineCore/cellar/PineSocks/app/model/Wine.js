Ext.define('WineCellar.model.Wine', {
	extend: 'Ext.data.Model',
	requires:['WineCellar.model.Winery'],
	fields: [
		{name:'name', type:'string'},
		{name:'varietal', type:'string'},
		{name:'winetype', type:'string'},
		{name:'year', type:'int'},
		{name:'upc', type:'string'},
		{name:'verified', type:'boolean'}
	],
	associations:[{
		type:"hasOne",
		associationKey:"Winery", //this is the name in json
		model:"WineCellar.model.Winery",
		name:"winery",
		getterName:"getWinery",
		setterName:"setWinery"
	}],
	proxy: {
		type: 'rest',
		getUrl: function(request) {
			if(!Ext.isEmpty(request.url)) { return request.url; }
			return "../truth/winery/" + this.winery_id + "/wine";
		},		
		noCache:false,
		extraParams:{extended_listing:"true"},
		reader: {
			type: 'json',
			root: 'wines'
		}
	}
});

