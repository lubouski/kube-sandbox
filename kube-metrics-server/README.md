## Kubernetes metrics-sever. 
Grab metrics from podes and nodes (CPU, Memory). 

### Deployment 
```
$ kubectl create -f .
```
Note: some additional parrameters should be passed to metrics-server deployment
```
        command:
          - /metrics-server
          - --kubelet-insecure-tls
          - --requestheader-allowed-names=aggregator
          - --kubelet-preferred-address-types=InternalIP
```

