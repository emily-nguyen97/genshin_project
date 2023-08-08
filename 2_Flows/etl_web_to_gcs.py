from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket

@task(retries=3)
def fetch(dataset_url):
    '''Read data from web into pandas DataFrame'''
    df = pd.DataFrame(pd.read_html(dataset_url)[0])
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
    path = Path(f'0_Data/{dataset_file}.parquet')
    df.to_parquet(path, compression='gzip')
    return path

@task()
def write_gcs(path):
    gcs_block = GcsBucket.load('genshin-gcs')
    gcs_block.upload_from_path(from_path=path, to_path=path)
    return

@flow()
def etl_web_to_gcs():
    '''Main ETL function'''
    dataset_file = f'char_data'
    dataset_url = f'https://genshin-impact.fandom.com/wiki/Character/List'

    df = fetch(dataset_url)
    df_clean = clean(df)
    path = write_local(df_clean, dataset_file)
    write_gcs(path)

    # Also send Youtube data to gcs
    youtube_path = f'0_Data/genshin_data_V3_7.csv'
    write_gcs(youtube_path)

if __name__ == '__main__':
    etl_web_to_gcs()