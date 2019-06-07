# Prometheus Operator

Operators were introduced by CoreOS as a class of software that operates other software, putting operational knowledge collected by humans into software. Read more in the original blog post, [Introducing Operators][introducing-operators].

The Prometheus Operator serves to make running Prometheus on top of Kubernetes as easy as possible, while preserving Kubernetes-native configuration options.

### Prometheus Operator manifest
Apply a Prometheus Operator Deployment, and its required ClusterRole, ClusterRoleBinding, and Service Account.
```
$ kubectl apply -f prometheus-operator.yml
```
Then deploy three instances of a simple example application, which listens and exposes metrics on port `8080`
```
$ kubectl apply -f example-app-depl.yml
```
The ServiceMonitor has a label selector to select Services and their underlying Endpoint objects. The Service object for the example application selects the Pods by the `app` label having the `example-app` value. The Service object also specifies the port on which the metrics are exposed.
```
$ kubectl apply -f example-app-service.yml
```
This Service object is discovered by a ServiceMonitor, which selects in the same way. The `app` label must have the value `example-app.
````
$ kubectl apply -f prometheus-servicemonitor.yml
```
Create a ClusterRole and ClusterRoleBinding for the Prometheus Pods.
```
$ kubectl apply -f prometheus-rbac.yml
```
Finally, a Prometheus object defines the serviceMonitorSelector to specify which `ServiceMonitors` should be included. Above the label `team: frontend` was specified, so that's what the Prometheus object selects by.
```
$ kubectl apply -f prometheus-prometheus.yml
```
To access the Prometheus instance it must be exposed to the outside. This example exposes the instance using a Service of type clusterIP and ingress service with rewrite rule to `/prometheus`.
```
$ kubectl apply -f prometheus-service.yml
```

Once this Service is created the Prometheus web UI is available under the lubouski.test.com:30000/prometheus (please check ingress config file and provide DNS entry for IP of the master cluster node). The targets page in the web UI now shows that the instances of the example application have successfully been discovered.


