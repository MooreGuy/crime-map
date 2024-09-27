bash ./build.sh
kubectl delete -f ../kubernetes/reparse-logs-job.yaml
kubectl create -f ../kubernetes/reparse-logs-job.yaml

pod="$(kubectl get pods | grep reparse-logs | awk '{print $1}')"
echo "Waiting for pod ${pod} to be Ready"
kubectl wait --for=condition=Ready "pod/${pod}"
kubectl logs -f "${pod}" 
