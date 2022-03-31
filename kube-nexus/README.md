## Install and configure single instance of Nexus
To install single instance of Nexus just sinply run command bellow, what is important to notice is `nexus-nodeport.yml` manifest, which could help us configure initial Nexus admin user and password via setup wizard.
```
$ kubectl create ns nexus
$ kubectl apply -f .
``` 
After installation command, Nexus service showld be running as statefullSet container. And could be accessed via <worker-node-ip>:30339 be aware that particular NodePort is free and can be used.
```
# verify that nexus is working
$ kubectl get po -n nexus
NAME      READY   STATUS    RESTARTS        AGE
nexus-0   1/1     Running   2 (3h16m ago)   46h
```
Then go to the browser and paste `<worker-node-ip>:30339` URL, sign in with default credencials, username: `admin`, and password could be retrieved from nexus-0 conatainer, as presented bellow.
```
$ kubectl exec -ti nexus-0 -n nexus bash
kubectl exec [POD] [COMMAND] is DEPRECATED and will be removed in a future version. Use kubectl exec [POD] -- [COMMAND] instead.
bash-4.4$ cd /nexus-data/
bash-4.4$ cat admin.password
```
Use output of `bash-4.4$ cat admin.password` as initial password for sign-in to Nexus, and follow the setup wizard. Last step is to delete NodePort service from cluster.
```
$ kubectl delete -f nexus-nodeport.yml
```
