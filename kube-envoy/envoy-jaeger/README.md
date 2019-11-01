## Simplified example of jaeger service tracing 

Here we have two simple services written on `python:flask`, sender and receiver. 
Sender redirects traffic to kubernetes service `myapp2` which represent envoy proxy to receiver service, and intergration with `jaeger`

### Run setup
```
$ kubectl apply -f .
```

### For testing we will use `busybox` container
```
$ kubectl run test --image=busybox:1.28 --restart=Never --rm -ti
$ wget myapp2
```

### Jaeger UI could be accessed via node port

```
In browser go to `<node_ip>:30037` 
```


