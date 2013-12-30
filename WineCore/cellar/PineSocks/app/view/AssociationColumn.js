Ext.define('WineCellar.view.AssociationColumn', {
    extend: 'Ext.grid.column.Column',
    alias: ['widget.associationcolumn'],
    alternateClassName: 'Ext.grid.AssociationColumn',

    defaultRenderer: function(val, meta, record){
        var column = meta.column;
        var split = column.dataIndex.split(".");
        var fnName = "get" + split[0];
        var association = record[fnName]();
        if(!Ext.isEmpty(association)) {
            val = association.get(split[1])
            return val;
        }
        return "Association Not Found";
    }
});
