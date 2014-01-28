
deploy:
	~/google_appengine/appcfg.py update .

run:
	~/google_appengine/dev_appserver.py . --host=0.0.0.0 --admin_host=0.0.0.0 --skip_sdk_update_check

runclean:
	~/google_appengine/dev_appserver.py . --host=0.0.0.0 --admin_host=0.0.0.0 --clear_datastore=yes
