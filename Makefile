REGISTRY   		:= registry.gitlab.com/hoovada/hoovada-services
REPO_NAME   	:= $$(/usr/bin/basename -s .git `git config --get remote.origin.url`)
GIT_COMMIT 		:= $$(git rev-parse --short HEAD)
GIT_BRANCH 		:= $$(git rev-parse --abbrev-ref HEAD)
DATE 			:= $$(date +'%d%b%Y')

API_TEST    			:= ${REGISTRY}:api-${GIT_COMMIT}-${DATE}
SOCKETIO_TEST   		:= ${REGISTRY}:socketio-${GIT_COMMIT}-${DATE}
SCHEDULED_JOBS_TEST   	:= ${REGISTRY}:scheduled-jobs-${GIT_COMMIT}-${DATE}
NGINX_TEST				:= ${REGISTRY}:nginx-${GIT_COMMIT}-${DATE}

VERSION 				:= v0.2.0
API_LIVE   				:= ${REGISTRY}:api-${VERSION}-${DATE}
SOCKETIO_LIVE   		:= ${REGISTRY}:socketio-${VERSION}-${DATE}
SCHEDULED_JOBS_LIVE   	:= ${REGISTRY}:scheduled-jobs-${GIT_COMMIT}-${DATE}
NGINX_LIVE				:= ${REGISTRY}:nginx-${VERSION}-${DATE}

build:
	@docker build -t ${API_TEST} -f ./docker/app/Dockerfile .
	@docker build -t ${SOCKETIO_TEST} -f ./docker/app_socketio/Dockerfile .
	@docker build -t ${SCHEDULED_JOBS_TEST} -f ./docker/scheduled_jobs/Dockerfile .
	@docker build -t ${NGINX_TEST} -f ./docker/nginx/Dockerfile .

push:
	@docker push ${API_TEST}
	@docker push ${SOCKETIO_TEST}
	@docker push ${SCHEDULED_JOBS_TEST}
	@docker push ${NGINX_TEST}

deploy:
	@kubectl set image deployment/app app=${API_TEST} nginx=${NGINX_TEST} -n hoovada-staging --record
	@kubectl set image deployment/socketio socketio=${SOCKETIO_TEST} nginx=${NGINX_TEST} -n hoovada-staging --record
	@kubectl set image deployment/scheduled-jobs scheduled-jobs=${SCHEDULED_JOBS_TEST} -n hoovada-staging --record

all: build push deploy

build-live:
	@docker build -t ${API_LIVE} -f ./docker/app/Dockerfile .
	@docker build -t ${SOCKETIO_LIVE} -f ./docker/app_socketio/Dockerfile .
	@docker build -t ${SCHEDULED_JOBS_LIVE} -f ./docker/scheduled_jobs/Dockerfile .
	@docker build -t ${NGINX_LIVE} -f ./docker/nginx/Dockerfile .

push-live:
	@docker push ${API_LIVE}
	@docker push ${SOCKETIO_LIVE}
	@docker push ${NGINX_LIVE}

deploy-live:
	@kubectl set image deployment/api api=${API_LIVE} nginx=${NGINX_LIVE} -n hoovada-live --record
	@kubectl set image deployment/socketio socketio=${API_TEST} nginx=${NGINX_LIVE} -n hoovada-live --record
	@kubectl set image deployment/scheduled-jobs scheduled-jobs=${SCHEDULED_JOBS_LIVE} -n hoovada-live --record

all-live: build-live push-live deploy-live

login:
	@docker login registry.gitlab.com
