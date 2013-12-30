Ext.define('WineCellar.store.WineInventory', {
  extend:"Ext.data.Store",
  storeId:"WineTruth",
  require:["WineCellar.model.Wine"],
  model:"WineCellar.model.WineBottle",
  autoLoad:true,
  proxy: {
      type: 'ajax',
      url:"app/store/WineInventorySampleData.JSON",
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




