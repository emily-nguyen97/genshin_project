# Setting up


## Download the latest version
'''bash
wget https://releases.hashicorp.com/terraform/1.5.4/terraform_1.5.4_linux_amd64.zip
'''

## Unzip the file
'''bash
unzip terraform_1.5.4_linux_amd64.zip
'''

## Move the executable into a directory for executables
'''bash
sudo mv terraform /usr/local/bin/
'''

# Things to personally check

## Check if these commands need to be run at any point
'''bash
chmod +x terraform
export PATH=$PATH:~/terraform
'''