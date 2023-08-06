from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials

@task(retries=3)
def extract_from_gcs():
    '''Download genshin data from GCS'''
    gcs_path = f'0_Data/char_data.parquet'
    gcs_youtube_path = f'0_Data/genshin_data_V3_7.csv'

    gcs_block = GcsBucket.load('genshin-gcs')
    gcs_block.get_directory(from_path=gcs_path, local_path=f'../0_Data/')
    gcs_block.get_directory(from_path=gcs_youtube_path, local_path=f'../0_Data/')

    return Path(f'../0_Data/{gcs_path}'), Path(f'../0_Data/{gcs_youtube_path}')

@task()
def transform(path):
    '''Clean data a little '''
    df = pd.read_parquet(path)
    print(f'Split Model Type into two columns: Size and Gender')
    print(f'Pre: example data')
    print(df.head(2))
    df['Size'] = df['Model Type'].str.split(' ').str[0]
    df['Gender'] = df['Model Type'].str.split(' ').str[1]
    df.drop('Model Type', axis=1, inplace=True)
    print(f'Post: example data')
    print(df.head(2))
    return df

@task()
def write_bq(df,dest_table):
    '''Write DataFrame to BigQuery'''
    gcp_credentials_block = GcpCredentials.load('genshin-gcp-creds')

    df.to_gbq(
        destination_table=dest_table,
        project_id='dtc-de-course-381518',
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=1_000,
        if_exists='append'
    )

@flow()
def etl_gcs_to_bq():
    '''Main ETL flow to load data into BigQuery'''
    path, youtube_path = extract_from_gcs()

    df = transform(path)
    df_youtube = pd.read_csv(youtube_path)

    write_bq(df, 'genshin.chars')
    write_bq(df_youtube, 'genshin.playstyles')

if __name__ == '__main__':
    etl_gcs_to_bq()