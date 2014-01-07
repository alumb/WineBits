Ext.define('WineCellar.controller.WineInventory', {
	extend: 'Ext.app.Controller',
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
						queryPlan.query += " winery_id:" + id
					}
				},
				'select':function(combo,record) {
					Ext.getCmp("WineTypeCombo").setValue(record[0].get("winetype"));
					Ext.getCmp("VarietalCombo").setValue(record[0].get("varietal"));
					Ext.getCmp("YearField").setValue(record[0].get("year"));
				},
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

						Ext.getStore("WineInventory").add(wineBottle);
						Ext.getStore("WineInventory").sync();
					//}

				}
			}
		});
		this.application.on({	
		
		});
	}
});
