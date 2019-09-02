## Kubenetes dashboard access only to `default` namespace

Generated service account on `default` namespace, will provide for us token to access Kubernetes dashboard but only in `default` namespace.

```
$ kubectl get secret
$ $ kubectl describe secret default-user-token-ptmxm
```

That's it.
