all:
	@bash start_server.sh


ap_get:
	@sh apache_test/get_1000.sh


ap_stat:
	@sh apache_test/stat_1000.sh


ap_birth:
	@sh apache_test/birth_1000.sh
