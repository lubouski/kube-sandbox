# Kubernetes Training: How to Deploy a Cluster from Scratch

This lab contains the commands and script used for the Supergiant webinar _Kubernetes Training: How to Deploy a Cluster from Scratch_. The slides for this webinar can be found [here](test).

Note: This lab is meant to be performed on OS X, as the target audience for this webinar generally prefers it.

---

# Preparing a VM

This section will prepare an environment for kube setup.

## Install Vagrant & VirtualBox

1. Install the latest version of [Vagrant](https://www.vagrantup.com/downloads.html).
1. Install the latest version of [Virtualbox](https://www.virtualbox.org/wiki/Downloads).

1. Test the installation:

    OS X/Linux:

    ```bash
    vagrant --version
    vboxmanage --version
    ```

1. Create a directory for the kube:

    ```bash
    mkdir super-u-kube
    cd super-u-kube
    ```

1. Create a xenial64 Vagrant environment:

    ```bash
    vagrant init ubuntu/xenial64
    ```

1. Start the VM:

    ```bash
    vagrant up --provider virtualbox
    ```

1. SSH into the VM, and switch to root:

    ```bash
    vagrant ssh
    sudo -i
    ```

1. Update and upgrade Ubuntu:

    ```bash
    apt update
    apt upgrade -y
    ```

## Install K8s Binaries

The next steps will prepare the VM for kube setup.

1. Install Docker:

    ```bash
    apt install docker.io -y
    ```

1. Download and extract the K8s binaries:

    ```bash
    wget https://storage.googleapis.com/kubernetes-release/release/v1.9.11/kubernetes-server-linux-amd64.tar.gz
    tar -xzf kubernetes-server-linux-amd64.tar.gz
    ```

1. Install the K8s binaries:

    ```bash
    cd kubernetes/server/bin/
    mv kubectl kubelet kube-apiserver kube-controller-manager kube-scheduler kube-proxy /usr/bin/
    cd
    ```

1. Test that `kubectl` can now be called:

    ```bash
    kubectl
    ```

1. Remove unused resources:

    ```bash
    rm -rf kubernetes kubernetes-server-linux-amd64.tar.gz
    ```

---

# Creating the Kube

## Set up kubelet

The next steps will get kubelet working and show it in action.

1. Create a directory for kubelet manifests:

    ```bash
    mkdir -p /etc/kubernetes/manifests
    ```

1. Start kubelet in the background:

    ```bash
    kubelet --pod-manifest-path /etc/kubernetes/manifests &> /etc/kubernetes/kubelet.log &
    ```

1. Check its status and initial logs:

    ```bash
    ps -au | grep kubelet
    head /etc/kubernetes/kubelet.log
    ```

1. Create a Pod using the kubelet's manifest directory:

    ```bash
    cat <<EOF > /etc/kubernetes/manifests/kubelet-test.yaml
    ```

    ```yaml
    apiVersion: v1
    kind: Pod
    metadata:
      name: kubelet-test
    spec:
      containers:
      - name: alpine
        image: alpine
        command: ["/bin/sh", "-c"]
        args: ["while true; do echo SuPeRgIaNt; sleep 15; done"]
    ```

    ```bash
    EOF
    ```

1. Verify that kubelet has started the Pod (this may take up to a minute):

    ```bash
    docker ps
    ```

1. Check the container's logs:

    ```bash
    docker logs {CONTAINER ID}
    ```

## Set up etcd

The next steps will get the kube's database/state store working and show it in action.

1. Download and extract etcd and etcdctl:

    ```bash
    wget https://github.com/etcd-io/etcd/releases/download/v3.2.26/etcd-v3.2.26-linux-amd64.tar.gz
    tar -xzf etcd-v3.2.26-linux-amd64.tar.gz
    ```

1. Install the etcd and etcdctl binaries:

    ```bash
    mv etcd-v3.2.26-linux-amd64/etcd /usr/bin/etcd
    mv etcd-v3.2.26-linux-amd64/etcdctl /usr/bin/etcdctl
    ```

1. Remove leftover resources:

    ```bash
    rm -rf etcd-v3.2.26-linux-amd64 etcd-v3.2.26-linux-amd64.tar.gz
    ```

1. Start etcd:

    ```bash
    etcd --listen-client-urls http://0.0.0.0:2379 --advertise-client-urls http://localhost:2379 &> /etc/kubernetes/etcd.log &
    ```

1. See if the database is healthy with etcdctl:

    ```bash
    etcdctl cluster-health
    ```

1. Try to get any resources from the kube:

    ```bash
    kubectl get all --all-namespaces
    ```

## Set up kube-apiserver

The next steps will get the kube's API working and show it in action.

1. Start kube-apiserver:

    ```bash
    kube-apiserver --etcd-servers=http://localhost:2379 --service-cluster-ip-range=10.0.0.0/16 --bind-address=0.0.0.0 --insecure-bind-address=0.0.0.0 &> /etc/kubernetes/apiserver.log &
    ```

1. Check its status and initial logs:

    ```bash
    ps -au | grep apiserver
    head /etc/kubernetes/apiserver.log
    ```

1. Hit an API endpoint to see kube-apiserver respond:

    ```bash
    curl http://localhost:8080/api/v1/nodes
    ```

## Set up a kubeconfig File for kubectl

The next steps will allow kubectl to be properly configured.

1. Check to see that kubectl sees the API server:

    ```bash
    kubectl cluster-info
    ```

1. Add the API server address to a kubeconfig file:

    ```bash
    kubectl config set-cluster kube-from-scratch --server=http://localhost:8080
    kubectl config view
    ```

1. Create a context for kubectl which will point to that apiserver:

    ```bash
    kubectl config set-context kube-from-scratch --cluster=kube-from-scratch
    kubectl config view
    ```

1. Use the context created earlier for kubectl:

    ```bash
    kubectl config use-context kube-from-scratch
    kubectl config view
    ```

1. check that resources can now be seen on the cluster:

    ```bash
    kubectl get all --all-namespaces
    kubectl get no
    ```

## Set up the New Config for kubelet

The next steps will take the configuration created and use it to configure kubelet.

1. Restart kubelet with a new flag pointing it to the apiserver (this step may fail once or twice, try again):

    ```bash
    pkill -f kubelet
    kubelet --register-node --kubeconfig=".kube/config" &> /etc/kubernetes/kubelet.log &
    ```

1. Check its status and initial logs:

    ```bash
    ps -au | grep kubelet
    head /etc/kubernetes/kubelet.log
    ```
  
1. Check to see that kubelet has registered as a node:

    ```bash
    kubectl get no
    ```

1. Check to see the old Pod is not coming up:

    ```bash
    docker ps
    ```

1. Check that the Pod manifest is still present:

    ```bash
    ls /etc/kubernetes/manifests
    ```

1. Create a new Pod using kubectl, to test control plane components as they are set up:

    ```bash
    cat <<EOF > ./kube-test.yaml
    ```

    ```yaml
    apiVersion: v1
    kind: Pod
    metadata:
      name: kube-test
      labels:
        app: kube-test
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - name:  http
          containerPort: 80
          protocol: TCP
    ```

    ```bash
    EOF
    kubectl create -f kube-test.yaml
    ```

1. Check the Pod's status:

    ```bash
    kubectl get po
    ```

## Set up kube-scheduler

The next steps will allow Pods to schedule on the kube.

1. Start the scheduler:

    ```bash
    kube-scheduler --master=http://localhost:8080/ &> /etc/kubernetes/scheduler.log &
    ```

1. Check its status and initial logs:

    ```bash
    ps -au | grep scheduler
    head /etc/kubernetes/scheduler.log
    ```

1. Check to see if the Pod was scheduled:

    ```bash
    kubectl get po
    ```

1. Delete the Pod:

    ```bash
    kubectl delete po --all
    ```

## Set up kube-controller-manager

The next steps will set up a controller-manager for state-enforcment of various things in the kube.

1. Create a Deployment:

    ```bash
    cat <<EOF > ./replica-test.yaml
    ```

    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: replica-test
    spec:
      replicas: 3
      selector:
        matchLabels:
          app: replica-test
      template:
        metadata:
          name: replica-test
          labels:
            app: replica-test
        spec:
          containers:
          - name: nginx
            image: nginx
            ports:
            - name:  http
              containerPort: 80
              protocol: TCP
    ```

    ```bash
    EOF
    kubectl create -f replica-test.yaml
    ```

1. Check the Deployment's status:

    ```bash
    kubectl get deploy
    ```

1. Check that no Pods are `Pending` for this Deployment:

    ```bash
    kubectl get po
    ```

1. Start the controller-manager:

    ```bash
    kube-controller-manager --master=http://localhost:8080 &> /etc/kubernetes/controller-manager.log &
    ```

1. Check its status and initial logs:

    ```bash
    ps -au | grep controller
    head /etc/kubernetes/controller-manager.log
    ```

1. Check the status of the Deployment:

    ```bash
    kubectl get deploy
    ```

1. Resume and check the rollout of the Deployment, if the number of `AVAILABLE` Pods still does not change:

    ```bash
    kubectl rollout resume deploy/replica-test
    kubectl rollout status deploy/replica-test
    ```

1. Check the new Pods:

    ```bash
    kubectl get po
    ```

## Set up kube-proxy

The next steps will allow the Deployment to communicate outside of the Docker network in a K8s-compliant manner.

1. Create a Service for the `replica-test` Deployment:

    ```bash
    cat <<EOF > ./service-test.yaml
    ```

    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: replica-test
    spec:
      type: ClusterIP
      ports:
      - name: http
        port: 80
      selector:
        app: replica-test
    ```

    ```bash
    EOF
    kubectl create -f service-test.yaml
    ```

1. Curl the service to see if any Pod is contacted:

    ```bash
    kubectl get svc
    curl {CLUSTER IP}:80
    ```

1. Start kube-proxy:

    ```bash
    kube-proxy --master=http://localhost:8080/ &> /etc/kubernetes/proxy.log &
    ```

1. Check its status and initial logs:

    ```bash
    ps -au | grep proxy
    head /etc/kubernetes/proxy.log
    ```

1. Curl the Service again to see if any Pod is contacted:

    ```bash
    kubectl get svc
    curl {CLUSTER IP}:80
    ```

---

# Conclusion

The next steps will clean up any resources used or created by this lab (optional).

1. Exit out of the VM:

    ```bash
    exit
    exit
    ```

1. Stop Vagrant:

    ```bash
    vagrant halt
    ```

1. To remove all traces of the VM (optional):

    ```bash
    vagrant destroy
    vagrant box remove ubuntu/xenial64
    ```

1. To remove all traces of the lab (if the VM was removed) (optional):

    ```bash
    cd ..
    rm -rf super-u-kube
    ```

This concludes the lab for _Kubernetes Training: How to Deploy a Cluster from Scratch_.

---

