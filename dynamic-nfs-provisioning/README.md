## NFS subdir external provisioner
NFS subdir external provisioner is an automatic provisioner that use your existing and already configured NFS server to support dynamic provisioning of Kubernetes Persistent Volumes via Persistent Volume Claims. Persistent volumes are provisioned as ${namespace}-${pvcName}-${pvName}.

Documentation link: [nfs-subdir-external-provisioner](https://github.com/kubernetes-sigs/nfs-subdir-external-provisioner)

Next will be described how to configure NFS servcer on Ubuntu 20.04 and NFS clients on Kubernetes worker nodes.

### Configuration of NFS server
It requires to execute simple command and fill-in some configuration files.
```
$ sudo apt update
$ sudo apt install nfs-kernel-server -y
$ sudo systemctl status nfs-server
$ cd /srv
$ sudo mkdir -p nfs/kubedata
$ sudo chown nobody:nogroup /srv/nfs/kubedata/
$ sudo chmod -R 777 /srv/nfs/kubedata/
# add the following line to the end of config
# /srv/nfs/kubedata	*(rw,sync,no_subtree_check,no_root_squash,no_all_squash,insecure)
$ sudo vim /etc/exports
$ sudo systemctl enable --now nfs-server
$ sudo systemctl restart nfs-server
$ sudo systemctl status nfs-server
$ sudo exportfs -rav
$ sudo showmount -e localhost
```
In general that's all from the side of NFS servcer host, let's configure NFS clients on worker nodes.
```
$ sudo apt-get install nfs-common -y
# test that NFS mount is working
$ mount -t nfs 10.244.221.26 :/srv/nfs/kubedata /mnt
$ mount | grep kubedata
$ umount /mnt
```
### Change deployment file according to IP of NFS server
At deployment.yml change IP and NFS directory name according to NFS server configuration. And apply kubernetes manifest.
```
$ kubectl apply -f .
``` 
Then we could check NFS server shared directory that file SUCCESS created at /srv/nfs/kubedata/<volume name>/SUCCESS
