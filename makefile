VENV_DIR = '.venv'
PROJECT_NAME := property_scraper

######################
# Help
######################
define HELP_MSG
	make installForLocalDev			make a virtualenv in the base directory (see createVirtualEnvironment) and install dependencies.
	make createVirtualEnvironment	create a virtual environment in '${VENV_DIR}'.
endef
PROJECT_HELP_MSG := $(PROJECT_HELP_MSG)$(NEWLINE)$(NEWLINE)$(HELP_MSG)

######################
# Install Helpers
######################
.PHONY: createVirtualEnvironment
createVirtualEnvironment:
	@test -d .venv || python3 -m venv --prompt $(PROJECT_NAME) ./$(VENV_DIR)
	@echo 'Environment created. Run "source ./$(VENV_DIR)/bin/activate" to activate the virtual environment.\n"deactivate" to exit it.'

.PHONY: install
install: createVirtualEnvironment requirements.txt
	@$(VENV_DIR)/bin/pip install --upgrade pip
	@$(VENV_DIR)/bin/pip install --upgrade --requirement requirements.txt

.PHONY: installForLocalDev
installForLocalDev: install
	@echo 'Local install complete'

######################
# MYSQL Helpers
######################
MYSQL_SRC_DIR=$(shell pwd)/sql
MYSQL_ROOT_PASSWORD := password
MYSQL_DATABASE:= property_scraper
DB_HOST=$(shell docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' property-scraper-mysql)
.PHONY: mysql
mysql:
	@docker run -it \
		--rm \
		mysql mysql -h$(DB_HOST) -uroot $(MYSQL_DATABASE) -p

.PHONY: dbip
dbip:
	@echo $(DB_HOST)

.PHONY: rundb
rundb:
	MYSQL_SRC_DIR=$(MYSQL_SRC_DIR) \
	MYSQL_ROOT_PASSWORD=$(MYSQL_ROOT_PASSWORD) \
	./.docker/run.sh
