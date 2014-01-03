Ext.define('WineCellar.model.Winery', {
    extend: 'Ext.data.Model',
    fields: [
        {name:'name', type:'string'},
        {name:'location', type:'string'},
        {name:'country', type:'string'},
        {name:'region', type:'string'},
        {name:'subregion', type:'string'}
    ]
});
