Ext.define('WineCellar.store.writer.Rest', {
	extend: 'Ext.data.writer.Writer',
	alias: 'writer.rest',
	
	writeRecords: function(request, data) {
		request.params = data[0];
		return request;
	}
});
