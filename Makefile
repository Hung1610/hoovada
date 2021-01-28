REGISTRY   		:= registry.gitlab.com/hoovada/hoovada-services
REPO_NAME   	:= $$(/usr/bin/basename -s .git `git config --get remote.origin.url`)
GIT_COMMIT 		:= $$(git rev-parse --short HEAD)
GIT_BRANCH 		:= $$(git describe --tags --exact-match 2> /dev/null || git symbolic-ref -q --short HEAD || git rev-parse --short HEAD)
DATE 			:= $$(date +'%d%b%Y')

API   			:= ${REGISTRY}:api-${GIT_COMMIT}-${GIT_BRANCH}-${DATE}
SOCKETIO 		:= ${REGISTRY}:socketio-${GIT_COMMIT}-${GIT_BRANCH}-${DATE}
SCHEDULED_JOBS  := ${REGISTRY}:scheduled-jobs-${GIT_COMMIT}-${GIT_BRANCH}-${DATE}
NGINX			:= ${REGISTRY}:nginx-${GIT_COMMIT}-${GIT_BRANCH}-${DATE}


build:
	@docker build -t ${API} -f ./docker/app/Dockerfile .
	@docker build -t ${SOCKETIO} -f ./docker/app_socketio/Dockerfile .
	@docker build -t ${SCHEDULED_JOBS} -f ./docker/scheduled_jobs/Dockerfile .
	@docker build -t ${NGINX} -f ./docker/nginx/Dockerfile .

push:
	@docker push ${API}
	@docker push ${SOCKETIO}
	@docker push ${SCHEDULED_JOBS}
	@docker push ${NGINX}

deploy-staging:
	@kubectl set image deployment/app app=${API} nginx=${NGINX} -n hoovada-staging --record
	@kubectl set image deployment/socketio socketio=${SOCKETIO} nginx=${NGINX} -n hoovada-staging --record
	@kubectl set image deployment/scheduled-jobs scheduled-jobs=${SCHEDULED_JOBS} -n hoovada-staging --record

all-staging: build push deploy-staging

deploy-test:
	@kubectl set image deployment/app app=${API} nginx=${NGINX} -n hoovada-test --record
	@kubectl set image deployment/socketio socketio=${SOCKETIO} nginx=${NGINX} -n hoovada-test --record
	@kubectl set image deployment/scheduled-jobs scheduled-jobs=${SCHEDULED_JOBS} -n hoovada-test --record

all-test: build push deploy-test

deploy-live:
	@kubectl set image deployment/app app=${API} nginx=${NGINX} -n hoovada-live --record
	@kubectl set image deployment/socketio socketio=${SOCKETIO} nginx=${NGINX} -n hoovada-live --record
	@kubectl set image deployment/scheduled-jobs scheduled-jobs=${SCHEDULED_JOBS} -n hoovada-live --record

all-live: build push deploy-live

login:
	@docker login registry.gitlab.com