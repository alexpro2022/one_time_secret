# K8S
https://docs.docker.com/guides/python/deploy/#deploy-and-check-your-application

<br>
## Deploy and check your application:
<br>

1. Deploy your database to Kubernetes:
```bash
kubectl apply -f k8s/docker-postgres-kubernetes.yaml
```
You should see output that looks like the following, indicating your Kubernetes objects were created successfully:

    deployment.apps/postgres created
    service/postgres created
    persistentvolumeclaim/postgres-pvc created
    secret/postgres-secret created
<br>

2. Deploy your python application:
```bash
kubectl apply -f k8s/docker-python-kubernetes.yaml
```
You should see output that looks like the following, indicating your Kubernetes objects were created successfully:

    deployment.apps/docker-python-demo created
    service/service-entrypoint created
<br>

3. Make sure everything works by listing your deployments.
```bash
kubectl get deployments
```
Your deployment should be listed as follows:

    NAME                 READY   UP-TO-DATE   AVAILABLE   AGE
    docker-python-demo   1/1     1            1           48s
    postgres             1/1     1            1           2m39s

This indicates all one of the pods you asked for in your YAML are up and running.
<br>

4. Do the same check for your services:
```bash
kubectl get services
```
You should get output like the following.

    NAME                 TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
    kubernetes           ClusterIP   10.43.0.1      <none>        443/TCP          13h
    postgres             ClusterIP   10.43.209.25   <none>        5432/TCP         3m10s
    service-entrypoint   NodePort    10.43.67.120   <none>        8000:30001/TCP   79s
<br>

5. In addition to the default kubernetes service, you can see your service-entrypoint service, accepting traffic on port 30001/TCP and the internal ClusterIP postgres with the port 5432 open to accept connections from you python app.

In a terminal, curl the service. Note that a database was not deployed in this example.
```bash
curl http://localhost:30001/
```
<br>

6. Run the following commands to tear down your application.
```bash
kubectl delete -f k8s/docker-python-kubernetes.yaml
kubectl delete -f k8s/docker-postgres-kubernetes.yaml
docker system prune -f
```
<br>
