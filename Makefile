REGISTRY   		:= registry.gitlab.com/hoovada/hoovada-services
VERSION 		:= v0.2.0
REPO_NAME   	:= $$(/usr/bin/basename -s .git `git config --get remote.origin.url`)
GIT_COMMIT 		:= $$(git rev-parse --short HEAD)
GIT_BRANCH 		:= $$(git rev-parse --abbrev-ref HEAD)
API_TEST    	:= ${REGISTRY}:${REPO_NAME}-${GIT_BRANCH}-${GIT_COMMIT}
SOCKETIO_TEST   := ${REGISTRY}:socketio-${GIT_BRANCH}-${GIT_COMMIT}
API_LIVE   		:= ${REGISTRY}:${VERSION}
SOCKETIO_LIVE   := ${REGISTRY}:socketio-${VERSION}
IMG_NGINX		:= ${REGISTRY}:nginx-${REPO_NAME}-${GIT_COMMIT}

build-test:
	@docker build -t ${API_TEST} -f ./docker/app/Dockerfile .
	@docker build -t ${SOCKETIO_TEST} -f ./docker/app_socketio/Dockerfile .
	@docker build -t ${IMG_NGINX} -f ./docker/nginx/Dockerfile .

push-test:
	@docker push ${API_TEST}
	@docker push ${SOCKETIO_TEST}
	@docker push ${IMG_NGINX}

deploy-test:
	@kubectl set image deployment/backend-${GIT_BRANCH} backend-${GIT_BRANCH}=${API_TEST} nginx=${IMG_NGINX} -n hoovada-staging --record
	@kubectl set image deployment/backend-socketio backend-socketio=${API_TEST} nginx=${IMG_NGINX} -n hoovada-staging --record

all-test: build-test push-test deploy-test

build-live:
	@docker build -t ${API_LIVE} -f ./docker/app/Dockerfile .
	@docker build -t ${SOCKETIO_TEST} -f ./docker/app_socketio/Dockerfile .
	@docker build -t ${IMG_NGINX} -f ./docker/nginx/Dockerfile .

push-live:
	@docker push ${API_LIVE}
	@docker push ${SOCKETIO_LIVE}
	@docker push ${IMG_NGINX}

deploy-live:
	@kubectl set image deployment/backend-live backend-live=${API_TEST} nginx=${IMG_NGINX} -n hoovada-live --record
	@kubectl set image deployment/backend-socketio backend-socketio=${API_TEST} nginx=${IMG_NGINX} -n hoovada-live --record

all-live: build-live push-live deploy-live

login:
	@docker login registry.gitlab.com
