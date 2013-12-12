
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
 listeners:{
    "load":function() {
      
    }
  }
});




