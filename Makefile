all:
	@bash start_server.sh
	@echo "Server work"


ap_get:
	@sh apache_test/get_1000.sh > log.txt
	@echo "Check log.txt if you want to see output"

ap_stat:
	@sh apache_test/stat_1000.sh > log.txt
	@echo "Check log.txt if you want to see output"


ap_birth:
	@sh apache_test/birth_1000.sh > log.txt
	@echo "Check log.txt if you want to see output"

ap_post:
	@sh apache_test/post_1000.sh > log.txt
	@echo "Check log.txt if you want to see output"

ap_big_post:
	@ab -n 2 -c 1 -v 2 -p very_big_data.json -T 'application/json' http://0.0.0.0:8080/imports
