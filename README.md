# 2023-HFU-Winter
## 建立虛擬環境
pip install virtualenv
python -m venv 環境的名字

## 開啟虛擬環境
### 先確定VSCODE是不是已經幫你綁定了？
1. 確定CMD前面有沒有括號
2. 用以下指令執行
    * Windows
        * get-command python
        * get-command pip
    * Mac or Unix-like
        * where python
        * where pip

### 若無：Mac or Unix-like
* source 環境的名字/bin/activate
### 若無：Windows
* 環境的名字\Scripts\Activate.ps1
    * 若無法執行出現紅字，可以以系統管理員開啟另一個命令提示字元(PowerShell)，並執行以下指令：
    * Set-ExecutionPolicy Unrestricted -Scope LocalMachine