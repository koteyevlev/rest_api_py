all:
	@bash start_server.sh


ap_get:
	@sh apache_test/get_1000.sh > log.txt


ap_stat:
	@sh apache_test/stat_1000.sh > log.txt


ap_birth:
	@sh apache_test/birth_1000.sh > log.txt

ap_post:
	@sh apache_test/post_1000.sh > log.txt
