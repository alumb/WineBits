Ext.define('WineCellar.controller.WineTruth', {
	extend: 'Ext.app.Controller',
	views:["WineTruthList"],
	models:["Wine"],
	stores:["Wines","Wineries"]
});
