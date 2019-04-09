# Kubernetes setup



## Initial setup
The following setup only happens once.

### Connecting to the k8s cluster
Go to https://145.100.58.53/ and log in.
Navigate to the cluster page and download the Kubeconfig file to your local
machine.

    export KUBECONFIG=/path/to/kubeconfig.yaml
    # test it
    kubectl get po

### Permissions to start jobs
Since the cluster has RBAC enabled pods need to be given permission to access
the Kubernetes API.

    kubectl apply -f task_distributor_rbac.yaml



## Updating deployments

    kubectl apply -f task_distributor.yaml

To update the job description use

    # to update
    kubectl create cm job-template --from-file=job.yaml -o yaml --dry-run | kubectl replace -f - 
    # to create
    kubectl create cm job-template --from-file=job.yaml -o yaml --dry-run | kubectl create -f -



## Running the python code

Currently the application is deployed at
http://145.100.58.247:31162

The API has a Swagger endpoint.

```
curl -XPOST http://145.100.58.247:31162/k8s/job \
    -H "Content-Type: application/json" \
    -d '{"path": "/tempZone/home/demo/P_project/I_investigation/S_study/DNA/A_assayX"}'
```
