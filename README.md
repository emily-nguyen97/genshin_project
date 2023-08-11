# Genshin Impact Project

# Docker

This is how I set it up for WSL. First, I followed the instructions [here](https://docs.docker.com/engine/install/ubuntu/) and [here](https://docs.docker.com/desktop/wsl/). 

# Reproducibility

0.) Start up virtual environment or docker
```shell
conda activate genshin_env
```

1.) Start up Terraform to set up the BigQuery dataset and GCS

2.) Start up Prefect to get the data, store it in GCS, and then move it to BigQuery

3.) Start up dbt Cloud