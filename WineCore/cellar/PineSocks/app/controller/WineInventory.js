Ext.define('WineCellar.controller.WineInventory', {
	extend: 'Ext.app.Controller',
	requires:[
		'Ext.JSON'
	],
	views:["Inventory","WineBottleEdit"],
	models:["WineBottle"],
	stores:["WineInventory"],
	init: function () {
		this.control({
			'#WineryCombo':{
				'select':function(combo,record) {
					var locationCombo = Ext.getCmp("LocationCombo");
					locationCombo.setValue(record[0].get("location"));
				}
			},
			'#WineCombo':{
				'beforequery':function(queryPlan) {
					var wineryCombo = Ext.getCmp("WineryCombo");
					var record = wineryCombo.findRecordByValue(wineryCombo.getValue());
					if(!Ext.isEmpty(record)) {
						var id = record.get("id");
						queryPlan.combo.getStore().getProxy().winery_id = id;
					}
				},
				'select':function(combo,record) {
					Ext.getCmp("WineTypeCombo").setValue(record[0].get("winetype"));
					Ext.getCmp("VarietalCombo").setValue(record[0].get("varietal"));
					Ext.getCmp("YearField").setValue(record[0].get("year"));
				}
			},
			'WineBottleEdit button[action=add]':{
				'click':function(button) {
					var form = button.up('form').getForm();
					//if (form.isValid()) {
						var values = form.getFieldValues();

						var wineBottle = Ext.create('WineCellar.model.WineBottle', {
							yearBought:values.bought.getFullYear(),
							drinkBefore:values.bought.getFullYear()+values.drinkBefore
						});

						var wine = Ext.getStore("Wines").findRecord("id",values.wine);
						wineBottle.setWine(wine);

						wineBottle.save();

						Ext.defer(function() {
							Ext.getStore("WineInventory").reload();
						}, 1000);
					//}

				}
			}
		});
		this.application.on({	
		
		});
		Ext.Ajax.request({
			url:"/truth/cellar",
			success: function(response) {
				this.cellar = Ext.JSON.decode(response.responseText);
				Ext.getStore("WineInventory").load();
			}
		});
	}
});
