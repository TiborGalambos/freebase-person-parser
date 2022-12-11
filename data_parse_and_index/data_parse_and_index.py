import glob
import os.path
import pandas as pd
import shutil
from whoosh import index
from whoosh.fields import Schema, TEXT
import people_object_extracter
from settings import INDEX_PATH


def load_data_from_parquet():
    parquet_files = glob.glob(os.path.join('/usr/src/data/data', "*.parquet"))
    parq_df = pd.concat((pd.read_parquet(f) for f in parquet_files))
    return parq_df


if __name__ == '__main__':

    # make sure you executed hadoop script after the previous python script
    # hadoop fs -get /user/root/data /usr/src/data

    parq_df = load_data_from_parquet()
    print("data loaded")

    schema = Schema(name=TEXT(stored=True),
                    birthdate=TEXT(stored=True),
                    deathdate=TEXT(stored=True),
                    birthplace=TEXT(stored=True),
                    placelived=TEXT(stored=True))

    if os.path.exists(INDEX_PATH):
        print('removing old index files')
        shutil.rmtree(INDEX_PATH)

    if not os.path.exists(INDEX_PATH):
        print('creating index files')
        os.mkdir(INDEX_PATH)
        ix = index.create_in(INDEX_PATH, schema)
        writer = ix.writer()
        people_object_extracter.get_people_objects(writer, parq_df)
        writer.commit()
        print('index files created')

    exit(0)
