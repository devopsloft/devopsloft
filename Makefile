UNAME := $(shell uname)

ifdef CI
	ENVIRONMENT = ci
else
	ENVIRONMENT = dev
endif

include .env.${ENVIRONMENT}
export

/usr/local/bin/chromedriver:
    ifeq ($(OS), "Darwin")
		brew install chromedriver
    endif

functional-tests: /usr/local/bin/chromedriver
	./build/build.sh $$ENVIRONMENT
	docker run --rm -v /var/run/docker.sock:/var/run/docker.sock $$NAMESPACE/spinner:latest ./spin-docker.py --environment $$ENVIRONMENT
	pytest -v -n=2 tests/functional
	docker run --rm -v /var/run/docker.sock:/var/run/docker.sock $$NAMESPACE/spinner:latest ./spin-docker.py --environment $$ENVIRONMENT --action destroy
