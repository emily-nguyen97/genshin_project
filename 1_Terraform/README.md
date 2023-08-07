### Setting up

'''shell
# Download the latest version
wget https://releases.hashicorp.com/terraform/1.5.4/terraform_1.5.4_linux_amd64.zip

# Unzip the file
unzip terraform_1.5.4_linux_amd64.zip

# Move the executable into a directory for executables
sudo mv terraform /usr/local/bin/
'''

### Things to personally check

'''shell
# Check if these commands need to be run at any point
chmod +x terraform
export PATH=$PATH:~/terraform
'''