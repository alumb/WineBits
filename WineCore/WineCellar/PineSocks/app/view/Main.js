Ext.define('WineCellar.view.Main', {
    extend: 'Ext.tab.Panel',
    xtype:"app-main",
    requires:[
        'Ext.tab.Panel',
        'Ext.layout.container.Border',
        'WineCellar.view.WineTruthList'
    ],
    
    layout:"fit",

    items:[{
        xtype:'WineTruthList',
        title: 'Wine Truth List'
    }]
});
