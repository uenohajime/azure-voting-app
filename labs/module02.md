# Module02: Deploy the application to AKS Cluster

Clone the Github repo via the command line, and change directory:

```sh
git clone https://github.com/yokawasa/azure-voting-app.git
cd azure-voting-app
```

## Create Storage Resource
```sh
kubectl apply -f kubernetes-manifests/storage-resources.yaml
```
> output
```
storageclass.storage.k8s.io/slow created
persistentvolumeclaim/mysql-pv-claim created
```

Get PVC info list with the following command and confirm that `mysql-pv-claim` PVC resource's status is `Bound`
```sh
kubectl get pvc
```
> output
```
NAME             STATUS    VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
mysql-pv-claim   Bound     pvc-347c7f87-9117-11e8-be5c-0267c07f8713   1Gi        RWO            default        1m
```

## Create Secret Resource

Create Secret resource with the following command
```sh
kubectl apply -f kubernetes-manifests/pod-secrets.yaml
```
> output
```
secret/azure-vote created
```

### [NOTE] How to check secret info in your Secret resource

Get Secret list with the following command
```sh
kubectl get secrets
```
> output
```
NAME                  TYPE                                  DATA      AGE
azure-vote            Opaque                                5         30s
default-token-bgsqd   kubernetes.io/service-account-token   3         36m
```

Get the detail of Secret resource `azure-vote`

```sh 
kubectl get secrets azure-vote -o yaml
```
> output
```yaml
apiVersion: v1
data:
  MYSQL_DATABASE: YXp1cmV2b3Rl
  MYSQL_HOST: YXp1cmUtdm90ZS1iYWNr
  MYSQL_PASSWORD: UGFzc3dvcmQxMg==
  MYSQL_ROOT_PASSWORD: UGFzc3dvcmQxMg==
  MYSQL_USER: ZGJ1c2Vy
kind: Secret
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"v1","data":{"MYSQL_DATABASE":"YXp1cmV2b3Rl","MYSQL_HOST":"YXp1cmUtdm90ZS1iYWNr","MYSQL_PASSWORD":"UGFzc3dvcmQxMg==","MYSQL_ROOT_PASSWORD":"UGFzc3dvcmQxMg==","MYSQL_USER":"ZGJ1c2Vy"},"kind":"Secret","metadata":{"annotations":{},"name":"azure-vote","namespace":"default"},"type":"Opaque"}
  creationTimestamp: 2018-07-26T21:05:59Z
  name: azure-vote
  namespace: default
  resourceVersion: "3627"
  selfLink: /api/v1/namespaces/default/secrets/azure-vote
  uid: b2660f6b-9117-11e8-be5c-0267c07f8713
type: Opaque
```
> Get the output in YAML format with `-o yaml` option
> Secret info is store as Key/Value pair, and each secret value needs to be base64 encoded（For the detail, see [kubenetes.io - Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)）

As each Secret value is base64 encoded, it needs to be base64 decoded to look up its context (ie. MYSQL_PASSWORD）
```sh
echo "UGFzc3dvcmQxMg==" | base64 --decode
```
> output
```
Password12
```

## Create Deployment
Create Deployment resource with the following command
```sh
kubectl apply -f kubernetes-manifests/azure-vote-deployment.yaml
```
> output
```
deployment.apps/azure-vote-back created
deployment.apps/azure-vote-front created
```

Get Pod info list and confirm that all created Pods' status are `Running`

```sh
kubectl get pod -w
```
> output
```
NAME                                READY     STATUS              RESTARTS   AGE
azure-vote-back-75b9bbc874-8wx6p    0/1       ContainerCreating   0          1m
azure-vote-front-86694fdcb4-5jjsm   0/1       ContainerCreating   0          1m
azure-vote-front-86694fdcb4-t6pg6   0/1       ContainerCreating   0          1m
azure-vote-back-75b9bbc874-8wx6p    1/1       Running   0         1m
azure-vote-front-86694fdcb4-5jjsm   1/1       Running   0         2m
azure-vote-front-86694fdcb4-t6pg6   1/1       Running   0         2m
```
> Option `-w` can watch for changes after listing/getting the requested objects

Get Deployment info list and confirm that the number of `DESIRED` and `AVAILABLE` is same.
```sh
$ kubectl get deploy

NAME               DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
azure-vote-back    1         1         1            1           2m
azure-vote-front   2         2         2            2           2m
```

## Create Service

Create Service resource with the following command
```sh
kubectl apply -f kubernetes-manifests/services.yaml
```
> output
```
service/azure-vote-back created
service/azure-vote-front created
```

Get Service info list. Wait until an external IP for `azure-vote-front` is assigned in `EXTERNAL-IP` field

```sh
kubectl get svc -w
```
> output
```
NAME               TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
azure-vote-back    ClusterIP      10.0.127.62    <none>        3306/TCP       36s
azure-vote-front   LoadBalancer   10.0.188.136   <pending>     80:32156/TCP   36s
kubernetes         ClusterIP      10.0.0.1       <none>        443/TCP        46m
azure-vote-front   LoadBalancer   10.0.188.136   13.77.158.144   80:32156/TCP   3m
```
> Option `-w` can watch for changes after listing/getting the requested objects

Access the service with an assigned external IP
```
curl 13.77.158.144    << an assigned external IP
```

NOTE: an external IP can be obtained by using `-o jsonpath` option like this:
```sh
EXTERNALIP=$(kubectl get svc azure-vote-front -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
echo $EXTERNALIP
```

![](../img/browse-app.png)

---
[Top](toc.md) | [Back](module01.md) | [Next](module03.md)