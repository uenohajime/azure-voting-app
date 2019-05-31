# Module01: Create Azure Kubernetes Service (AKS) Cluster

## 1. Create Resource Group
```sh
az group create -g user_akstest -l japaneast
```

## 2. Create AKS Cluster
```sh
az aks create -g user_akstest \
    -n userakscluster \
    -c 3 \
    -k 1.12.7 \
    --enable-addons http_application_routing \
    --generate-ssh-keys
```
>- This tutorial assumes that you create the AKS cluster named `user-akscluster` (node count `3`, Kubernetes cluster version `1.12.7`) under the resource group named `user-akstest`
>- If you already have a ssh key generated and you want to use it instead of generating new key, specify your SSH key with `--ssh-key-value` option instead of `--generate-ssh-keys` in creating AKS Cluster. Please see azure CLI command reference for az aks create for more details

Run the following command to configure kubectl to connect to your Kubernetes cluster, run the following command:
```
az aks get-credentials -g user-akstest -n user-akscluster
```

Finally, check if you can connect to the cluster by running the following command:

```sh
kubectl get nodes
```
> output
```
NAME                       STATUS    ROLES     AGE       VERSION
aks-nodepool1-40291275-0   Ready    agent   2m55s   v1.12.7
aks-nodepool1-40291275-1   Ready    agent   2m48s   v1.12.7
aks-nodepool1-40291275-2   Ready    agent   2m53s   v1.12.7
```

---
[Top](toc.md) | [Back](module00.md) | [Next](module02.md)