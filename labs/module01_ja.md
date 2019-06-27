# Module01: Azure Kubernetes Service (AKS) クラスタの作成

<!-- TOC -->
- [Module01: Azure Kubernetes Service (AKS) クラスタの作成](#Module01-Azure-Kubernetes-Service-AKS-%E3%82%AF%E3%83%A9%E3%82%B9%E3%82%BF%E3%81%AE%E4%BD%9C%E6%88%90)
  - [1. リソースグループを作成](#1-%E3%83%AA%E3%82%BD%E3%83%BC%E3%82%B9%E3%82%B0%E3%83%AB%E3%83%BC%E3%83%97%E3%82%92%E4%BD%9C%E6%88%90)
  - [2. AKSクラスタを作成](#2-AKS%E3%82%AF%E3%83%A9%E3%82%B9%E3%82%BF%E3%82%92%E4%BD%9C%E6%88%90)
    - [2-1. AKSクラスタの作成 (管理者アカウントで実行する場合)](#2-1-AKS%E3%82%AF%E3%83%A9%E3%82%B9%E3%82%BF%E3%81%AE%E4%BD%9C%E6%88%90-%E7%AE%A1%E7%90%86%E8%80%85%E3%82%A2%E3%82%AB%E3%82%A6%E3%83%B3%E3%83%88%E3%81%A7%E5%AE%9F%E8%A1%8C%E3%81%99%E3%82%8B%E5%A0%B4%E5%90%88)
    - [2-2. AKSクラスタの作成 (管理者権限のないアカウントで実行する場合)](#2-2-AKS%E3%82%AF%E3%83%A9%E3%82%B9%E3%82%BF%E3%81%AE%E4%BD%9C%E6%88%90-%E7%AE%A1%E7%90%86%E8%80%85%E6%A8%A9%E9%99%90%E3%81%AE%E3%81%AA%E3%81%84%E3%82%A2%E3%82%AB%E3%82%A6%E3%83%B3%E3%83%88%E3%81%A7%E5%AE%9F%E8%A1%8C%E3%81%99%E3%82%8B%E5%A0%B4%E5%90%88)
  - [3. クラスタアクセス用資格情報取得](#3-%E3%82%AF%E3%83%A9%E3%82%B9%E3%82%BF%E3%82%A2%E3%82%AF%E3%82%BB%E3%82%B9%E7%94%A8%E8%B3%87%E6%A0%BC%E6%83%85%E5%A0%B1%E5%8F%96%E5%BE%97)

## 1. リソースグループを作成
```sh
az group create -g user_akstest -l japaneast
```

## 2. AKSクラスタを作成

### 2-1. AKSクラスタの作成 (管理者アカウントで実行する場合)

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

### 2-2. AKSクラスタの作成 (管理者権限のないアカウントで実行する場合)

サービスプリンシパル作成権限（対象アカウントに`Owner/所有者`または`User Access Administrator/ユーザーアクセス管理者`ロールが割り当てられている）をもったアカウント保持者に依頼して次のようにAKSクラスタ作成のためのサービスプリンシパルを作成してもらう
> NOTE: サービスプリンシパルを作成するには、アプリケーションを Azure AD テナントに登録し、サブスクリプション内のロールにアプリケーションを割り当てるためのアクセス許可が必要です。対象アカウントに`Owner/所有者`または`User Access Administrator/ユーザーアクセス管理者`ロールが割り当てられていることをご確認ください。ロールに関する詳細は[こちら](https://docs.microsoft.com/ja-jp/azure/role-based-access-control/rbac-and-directory-admin-roles#azure-rbac-roles)を参照ください
```sh
# az ad sp create-for-rbac --skip-assignment -n <サービスプリンシパル名>
az ad sp create-for-rbac --skip-assignment -n my-aks-sp
```
実行すると次のような結果出力が得られるのでこの出力結果をAKSクラスタを作成する担当者に渡してください。この中で`appId`と`password`がAKSクラスタ作成時に必要になります
```json
{
  "appId": "72155cb8-d08d-4435-9052-4b8e8f7352a9",
  "displayName": "my-aks-sp",
  "name": "http://my-aks-sp",
  "password": "13420a1e-ec5f-4a83-b763-b6f599e88899",
  "tenant": "72f988bf-86f1-41af-91ab-2d7cd011db47"
}
```

次のようにサービスプリンシパル情報を指定してAKSクラスタを作成します
```sh
SP_CLIENT_ID="<上記サービスプリンシパル情報のappID>"
SP_CLIENT_SECRET="<上記サービスプリンシパル情報のpassword>"

az aks create -g user_akstest \
    -n userakscluster \
    -c 3 \
    -k 1.12.7 \
    --enable-addons http_application_routing \
    --service-principal $SP_CLIENT_ID \
    --client-secret $SP_CLIENT_SECRET \
    --generate-ssh-keys
```
> - このチュートリアルではグループリソース名`user-akstest`の元に AKSクラスタ`user-akscluster` (ノード数 `3`、Kubernetesバージョン`1.12.5`)を作成すると仮定している
> - `--service-principal`と`--client-secret`でそれぞれサービスプリンシパルIDとサービスプリンシパルパスワードを指定する
> - 新規でSSH鍵を作成するのではなく、もし既存のSSH鍵があって、それを利用したい場合は、AKSクラスタ作成時に`--generate-ssh-keys`オプションを指定するのはなく`--ssh-key-value`オプションに自分のSSH鍵を指定ください

## 3. クラスタアクセス用資格情報取得

次のコマンドを実行してKugernetesクラスタアクセスのための資格情報を取得
```sh
az aks get-credentials -g user_akstest -n userakscluster
```

次のコマンドでクラスタにアクセスしてノードを取得する
```sh
kubectl get nodes
```
> Output
```
NAME                       STATUS    ROLES     AGE       VERSION
aks-nodepool1-40291275-0   Ready    agent   2m55s   v1.12.7
aks-nodepool1-40291275-1   Ready    agent   2m48s   v1.12.7
aks-nodepool1-40291275-2   Ready    agent   2m53s   v1.12.7
```

---
[Top](toc_ja.md) | [Back](module00_ja.md) | [Next](module02_ja.md)
