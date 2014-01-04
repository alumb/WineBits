Ext.define("WineCellar.view.WineBottleEdit", {
	extend: 'Ext.form.Panel',
	xtype:'WineBottleEdit',
	requires:[
		'Ext.form.FieldSet',
		'Ext.form.field.Date'
	],
	layout:'anchor',
	bodyPadding:7,
	defaults:{
		labelAlign:'right',
		xtype:'textfield',
		width:400
	},
	items:[
		{fieldLabel:'Winery', name:'winery'},
		{
			xtype:'fieldset',
			title:"Wine",
			width:"100%",
			margin:"0 0 10 0",
			defaults:{
				labelAlign:'right',
				xtype:'textfield',
				width:400
			},
			layout:{
				type:'hbox',
				align:'stretchmax'
			},
			items:[
				{fieldLabel:'Wine', name:'winery'},
				{fieldLabel:'Varietal', name:'winery'},
				{fieldLabel:'Wine Type', name:'winery'},
				{fieldLabel:'Year', name:'winery'},
			]
		},
		{fieldLabel:'Bought', xtype:"datefield", name:'winery'},
		{fieldLabel:'drink before', name:'winery'},
	],
	buttons: [{
		text: 'Reset',
		handler: function() {
			this.up('form').getForm().reset();
		}
	}, {
		text: 'Add',
		formBind: true, //only enabled once the form is valid
		disabled: true,
		handler: function() {
			var form = this.up('form').getForm();
			if (form.isValid()) {
				form.submit({
					success: function(form, action) {
						 Ext.Msg.alert('Success', action.result.msg);
					},
					failure: function(form, action) {
						Ext.Msg.alert('Failed', action.result.msg);
					}
				});
			}
		}
	}]
});
