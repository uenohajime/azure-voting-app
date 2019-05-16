# Module01: Azure Kubernetes Service (AKS) クラスタの作成

## 1. リソースグループを作成
```sh
az group create -g user_akstest -l japaneast
```

## 2. AKSクラスタを作成

AKSクラスタの作成
```sh
az aks create -g user_akstest \
    -n userakscluster \
    -c 3 \
    -k 1.12.7 \
    --enable-addons http_application_routing \
    --generate-ssh-keys
```
> - このチュートリアルではグループリソース名`user-akstest`の元に AKSクラスタ`user-akscluster` (ノード数 `3`、Kubernetesバージョン`1.12.5`)を作成すると仮定している
> - 新規でSSH鍵を作成するのではなく、もし既存のSSH鍵があって、それを利用したい場合は、AKSクラスタ作成時に`--generate-ssh-keys`オプションを指定するのはなく`--ssh-key-value`オプションに自分のSSH鍵を指定ください


次のコマンドを実行してKugernetesクラスタアクセスのための資格情報を取得
```sh
az aks get-credentials -g user_akstest -n userakscluster
```

次のコマンドでクラスタにアクセスしてノードを取得する
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
[Top](toc_ja.md) | [Back](module00_ja.md) | [Next](module02_ja.md)
