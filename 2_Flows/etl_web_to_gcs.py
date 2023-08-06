from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket

@task(retries=3)
def fetch(dataset_url):
    '''Read data from web into pandas DataFrame'''
    df = pd.DataFrame(pd.read_html(url)[0])
    return df

@task(log_prints=True)
def clean(df):
    '''Drop irrelevant columns'''
    df.dropna(axis=1,inplace=True)
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df

@task()
def write_local(df, dataset_file):
    '''Write DataFrame locally as a parquet file'''
    path = Path(f"0_Data/{dataset_file}.parquet")
    df.to_parquet(path, compression='gzip')
    return path

@task()
def write_gc(path):
    gcs_block = GcsBucket.load('')

    url = 'https://genshin-impact.fandom.com/wiki/Character/List'
