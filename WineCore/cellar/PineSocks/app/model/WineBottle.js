Ext.define('WineCellar.model.WineBottle', {
	extend: 'Ext.data.Model',
	requires:[
		'WineCellar.store.writer.Rest'
	],
	fields: [
		{name:'yearBought', type:'int'},
		{name:'drinkBefor', type:'int'},
		{name:'drunkOn', type:'date'}

	],
	associations:[{
		type:"hasOne",
		associationKey:"Wine", //this is the name in json
		model:"WineCellar.model.Wine",
		name:"wine",
		getterName:"getWine",
		setterName:"setWine"
	},{
		type:"hasOne",
		associationKey:"WineCellar", //this is the name in json
		model:"WineCellar.model.WineCellar",
		name:"WineCellar",
		getterName:"getWineCellar",
		setterName:"setWineCellar"
	}],
	proxy: {
		type: 'rest',
		url: "../truth/cellar/wine",
		noCache:false,
		extraParams:{extended_listing:"true"},
		reader: {
			type: 'json',
			root: 'wineBottles'
		},
		writer: {
			type: 'rest',
			getRecordData: function(record, operation) {
				var data = Ext.data.writer.Json.prototype.getRecordData.apply(this,[record, operation]);
				data.wine_id = record.getWine().get("id");
				data.winery_id = record.getWine().getWinery().get("id");
				return data;
			}
		}
	}
});

