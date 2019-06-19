## Fluentbit is the fully open source sollution for log streaming writed on "C"
Main caveat is to generate logs in container. Run inside the `alpine` container `ln -sf /proc/1/fd/1 /var/log/test.log`
It could be easy done with `echo "hello world" >> /var/log/test.log`. And create directory on all nodes `mkdir /tmp/fluentbit` and thenfinally `apply` manifests from git repo.

### How to
Just apply manifest files:
```
kubectl apply -f fluentbit-namespace.yml
kubectl apply -f fluentbit-service-account.yml
kubectl apply -f fluentbit-role.yml
kubectl apply -f fluentbit-rolebinding.yml
kubectl apply -f fluentbit-configmap.yml
kubectl apply -f fluentbit-ds.yml
``` 


