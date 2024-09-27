docker build -t log-scraper .
docker tag log-scraper g1ymoore/crime-map:log-scraper
docker push g1ymoore/crime-map:log-scraper

kubectl delete job test-log-scraper
kubectl get pods | grep test-log-scraper | awk '{print $1;}' | xargs kubectl delete pod
kubectl create job test-log-scraper --from cronjob/log-scraper

pod=""
while  [ -z "$pod" ]; do pod="$(kubectl get pods | grep test-log-scraper | awk '{print $1}')"; done

echo "Waiting for pod ${pod} to be Ready"
kubectl wait --for=condition=Ready "pod/${pod}"
kubectl logs -f "${pod}"
