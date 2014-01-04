Ext.define('WineCellar.view.AssociationColumn', {
	extend: 'Ext.grid.column.Column',
	alias: ['widget.associationcolumn'],
	alternateClassName: 'Ext.grid.AssociationColumn',

	defaultRenderer: function(val, meta, record){
		try{
			var column = meta.column;
			var split = column.dataIndex.split(".");
			var fnName;
			var i, len;
			for(i = 0, len = split.length - 1; i < len; i++) {
				fnName = "get" + split[i];
				record = record[fnName]();
			}
			if(!Ext.isEmpty(record)) {
				val = record.get(split[i])
				return val;
			}
		}
		catch(ex) {}
		return "Association Not Found";
	}
});
