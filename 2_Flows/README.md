# How to use with Prefect for workflow orchestration

## Execution
```shell
prefect orion start
```

Go to the UI with the link provided by the command that was just ran. Before adding blocks, run
```shell
prefect block register -m prefect_gcp
```

And then go to the API to add blocks. 

Run the code from the highest directory with 
```shell
python 2_flows/etl_web_to_gcs.py
python 2_flows/etl_gcs_to_bq.py
```