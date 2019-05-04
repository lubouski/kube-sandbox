# Ingress is the built‑in Kubernetes load‑balancing framework for HTTP traffic. With Ingress, you control the routing of external traffic. When running on public clouds like AWS or GKE, the load-balancing feature is available out of the box.

## How to 
Deploy the two same web apps with a different name and two replicas for each:
```
$ kubectl create -f app-deployment.yml -f app-service.yml
```

### Create Nginx Ingress Controller, all resources for Nginx Ingress controller will be in a separate namespace:
### Default endpoint redirects all requests which are not defined by Ingress rules:
```
$ kubectl create namespace ingress
$ kubectl create -f default-backend-deployment.yml -f default-backend-service.yml -n=ingress
```

### Create a Nginx config to show a VTS page on our load balancer:
### Before we create Ingress controller and move forward you might need to create RBAC rules. Clusters deployed with kubeadm have RBAC enabled by default:
```
$ kubectl create -f nginx-ingress-controller-config-map.yml -n=ingress
$ kubectl create -f nginx-ingress-controller-roles.yml -n=ingress
$ kubectl create -f nginx-ingress-controller-deployment.yml -n=ingress
```

### Define Ingress rules for load balancer status page:
### And Ingress rules for sample web apps:
```
$ kubectl create -f nginx-ingress.yml -n=ingress
$ kubectl create -f app-ingress.yml
```

### The last step is to expose nginx-ingress-lb deployment for external access. We will expose it with NodePort, but we could also use ExternalIPs(192.168.42.76):
```
$ kubectl create -f nginx-ingress-controller-service.yml -n=ingress
```

Verify everything by accessing at those endpoints:
http://lubouski.test.com:30000/app1
http://lubouski.test.com:30000/app2
http://lubouski.test.com:32000/nginx_status
