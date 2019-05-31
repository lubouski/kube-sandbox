# Storage example of Persistent volume type - *NFS* 

## Why Do We Need Persistent Volumes?
The rationale for using a PersistentVolume  resource in Kubernetes is quite simple. On the one hand, we have different storage infrastructures such as Amazon EBS (Elastic Block Storage), GCE Persistent Disk, or GlusterFS, each having its specific storage type (e.g., block storage, NFS, object storage, data center storage), architecture, and API. If we were to attach these diverse storage types manually, we would have to develop custom plugins to interact with the external drive’s API, such as mounting the disk, requesting capacity, managing the disk’s life cycle, etc. We would also need to configure a cloud storage environment, all of which would result in unnecessary overhead.

Fortunately, the Kubernetes platform simplifies storage management for you. Its PersistentVolume  subsystem is designed to solve the above-described problem by providing APIs that abstract details of the underlying storage infrastructure (e.g., AWS EBS, Azure Disk etc.), allowing users and administrators to focus on storage capacity and storage types their applications will consume rather than the subtle details of each storage provider’s API.

## How to
First of all we need to install NFS server (what would be available to Kubernetes via network), and NFS clients on every Node.
And export shred directory on the NFS server (via /etc/exports).
```
client$ sudo apt update
client$ sudo apt install nfs-common
 
server$ sudo apt update
$server sudo apt install nfs-kernel-server
``` 
Configuring the NFS Exports on the Host Server
```
server$ sudo nano /etc/exports

/var/nfs/general    203.0.113.24(rw,sync,no_root_squash,no_subtree_check)

server$ sudo systemctl restart nfs-kernel-server
server$ sudo ufw status
```

To check whether mounting to server is working:
```
client$ sudo mkdir -p /nfs/general 
client$ sudo mount 203.0.113.0:/var/nfs/general /nfs/general

client$ df -h
```

Last one apply Kubernetes manifest of PV, PVC and pod manifest with alpine container inside, and look at the */opt* directory
and create some file, then check NFS server directory */var/nfs/general* 
```
$ kubectl apply -f storage-pv.yml
$ kubectl apply -f storage-pvc.yml
$ kubectl apply -f storage-pod.yml

$ kubectl exec -ti <pod-hash> sh
# touch /opt/test1.txt
```






