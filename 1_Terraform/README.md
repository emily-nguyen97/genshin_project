# Setting up


## Download the latest version
THIS IS FOR LINUX, JUST LINK TO GENERAL DOWNLOAD PAGE
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

# How to execute

```shell
# Refresh service-account's auth-token
gcloud auth application-default login

terraform init
terraform plan -var="project=<gcp-project-id>"
terraform apply -var="project=<gcp-project-id>"
```

```shell
# Delete infra to avoid costs on any running services
terraform destroy
```