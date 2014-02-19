
build: bundle.zip
	echo -n "Adobe eMail: " ;\
	read username ;\
	touch log.txt ;\
	curl -u $$username \
		--progress-bar \
		-X PUT \
		-F file=@bundle.zip \
		https://build.phonegap.com/api/v1/apps/757475 \
		| tee -a "log.txt" ; test ${PIPESTATUS[0]} 

bundle.zip: $(shell find www)
	echo "bundling!"
	zip -r bundle.zip www

