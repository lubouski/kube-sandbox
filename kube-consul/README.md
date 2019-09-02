## Running Consul on Kubernetes without TLS

Primary method for installing Consul is via helm chard. Btw here will be presented installation with casual manifest files.

To run this setup use command below:

```
$ kubectl apply -f .
```

Cousul ui will be accessible via `NodePort` on any node in cluster. To join consul agent outside of the cluster additionally exposed pot `8301` also via `NodePort`.

Everything else is similar to how standard Consul operates. 
