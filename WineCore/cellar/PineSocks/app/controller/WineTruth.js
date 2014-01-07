Ext.define('WineCellar.controller.WineTruth', {
	extend: 'Ext.app.Controller',
	views:["WineTruthList"],
	models:["Wine","Winery","Varietal","WineType"],
	stores:["Wines","Wineries","Locations","Varietals","WineTypes"]
});
