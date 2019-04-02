# Kubernetes storage introduction

We create a Pod that pulls an NGINX container (application container) writing some logs and the sidecar container with a busybox  Docker image that provides several Unix tools like bash in a single executable file.

## How to
```
$ kubectl create -f sidecar-logging.yaml
```

Our Pod is now running but is not exposed to the external world. In order to access NGINX server from outside of our cluster, we need to create a NodePort  Service type like this:

```
$ kubectl expose pod sidecar-logging --type=NodePort --port=80
```

Now, we can access NGINX on the yourhost:NodePort , which will redirect to the NGINX container listening on the port:80 . However, first we need to find out what port Kubernetes assigned to the NodePort  service.

```
$ kubectl describe service sidecar-logging
```

Now, we can trigger the server to write some logs to the /var/log/nginx/access.log  file by accessing yourhost:<NodePort>  from your browser or sending arbitrary curl  requests.
 
```
$ kubectl logs sidecar-logging busybox
```

This will return access logs specifying the IP of the machine that sent the request, HTTP resources to which requests were sent, type of requests, user agents (browsers), and dates.
