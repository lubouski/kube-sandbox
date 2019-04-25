# Fluentd is a fully free and fully open-source log collector that instantly enables you to have a ‘Log Everything’ architecture.

## How to
Main focus is in utilyzing configMap that could replace standard fluentd.conf file with our custom one.
Second one is that we using source @type **tail** for incoming logs from files that mouted in pod from system,
and match section is for matching needed entries and piping them to file in our case.
```
$ kubectl apply -f fluentd-configmap.yml
$ kubectl apply -f fluentd-daemonset.yml
```
Then get pod id, and exec inside it to find fluentd output log file
```
$ kubectl get pods
$ kubectl exec -it fluentd-gxw28 bash
$ cd fluentd/log
$ ls
```
This is just test example, that why fluentd container may not have enoyght rights to access container logs,
but that could be simulated with creation of test files with ownership **999:999**


