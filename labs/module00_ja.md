# Module00: 環境設定

## Azure Cloud Shellを立ち上げる

このハンズオンラボでは[Azure Cloud Shell (Bashモード)](https://docs.microsoft.com/en-us/azure/cloud-shell/overview)を使用して進めます。よって、まず最初にAzure Cloud ShellをBashモードで立ち上げてください

![](../img/cloud-shell-open-bash.png)

>[NOTE]: https://shell.azure.com/ にアクセスすることでフルスクリーンのAzure Cloud Shellを使うことができます

もしAzure Cloud Shellへのアクセスが初めての場合は、次のようなデータ永続化のためのAzure Fileの設定のためのプロンプトが表示されます

![](../img/cloud-shell-welcome.png)

"Bash (Linux)"オプションをクリックして、Azureサブスクリプションを選択して、"Create Storage"をクリックします

![](../img/cloud-shell-no-storage-mounted.png)

数秒後にストレージアカウントが作成されます。これでAzure Cloud Shellを使う準備が整いました。

## Azureサブスクリプションの選択（複数ある場合のみ）

次のコマンドを実行してAzureサブスクリプション一覧を表示します

```
$ az account list -o table

Name                             CloudName    SubscriptionId                        State    IsDefault
-------------------------------  -----------  ------------------------------------  -------  -----------
Visual Studio Premium with MSDN  AzureCloud   xxxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx  Enabled  True
Another sub1                     AzureCloud   xxxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx  Enabled  False
Another sub2                     AzureCloud   xxxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx  Enabled  False
Another sub3                     AzureCloud   xxxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx  Enabled  False
```

もし、複数のサブスクリプションを持っている場合は、次のように利用したいサブスクリプション名をデフォルトに設定ください

```
$ az account set -s 'Visual Studio Premium with MSDN'
```

## Register Azure Resource Providers

このハンズオンラボではAzureのNetwork, Storage, Compute と ContainerSerivcesのリソースを管理しますが、もしお使いのサブスクリプションにおいてこれらリソース管理が初めての場合は次のコマンドを実行してリソースプロバイダーを登録ください

```sh
$ az provider register -n Microsoft.Network
$ az provider register -n Microsoft.Storage
$ az provider register -n Microsoft.Compute
$ az provider register -n Microsoft.ContainerService
```

---
[Top](toc_ja.md) | [Next](module01_ja.md)