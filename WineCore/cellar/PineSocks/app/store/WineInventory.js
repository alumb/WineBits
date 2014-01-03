Ext.define('WineCellar.store.WineInventory', {
  extend:"Ext.data.Store",
  storeId:"WineTruth",
  require:[
    "WineCellar.model.Wine",
    'WineCellar.model.Winery'
  ],
  model:"WineCellar.model.WineBottle",
  autoLoad:true,
  proxy: {
      type: 'ajax',
      url:"server/inventory/",
      reader: {
          type: 'json',
          root: 'wineBottles'
      }
  },
 listeners:{
    "load":function() {
      //debugger;
    }
  }
});




