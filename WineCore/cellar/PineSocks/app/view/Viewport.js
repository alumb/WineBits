Ext.define('WineCellar.view.Viewport', {
	extend: 'Ext.container.Viewport',
	requires:[
		'Ext.layout.container.Fit',
		'WineCellar.view.Main'
	],

	layout: {
		type: 'fit'
	},

	items: [{
		xtype: 'app-main'
	}]
});
