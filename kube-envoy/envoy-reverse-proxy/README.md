## Envoy as reverse proxy for two services in Kubernetes

The setup is pretty similar to `envoy-loadbalancer` with minor differences in deployments services. And with `envoy.yml` configuration.

### Create Envoy Image
Just build and push image to your DockerHub account. In this example it is already built.
```
$ sudo docker build -t lubowsky/myapp-envoy:3 .
$ sudo docker push lubowsky/myapp-envoy:3 
```

### Prefix rewrite
```
master:
  prefix: "/prefix"
route:
  prefix_rewrite: "/"
```

### Create test deployments and service for app. And NodePort service and deployment for envoy

Access through `<node_ip>:30036/app1` or `<node_ip>:30036/app2` 
```
$ cd examples
$ kubectl apply -f .
```
