REGISTRY   		:= registry.gitlab.com/hoovada/hoovada-services
REPO_NAME   	:= $$(/usr/bin/basename -s .git `git config --get remote.origin.url`)
GIT_COMMIT 		:= $$(git rev-parse --short HEAD)
GIT_BRANCH 		:= $$(git rev-parse --abbrev-ref HEAD)
API_TEST    	:= ${REGISTRY}:${REPO_NAME}-${GIT_BRANCH}-${GIT_COMMIT}
SOCKETIO_TEST   := ${REGISTRY}:socketio-${GIT_BRANCH}-${GIT_COMMIT}
VERSION 		:= v0.2.0

API_LIVE   		:= ${REGISTRY}:${VERSION}
SOCKETIO_LIVE   := ${REGISTRY}:socketio-${VERSION}

build-test:
	@docker build -t ${API_TEST} -f ./docker/app/Dockerfile .
	@docker build -t ${SOCKETIO_TEST} -f ./docker/app_socketio/Dockerfile .

push-test:
	@docker push ${API_TEST}
	@docker push ${SOCKETIO_TEST}

deploy-test:
	@kubectl set image deployment/backend-${GIT_BRANCH} backend-${GIT_BRANCH}=${API_TEST} socketio=${SOCKETIO_TEST} -n hoovada-staging --record

all-test: build-test push-test deploy-test

build-live:
	@docker build -t ${API_LIVE} -f ./docker/app/Dockerfile .
	@docker build -t ${SOCKETIO_TEST} -f ./docker/app_socketio/Dockerfile .

push-live:
	@docker push ${API_LIVE}
	@docker push ${SOCKETIO_LIVE}

deploy-live:
	@kubectl set image deployment/backend-prod backend-prod=${API_LIVE} socketio=${SOCKETIO_LIVE} -n hoovada-live --record

all-live: build-live push-live deploy-live

login:
	@docker login registry.gitlab.com
