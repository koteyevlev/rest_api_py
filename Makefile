all:
	@bash start_server.sh
	@echo "\nServer work\n"


ap_get:
	@sh apache_test/get_1000.sh > log.txt
	@echo "\nCheck log.txt if you want to see output\n"

ap_stat:
	@sh apache_test/stat_1000.sh > log.txt
	@echo "\nCheck log.txt if you want to see output\n"


ap_birth:
	@sh apache_test/birth_1000.sh > log.txt
	@echo "\nCheck log.txt if you want to see output\n"

ap_post:
	@sh apache_test/post_1000.sh > log.txt
	@echo "\nCheck log.txt if you want to see output\n"
