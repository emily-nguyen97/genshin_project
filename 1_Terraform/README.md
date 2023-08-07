# Setting up


## Download the latest version
Download the zip file, unzip, and then move to a directory that is searched for executables
```bash
wget https://releases.hashicorp.com/terraform/1.5.4/terraform_1.5.4_linux_amd64.zip
unzip terraform_1.5.4_linux_amd64.zip
sudo mv terraform /usr/local/bin/
```

# Things to personally check

## Check if these commands need to be run at any point
```bash
chmod +x terraform
export PATH=$PATH:~/terraform
```