# Module02: Kubernetesにアプリケーションをデプロイする

<!-- TOC -->
- [Module02: Kubernetesにアプリケーションをデプロイする](#module02-kubernetes%E3%81%AB%E3%82%A2%E3%83%97%E3%83%AA%E3%82%B1%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E3%82%92%E3%83%87%E3%83%97%E3%83%AD%E3%82%A4%E3%81%99%E3%82%8B)
  - [Storageリソースの作成](#storage%E3%83%AA%E3%82%BD%E3%83%BC%E3%82%B9%E3%81%AE%E4%BD%9C%E6%88%90)
  - [Secretリソースの作成](#secret%E3%83%AA%E3%82%BD%E3%83%BC%E3%82%B9%E3%81%AE%E4%BD%9C%E6%88%90)
    - [[参考] 作成されたSecretリソースの機密情報の確認](#%E5%8F%82%E8%80%83-%E4%BD%9C%E6%88%90%E3%81%95%E3%82%8C%E3%81%9Fsecret%E3%83%AA%E3%82%BD%E3%83%BC%E3%82%B9%E3%81%AE%E6%A9%9F%E5%AF%86%E6%83%85%E5%A0%B1%E3%81%AE%E7%A2%BA%E8%AA%8D)
  - [Deploymentの作成](#deployment%E3%81%AE%E4%BD%9C%E6%88%90)
  - [Serviceの作成](#service%E3%81%AE%E4%BD%9C%E6%88%90)


次のコマンドでGithubレポジトリをCloneしてから、そのディレクトリに移動する
```sh
git clone https://github.com/yokawasa/azure-voting-app.git
cd azure-voting-app
```

## Storageリソースの作成
```sh
kubectl apply -f kubernetes-manifests/storage-resources.yaml
```
>出力結果
```
storageclass.storage.k8s.io/slow created
persistentvolumeclaim/mysql-pv-claim created
```

次のコマンドでPVCリソース情報を取得して、作成した`mysql-pv-claim` PVCオブジェクトのステータスが`Bound`であることを確認する
```
kubectl get pvc
```
> 出力結果
```
NAME             STATUS    VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
mysql-pv-claim   Bound     pvc-347c7f87-9117-11e8-be5c-0267c07f8713   1Gi        RWO            default        1m
```

## Secretリソースの作成
次のコマンドでSecretリソースを作成する。機密情報などに対して別途Secretリソースを作成し、環境変数として参照させることが推奨されている
```
$ kubectl apply -f kubernetes-manifests/pod-secrets.yaml

secret/azure-vote created
```

### [参考] 作成されたSecretリソースの機密情報の確認

登録されているSecret の一覧を取得
```sh
kubectl get secrets
```
> 出力結果
```
NAME                  TYPE                                  DATA      AGE
azure-vote            Opaque                                5         30s
default-token-bgsqd   kubernetes.io/service-account-token   3         36m
```

Secretリソース`azure-vote`の情報取得

```sh 
kubectl get secrets azure-vote -o yaml
```
> 出力結果
```
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
> オプション`-o yaml`でYAMLフォーマットで出力
> SecretにはKey/Valueペアで値が格納されていて、各値はbase64でエンコードされている必要がある（参考: [kubenetes.io - Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)）

Secretの各値はbase64でエンコードされているため中身をbase64デコードして確認する（例: MYSQL_PASSWORD）
```sh
echo "UGFzc3dvcmQxMg==" | base64 --decode
```
> 出力結果
```
Password12
```

## Deploymentの作成
次のコマンドでDeploymentを作成する
```
kubectl apply -f kubernetes-manifests/azure-vote-deployment.yaml
```
> 出力結果
```
deployment.apps/azure-vote-back created
deployment.apps/azure-vote-front created
```

作成されたPodの一覧を取得してPodステータスが`Running`となっていることを確認する

```sh
kubectl get pod -w
```
> 出力結果
```
NAME                                READY     STATUS              RESTARTS   AGE
azure-vote-back-75b9bbc874-8wx6p    0/1       ContainerCreating   0          1m
azure-vote-front-86694fdcb4-5jjsm   0/1       ContainerCreating   0          1m
azure-vote-front-86694fdcb4-t6pg6   0/1       ContainerCreating   0          1m
azure-vote-back-75b9bbc874-8wx6p   1/1       Running   0         1m
azure-vote-front-86694fdcb4-5jjsm   1/1       Running   0         2m
azure-vote-front-86694fdcb4-t6pg6   1/1       Running   0         2m
```
> オプション`-w`でPodの情報を監視続け変化があったPodの情報が出力される

作成されたDeploymentの一覧を取得して`DESIRED`の数と`AVAILABLE`の数が一致していることを確認する
```sh
kubectl get deploy
```
> 出力結果
```
NAME               DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
azure-vote-back    1         1         1            1           2m
azure-vote-front   2         2         2            2           2m
```

## Serviceの作成
次のコマンドでServiceを作成する
```sh
kubectl apply -f kubernetes-manifests/services.yaml
```
> 出力結果
```
service/azure-vote-back created
service/azure-vote-front created
```

作成されたServiceの一覧を取得する。`azure-vote-front`に`EXTERNAL-IP`が付与されるまで待つ

```sh
kubectl get svc -w
```
> 出力結果
```
NAME               TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
azure-vote-back    ClusterIP      10.0.127.62    <none>        3306/TCP       36s
azure-vote-front   LoadBalancer   10.0.188.136   <pending>     80:32156/TCP   36s
kubernetes         ClusterIP      10.0.0.1       <none>        443/TCP        46m
azure-vote-front   LoadBalancer   10.0.188.136   13.77.158.144   80:32156/TCP   3m
```
> オプション`-w`でPodの情報を監視続け変化があったPodの情報が出力される


作成されたServiceに`EXTERNAL-IP`経由でアクセスする。
```
curl 13.77.158.144    << 上記コマンドで取得したEXTERNAL-IPを指定
```

参考までに、`EXTERNAL-IP`は次のように`-o jsonpath`オプションでを抜き出すことも可能
```
EXTERNALIP=$(kubectl get svc azure-vote-front -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
echo $EXTERNALIP
```

![](../img/browse-app.png)

---
[Top](toc_ja.md) | [Back](module01_ja.md) | Next
