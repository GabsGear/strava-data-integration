import glob
import pandas as pd

CSV_FILES_PATH = "../data/*.csv"
PARQUET_FILES_PATH = "../data/parquet_files/"


def get_csv_files(path):
    return glob.glob(path)


def convert_file_to_parquet(file_path, output_path):
    parquet_file = output_path
    file_df = pd.read_csv(file_path)
    file_df.to_parquet(parquet_file)


def get_file_name_from_file_path(file_path):
    return file_path.split(".")[5]


files = get_csv_files(CSV_FILES_PATH)

for file in files:
    convert_file_to_parquet(
        file,
        output_path=f"{PARQUET_FILES_PATH}{get_file_name_from_file_path(file)}.parquet",
    )
