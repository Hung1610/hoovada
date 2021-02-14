REGISTRY   		:= registry.gitlab.com/hoovada/hoovada-services
REPO_NAME   	:= $$(/usr/bin/basename -s .git `git config --get remote.origin.url`)
GIT_COMMIT 		:= $$(git rev-parse --short HEAD)
GIT_BRANCH 		:= $$(git branch | grep \* | cut -d ' ' -f2)
DATE 			:= $$(date +'%d%b%Y')

API   			:= ${REGISTRY}:api-${GIT_COMMIT}-${GIT_BRANCH}-${DATE}
SOCKETIO 		:= ${REGISTRY}:socketio-${GIT_COMMIT}-${GIT_BRANCH}-${DATE}
SCHEDULED_JOBS  := ${REGISTRY}:scheduled-jobs-${GIT_COMMIT}-${GIT_BRANCH}-${DATE}
NGINX			:= ${REGISTRY}:nginx-${GIT_COMMIT}-${GIT_BRANCH}-${DATE}


build:
	@docker build -t ${API} -f ./docker/app/Dockerfile .
	@docker build -t ${SCHEDULED_JOBS} -f ./docker/scheduled_jobs/Dockerfile .
	@docker build -t ${NGINX} -f ./docker/nginx/Dockerfile .

push:
	@docker push ${API}
	@docker push ${SCHEDULED_JOBS}
	@docker push ${NGINX}

deploy-staging:
	@kubectl set image deployment/app app=${API} nginx=${NGINX} -n interactive-service --context=do-sgp1-test --record
	@kubectl set image deployment/scheduled-jobs scheduled-jobs=${SCHEDULED_JOBS} -n interactive-service --context=do-sgp1-test --record

all-staging: build push deploy-staging

deploy-test:
	@kubectl set image deployment/app app=${API} nginx=${NGINX} -n interactive-service --context=do-sgp1-test --record
	@kubectl set image deployment/scheduled-jobs scheduled-jobs=${SCHEDULED_JOBS} -n interactive-service --context=do-sgp1-test --record

all-test: build push deploy-test

deploy-live:
	@kubectl set image deployment/app app=${API} nginx=${NGINX} -n interactive-service --context=do-sgp1-production --record
	@kubectl set image deployment/scheduled-jobs scheduled-jobs=${SCHEDULED_JOBS} -n interactive-service --context=do-sgp1-production --record

all-live: build push deploy-live

login:
	@docker login registry.gitlab.com