# Kubernetes Web UI (dashboard)

Dashboard is a web-based Kubernetes user interface. You can use Dashboard to deploy containerized applications to a Kubernetes cluster, troubleshoot your containerized application, and manage the cluster resources. You can use Dashboard to get an overview of applications running on your cluster, as well as for creating or modifying individual Kubernetes resources (such as Deployments, Jobs, DaemonSets, etc). For example, you can scale a Deployment, initiate a rolling update, restart a pod or deploy new applications using a deploy wizard.

## How to
```
$ kubectl apply -f dashboard-admin.yml
```

Creates `cluster-admin` role for accessing kubernetes-dashboard 

```
$ kubectl apply -f kubernetes-dashboard.yml
```

Deploys kubernetes dashboard, note: args  `--enable-skip-login` added to allow anonimous user to access dashboard, via Skip button.

```
$ KUBECONFIG=~/.kube/test-config kubectl proxy -p 8001
```

Assumed that you copied admin config from kubernetes master server, to your local host and changed name to test-config.
Command bellow start proxy to your kubernetes dashboard. To access it go to url
* `http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/` 
