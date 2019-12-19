### How is it different from a HostPath Volume?

To better understand the benefits of a Local Persistent Volume, it is useful to compare it to a HostPath volume. HostPath volumes mount a file or directory from the host node’s filesystem into a Pod. Similarly a Local Persistent Volume mounts a local disk or partition into a Pod.

The biggest difference is that the Kubernetes scheduler understands which node a Local Persistent Volume belongs to. With HostPath volumes, a pod referencing a HostPath volume may be moved by the scheduler to a different node resulting in data loss. But with Local Persistent Volumes, the Kubernetes scheduler ensures that a pod using a Local Persistent Volume is always scheduled to the same node.

While HostPath volumes may be referenced via a Persistent Volume Claim (PVC) or directly inline in a pod definition, Local Persistent Volumes can only be referenced via a PVC. This provides additional security benefits since Persistent Volume objects are managed by the administrator, preventing Pods from being able to access any path on the host.

Additional benefits include support for formatting of block devices during mount, and volume ownership using fsGroup.

### How to Use Local Persistent Volume

First create StorageClass
```
$ kubectl apply -f storageclass.yml
```

Then apply PV, PVC and create test pod
```
$ kubectl apply -f local-pvc.yml -f local-pv.yml -f alpine-pod.yml
```

Then check that everything is working 
```
$ kubectl get pvc
NAME                  STATUS   VOLUME             CAPACITY   ACCESS MODES   STORAGECLASS    AGE
example-local-claim   Bound    example-local-pv   900Mi      RWO            local-storage   37m
```
```
$ kubectl exec -ti persistent-pod sh
/ # cd home/
/home # ls
lost+found      pv-rocks        sensetive.data
/home # exit
```

TL;DR - And do not forget to create a block storage (disk) format and mount it to some directory. In our example it is `/loopfs` 
```
# dd if=/dev/zero of=loopbackfile.img bs=100M count=10
# du -sh loopbackfile.img 
# losetup -fP loopbackfile.img
# losetup -a
# mkfs.ext4 /root/loopbackfile.img 
# mkdir /loopfs
# df -hP /loopfs/
# mount | grep loopfs

umount /loopfs
rmdir /loopfs
# losetup -d /dev/loop0
# rm /root/loopbackfile.img
```
