Ext.define('WineCellar.model.WineBottle', {
	extend: 'Ext.data.Model',
	fields: [
		{name:'yearBought', type:'int'},
		{name:'drinkBefor', type:'int'},
		{name:'drunkOn', type:'date'}

	],
	associations:[{
		type:"hasOne",
		associationKey:"wine", //this is the name in json
		model:"WineCellar.model.Wine",
		name:"wine",
		getterName:"getWine",
		setterName:"setWine"
	}],
	proxy: {
		type: 'rest',
		url:"server/inventory/",
		noCache:false,
		reader: {
			type: 'json',
			root: 'wineBottles'
		},
		writer: {
			type: 'json',
			allowSingle:false,
			getRecordData: function(record, operation) {
				var data = Ext.data.writer.Json.prototype.getRecordData.apply(this,[record, operation]);
				data.wine_id = record.getWine().get("id");
				data.winery_id = record.getWine().get("winery_id");
				return data;
			}
		}
	}
});

