Ext.define('WineCellar.model.Wine', {
    extend: 'Ext.data.Model',
    fields: [
        {name:'winery', type:'string'},
        {name:'name', type:'string'},
        {name:'varietal', type:'string'},
        {name:'winetype', type:'string'},
        {name:'year', type:'int'},
        {name:'upc', type:'string'},
        {name:'verified', type:'boolean'}
    ]
});

