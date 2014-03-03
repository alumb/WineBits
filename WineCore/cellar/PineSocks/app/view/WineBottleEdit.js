Ext.define("WineCellar.view.WineBottleEdit", {
	extend: 'Ext.form.Panel',
	xtype:'WineBottleEdit',
	requires:[
		'Ext.form.FieldSet',
		'Ext.form.field.Date',
		'Ext.form.field.ComboBox'
	],
	layout:'anchor',
	bodyPadding:7,
	items:[{
		anchor:"100%",
		xtype:'fieldset',
		title:"Winery",
		padding:"0 10 10 0",
		defaults:{
			labelAlign:'right'
		},
		layout:{
			type:'hbox',
			align:'stretchmax'
		},
		items:[{
			id:"WineryCombo",
			xtype: 'combo',
			name:"winery",
			store: "Wineries",
			displayField: 'name',
			valueField:"id",
			fieldLabel:"Winery",
			typeAhead: false,
			flex:1,
			queryParam:'q',
			minChars:2,
			listConfig: {
				loadingText: 'Searching...',
				emptyText: 'No matching wineries found.'
			}
		},{
			id:"LocationCombo",
			xtype: 'combo',
			store: "Locations",
			displayField: 'location',
			fieldLabel:"Location",
			typeAhead: false,
			flex:1,
			queryMode:'local',
			listConfig: {
				loadingText: 'Searching...',
				emptyText: 'No matching wineries found.'
			}
		}]
	},{
		anchor:"100%",
		xtype:'fieldset',
		title:"Wine",
		padding:"0 10 10 0",
		defaults:{
			labelAlign:'right',
			xtype:'textfield',
			width:400
		},
		layout:{
			type:'hbox',
			align:'stretchmax'
		},
		items:[{
			id:"WineCombo",
			xtype: 'combo',
			store: "Wines",
			displayField: 'name',
			valueField:"id",
			name:"wine",
			fieldLabel:"Wines",
			typeAhead: false,
			minChars:2,
			triggerAction:'last',
			flex:1,
			listConfig: {
				loadingText: 'Searching...',
				emptyText: 'No matching wines found.'
			}
		},
		{	
			id:"WineTypeCombo",
			xtype: 'combo',
			store: "WineTypes",
			displayField: 'winetype',
			fieldLabel:"Wine Types",
			typeAhead: false,
			queryMode:'local',
			flex:1,
			listConfig: {
				loadingText: 'Searching...',
				emptyText: 'No matching wine typess found.'
			}
		},
		{	
			id:"VarietalCombo",
			xtype: 'combo',
			store: "Varietals",
			displayField: 'varietal',
			fieldLabel:"Varietals",
			typeAhead: false,
			queryMode:'local',
			flex:1,
			listConfig: {
				loadingText: 'Searching...',
				emptyText: 'No matching varietals found.'
			}
		},
		{
				id:"YearField",
				fieldLabel:'Year', 
				name:'year',
				xtype:"numberfield",
				width:200,
				minValue:1800,
				maxValue:(new Date()).getFullYear(),
				value:(new Date()).getFullYear()-1
		}]
	},
	{fieldLabel:'Bought', xtype:"datefield", name:'bought',value: new Date()},
	{
			fieldLabel:'Good for (years)', 
			name:'drinkBefore',
			xtype:"numberfield",
			minValue:0,
			maxValue:50,
			size:4,
			value:2
	}],
	buttons: [{
		text: 'Reset',
		handler: function() {
			this.up('form').getForm().reset();
		}
	}, {
		text: 'Add',
		action:'add',
		formBind: true, //only enabled once the form is valid
		disabled: true
	}]
});
