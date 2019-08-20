## Getting started
The following example sets up the Velero server and client, then backs up and restores a sample application.
For simplicity, the example uses `Minio`, an S3-compatible storage service that runs locally on your cluster.

### Download Velero
Download the [latest official release's](https://github.com/heptio/velero/releases) tarball for your client platform.
```
$ mkdir velero && cd velero
$ wget https://github.com/heptio/velero/releases/download/v1.0.0/velero-v1.0.0-linux-amd64.tar.gz
$ tar zxf velero-v1.0.0-linux-amd64.tar.gz
$ sudo mv velero-v1.0.0-linux-amd64/velero /usr/local/bin/
$ rm -rf velero*
```

### Create a Velero-specific credentials file (`credentials-velero`) 
```
$ cat <<EOF>> credentials-velero
[default]
aws_access_key_id = minio
aws_secret_access_key = minio123
EOF
```

### Start `Minio`
Start the server and the local storage service. In the Velero directory, run
```
$ kubectl apply -f 00-minio-deployment.yaml
``` 
Provide <node-ip> and <nodeport>, check it in `kubectl get svc -n velero` for `Minio`
```
$ velero install \
    --provider aws \
    --bucket velero \
    --secret-file ./credentials-velero \
    --use-volume-snapshots=false \
    --backup-location-config region=minio,s3ForcePathStyle="true",s3Url=http://<node-ip>:<node-port>
```
Check that `Minio` available in your browser. And see that `velero` bucket is created. 

### Enable autocompletion if you want
```
$ source <(velero completion zsh)
```

### Example of how to use `Backup` and `Restore` for any objects in kubernetes cluster
Run test deployment with nginx server in any namespace
```
$ kubectl create ns testing
$ kubectl run nginx --image nginx --replicas 2 -n testing
```
Create `Backup` for with particular namespace
```
$ velero backup create first-nginx-backup --include-namespaces testing
```
Check that `Backup` was created, in `Minio` and with commands:
```
$ kubectl -n velero get backups
$ velero backups get
```
Than we simulate production crash, by deleting a testing namespace
```
$ kubectl delete ns testing
namespace "testing" deleted
$ kubectl get po -n testing
No resources found.
```
Time to use `Velero` Backup and Restore your configuration
```
$ velero restore create fisrt-backup-restore --from-backup first-nginx-backup 
$ kubectl get po -n testing
NAME                     READY   STATUS    RESTARTS   AGE
nginx-7bb7cd8db5-j6cbk   1/1     Running   0          68s
nginx-7bb7cd8db5-wssg4   1/1     Running   0          68s
```

Additionally we could `Backup` only some resources that we need:
```
$ velero backup create firstbackup --include-namespaces testing --include-resources pods,deployments
```
(Optional) Create regularly scheduled backups based on a cron expression using the app=nginx label selector:
```
$ velero schedule create nginx-daily --schedule="0 1 * * *" --selector app=nginx 
```

### Clean up
If you want to delete any backups you created, including data in object storage and persistent volume snapshots, you can run:
```
$ velero backup delete BACKUP_NAME
``` 
To completely uninstall Velero, minio, and the nginx example app from your Kubernetes cluster:
```
$ kubectl delete namespace/velero clusterrolebinding/velero
$ kubectl delete crds -l component=velero
$ kubectl delete -f examples/nginx-app/base.yaml
```

Now you get basics of how to use `Velero` aka `Valera`
