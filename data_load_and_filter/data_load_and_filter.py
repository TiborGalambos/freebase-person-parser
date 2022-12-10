import os.path
import shutil
import findspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType

from settings import open_this_file


def filter_dataframe(dataframe):
    people_ids = dataframe.filter((dataframe.context == '<http://rdf.freebase.com/ns/people.person>') &
                                  (dataframe.type == '<http://rdf.freebase.com/ns/type.object.type>'))
    people_with_name = dataframe.filter(dataframe.type == '<http://rdf.freebase.com/ns/type.object.name>')
    people_with_birth = dataframe.filter(dataframe.type == '<http://rdf.freebase.com/ns/people.person.date_of_birth>')

    rows_with_needed_data = dataframe.filter((dataframe.context == '<http://rdf.freebase.com/ns/people.person>') |
                                             (dataframe.type == '<http://rdf.freebase.com/ns/type.object.name>') |
                                             (dataframe.type == '<http://rdf.freebase.com/ns/people.person.date_of_birth>') |
                                             (dataframe.type == '<http://rdf.freebase.com/ns/people.deceased_person.date_of_death>'))

    only_people = rows_with_needed_data \
        .join(people_ids, rows_with_needed_data.object_id == people_ids.object_id, 'leftsemi')
    only_people_with_name = only_people \
        .join(people_with_name, only_people.object_id == people_with_name.object_id, 'leftsemi')
    final_raw_dataframe = only_people_with_name \
        .join(people_with_birth, only_people_with_name.object_id == people_with_birth.object_id, 'leftsemi')

    return final_raw_dataframe


def clear_directory_for_parquet():
    if not os.path.exists("/usr/src/data"):
        os.mkdir("/usr/src/data")
        print('new directory created')
    if os.path.exists("/usr/src/data/data"):
        shutil.rmtree('/usr/src/data/data')
        print('old directory deleted')


if __name__ == '__main__':

    findspark.init()
    spark = SparkSession.builder.master("local[4]").appName('test').getOrCreate()

    spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
    spark.conf.set("spark.sql.execution.arrow.enabled", "true")

    sc = spark.sparkContext
    sc.setLogLevel("ERROR")

    print(spark)

    freebaseSchema = StructType([
        StructField('object_id', StringType(), True),
        StructField('type', StringType(), True),
        StructField('context', StringType(), True),
        StructField('dot', StringType(), True)
    ])

    df = spark.read.options(delimiter='\t').schema(freebaseSchema).csv(open_this_file)
    print("read completed")

    final_raw_dataframe = filter_dataframe(df)
    print("filter completed")

    final_raw_dataframe.write.mode('overwrite').parquet('/user/root/data')
    print('write completed')

    clear_directory_for_parquet()

    # after script run:
    # hadoop fs -get /user/root/data /usr/src/data

    exit(0)
