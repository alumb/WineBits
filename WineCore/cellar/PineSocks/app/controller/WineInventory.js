Ext.define('WineCellar.controller.WineInventory', {
	extend: 'Ext.app.Controller',
	views:["Inventory"],
	models:["WineBottle"],
	stores:["WineInventory"]
});
