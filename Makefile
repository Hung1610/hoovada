REGISTRY   		:= registry.gitlab.com/hoovada/hoovada-services

REPO_NAME   	:= $$(/usr/bin/basename -s .git `git config --get remote.origin.url`)
GIT_COMMIT 		:= $$(git rev-parse --short HEAD)
GIT_BRANCH 		:= $$(git rev-parse --abbrev-ref HEAD)
TAG_TEST 		:= ${REPO_NAME}-${GIT_BRANCH}-${GIT_COMMIT}
IMG_TEST    	:= ${REGISTRY}:${TAG_TEST}

VERSION 		:= v1.0.0
IMG_PROD    	:= ${REGISTRY}:${VERSION}


build-test:
	@docker build -t ${IMG_TEST} -f ./docker/app/Dockerfile .

push-test:
	@docker push ${IMG_TEST}

deploy-test:
	@kubectl set image deployment/backend-${GIT_BRANCH} backend-${GIT_BRANCH}=${IMG_TEST} -n hoovada-staging

build-prod:
	@docker build -t ${IMG_PROD} -f ./docker/app/Dockerfile .

push-prod:
	@docker push ${IMG_PROD}

deploy-prod:
	@kubectl set image deployment/backend-prod backend-prod=${IMG_PROD}

login:
	@docker login registry.gitlab.com
