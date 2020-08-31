DOCKER_USER     := 
DOCKER_PASS     := 
REGISTRY   		:= tranlyvu/hoovada.com

REPO_NAME   	:= $$(/usr/bin/basename -s .git `git config --get remote.origin.url`)
GIT_COMMIT 		:= $$(git rev-parse --short HEAD)
GIT_BRANCH 		:= $$(git rev-parse --abbrev-ref HEAD)
TAG_TEST 		:= ${REPO_NAME}-${GIT_BRANCH}
IMG_TEST    	:= ${REGISTRY}:${TAG_TEST}

VERSION 		:= v1.0.0
IMG_PROD    	:= ${REGISTRY}:${VERSION}


build-test:
	@docker build  -t ${IMG_TEST} -f ./docker/app/Dockerfile .

push-test:
	@docker push ${IMG_TEST}

deploy-test:
	@kubectl set image deployment/backend backend=${IMG_TEST} -n hoovada-staging

build-prod:
	@docker build -t ${IMG_PROD} -f ./docker/app/Dockerfile .

push-prod:
	@docker push ${IMG_PROD}

deploy-prod:
	@kubectl set image deployment/hoovada-services hoovada-services=${IMG_PROD}

login:
	@docker login -u ${DOCKER_USER} -p ${DOCKER_PASS}
