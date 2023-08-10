# Genshin Impact Project

# To do

1.) See if I need to add ssh key to GCP in VM instances (under Metadata) --NOT NECESSARY IF I'M GOING TO RUN STUFF ON MY PERSONAL PC

# Docker

This is how I set it up for WSL. First, I followed the instructions here: https://docs.docker.com/engine/install/ubuntu/ and https://docs.docker.com/desktop/wsl/. 


1.) Start up Terraform to set up the BigQuery dataset and GCS
2.) Start up Prefect to get the data, store it in GCS, and then move it to BigQuery