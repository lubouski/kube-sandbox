## Envoy Proxy could provide various methods for loadbalancing, not just standard Round Robin from Cloud solutions.

Envoy have interesting service discovery mode called `STRICT_DNS`. Kubernetes service with `spec.clusterIP: None` could provide just A records for the pods IP addresses that would match the label. Such service type is good for implementing when we want Loadbalancing. 

```
root@myapp-envoy-db9768d4d-tjvtf:/# nslookup myapp
Server:		10.96.0.10
Address:	10.96.0.10#53

Non-authoritative answer:
Name:	myapp.default.svc.cluster.local
Address: 192.168.113.23
Name:	myapp.default.svc.cluster.local
Address: 192.168.113.40
```

### Create Envoy Image
Just build and push image to your DockerHub account. In this example it is already built.
```
$ sudo docker build -t lubowsky/myapp-envoy:1 .
$ sudo docker push lubowsky/myapp-envoy:1 
```

### Create test deployments and service for app. And NodePort service and deployment for envoy
```
$ kubectl apply -f .
```

