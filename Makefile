FILENAME=packer-ami.json

.PHONY: all build validate update

.DEFAULT_GOAL := default

default: help ;

all: build

build-ami: validate update
	@echo -e '>>>>>>>>>>>>>> Build AMI.'
	@packer build ${FILENAME}

validate:
	@echo -e '>>>>>>>>>>>>>> Validate JSON.'
	@packer validate ${FILENAME}

update:
	@echo -e '>>>>>>>>>>>>>> Fetching updates from git.'
	@git pull

test:
	@echo -e '>>>>>>>>>>>>>> Execute Molecule tests.'
	@./roles/vault/tox


help:
	@echo "-----------------------------------------------------------------------"
	@echo "                      Available commands                              -"
	@echo "-----------------------------------------------------------------------"
	@echo "   > build-ami - Build Packer image."
	@echo "   > update - Update from source."
	@echo "   > validate - Validate Packer json."
	@echo "-----------------------------------------------------------------------"