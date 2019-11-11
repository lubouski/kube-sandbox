# Kubernetes create kubeconfig for new user
By default after kubernetes installation you get admin-config **/etc/kubernetes/admin.conf** with full admin rights, so it is in our interest to configure RBAC for our cluster. 

## Get started
First we need to create a client certificate. 
``` 
$ mkdir cert && cd cert && openssl genrsa -out user1.key 2048
```
Then generate a Client Sign Request (CSR).
```
$ openssl req -new -key user1.key -out user1.csr -subj "/CN=user1/O=group1"
```
And last one in Cert generation, certificate itself.
```
$ sudo openssl x509 -req -in user1.csr -CA /etc/kubernetes/pki/ca.crt -CAkey /etc/kubernetes/pki/ca.key -CAcreateserial -out user1.crt -days 500
```
## Create user, context, role and rolebinding
Set a user entry in kubeconfig.
```
$ kubectl config set-credentials user1 --client-certificate=user1.crt --client-key=user1.key
```
Set a context entry in kubeconfig.
```
$ kubectl config set-context user1-context --cluster=kubernetes --user=user1
```
Create a Role.
```
$ kubectl apply -f user-role.yml
```
Create a BindingRole.
```
$ kubectl apply -f user-rolebinding.yml
```
Set user1-context.
```
$ kubectl config set-context user1-context --cluster=kubernetes --user=user1
```
Switch to context user1-context.
```
$ kubectl config use-context user1-context
```
Save kubeconfig output to a file.
```
$ kubectl config view --flatten --minify > user1-cluster-cert.txt
```
Last one, copy user1-cluster-cert.txt to administrator PC in **./kube/config**. And try to run any commands.
```
$ kubectl get pods -n kube-system
Error from server (Forbidden): pods is forbidden: User "user1" cannot list resource "pods" in API group "" in the namespace "kube-system"
``` 
Now user (administrator or developer) could access cluster with his own **kubeconfig** file, which could have restrictions as in our case only on get, list and watch pods, on namespace **default**.

For easy configuration of read-only user, we can use cluster-roles
```
$ kubectl get clusterroles | grep -v '^system'
$ kubectl apply -f cluster-rolebinding.yml
``` 
Then test that your user2 can only read any info from cluster in any namespace you want
```
$ KUBECONFIG=~/.kube/test-config kubectl get po -n kube-system
```

## Since `Kubernetes 1.15` kubeconfigfile could be generated with kubeadm
NB: advertise address could be found at `api-server` in /etc/kubernetes/manifests/kube-apiserver.yaml.
```
$ kubeadm alpha kubeconfig user --client-name=mynewuser --apiserver-advertise-address 192.168.100.200
```
