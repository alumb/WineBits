
Ext.define('WineCellar.store.WineTruth', {
  extend:"Ext.data.Store",
  storeId:"WineTruth",
  require:["WineCellar.model.Wine"],
  model:"WineCellar.model.Wine",
  autoLoad:true,
  proxy: {
      type: 'ajax',
      url:"app/store/WineTruthSampleData.JSON",
      reader: {
          type: 'json',
          root: 'wines'
      }
  },
  /*proxy: {
      type: 'rest',
      url:"../truth/search",
      reader: {
          type: 'json',
          root: 'wines'
      },
      noCache:true
  },*/
 listeners:{
    "load":function() {
      
    }
  }
});




