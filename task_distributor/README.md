# Flask API to Trigger Kubernetes Jobs

## Setup for development
```
mkvirtualenv wur_flask
workon wur_flask
```

```
pip install --upgrade pip
pip install -r requirements.txt
```

## Usage examples
```
curl -XPOST localhost:5000/k8s/cm --data @job.json --header "Content-Type: application/json"

#curl -XPOST localhost:5000/k8s/job
curl -XPOST localhost:5000/k8s/job \
    -H "Content-Type: application/json" \
    -d '{"path": "/tempZone/home/demo/P_project/I_investigation/S_study/DNA/A_assayX"}'

iinit
iput -f testfile /tempZone/home/davids/testwebhook/testfile
```

## Docker image

The docker image is currently available at [DockerHub](https://cloud.docker.com/repository/docker/haukurp/wur-task-distributor/general) or haukurp/wur-task-distributor.

### Automatic build
This dockerhub repo is connected to the github repo at https://github.com/sara-nl/wur-event-driven. When a tag is introduced in that repo a corresponding image and tag is created at DockerHub.

```
git tag 0.0.3
git push origin 0.0.3
```

### Manual build
```
docker login

# Maintain a version number according to the docker registry
version=0.1
docker build -t haukurp/wur-task-distributor:$version .
docker push haukurp/wur-task-distributor:$version
```
