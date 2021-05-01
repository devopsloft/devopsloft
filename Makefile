.PHONY: dependencies un functional

UNAME := $(shell uname)

ifdef CI
	ENVIRONMENT = ci
else
	ENVIRONMENT = dev
endif

include .env.${ENVIRONMENT}
export

/usr/local/bin/chromedriver:
    ifeq ($(UNAME), "Darwin")
		brew install chromedriver
    endif

dependencies:
	pip3 install -r tests/requirements.txt

functional: dependencies /usr/local/bin/chromedriver up 
	pytest -v -n=2 tests/functional
	docker run --rm -v /var/run/docker.sock:/var/run/docker.sock $$NAMESPACE/spinner:latest ./spin-docker.py --environment $$ENVIRONMENT --action destroy

up:
	./build/build.sh $$ENVIRONMENT
	docker build --build-arg ENVIRONMENT=$$ENVIRONMENT -t ${NAMESPACE}/spinner \
		-f devopsloft/spinner/Dockerfile .
	docker run --rm -v ${HOME}/.aws:/root/.aws -v /var/run/docker.sock:/var/run/docker.sock \
		${NAMESPACE}/spinner:latest
