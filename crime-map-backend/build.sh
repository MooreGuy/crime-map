#!/bin/sh
set -e
set -u

if [ "$#"  -ne 1 ]; then
	echo "Usage: ./build.sh <env>"
	exit 1
fi

env="$1"

docker build -t crime-map-backend .
docker tag crime-map-backend g1ymoore/crime-map:crime-map-backend
docker push g1ymoore/crime-map:crime-map-backend

if [ "${env}" = "prod" ]; then
	kubectl config use-context prod
else
	kubectl config use-context cm-dev
fi

kubectl rollout restart deployment.apps/crime-map-backend
kubectl rollout status deployment.apps/crime-map-backend
kubectl logs -f deployment/crime-map-backend 

#pod=""
#while  [ -z "$pod" ]; do pod="$(kubectl get pods | grep crime-map-backend | awk '{print $1}')"; done
#kubectl logs -f "${pod}"

