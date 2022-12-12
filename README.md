# Could they meet? - Freebase person parser

This is a school project for parsing information about people type objects from Freebase files. Those are naturally 
alive or dead people which has information about themselves in the Freebase data dump. After the parsing we index them
and let the user look up two names and find out whether they could meet based on three metrics: timeline they lived, 
place of birth and palace they lived.

# Freebase data

Freebase uses 3+1 columns in a row per information. 
The RDF data is serialized using the N-Triples format and it is encoded as UTF-8 text.

```
Example of a row/object in Freebase data dump file:

<http://rdf.freebase.com/ns/g.1238xvt1>  <http://rdf.freebase.com/ns/type.object.type>  <http://rdf.freebase.com/ns/people.person>	.
```

### ID
The rows in the file has IDs of the object that are being described, and they are always in the first column. 
An ID looks like this: `g.1238xvt1`. 
### Predicate
The second row contains the predicate. That is the type of data that will be in the third column. 
The predicate can be various. 
In this project we are looking for the following predicates:
```
people.person
type.object.name
people.person.date_of_birth
people.deceased_person.date_of_death
people.person.place_of_birth
people.person.places_lived
```
### Object
The third row contains the object, or the context of the information. In this project we are looking for names, dates, 
object types etc. The last column is just a single dot.

# Prerequisites

It is necessary to download and install few things in order to run the code.\
\
Docker: https://www.docker.com/ \
Docker image: https://hub.docker.com/r/iisas/hadoop-spark-pig-hive \
Freebase dump: https://developers.google.com/freebase \
Visual Studio Code: https://code.visualstudio.com/download \
\
Some VS Code extensions that will be useful: \
https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker \
https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack \

\
After these steps use Visual Studio Code to access the Docker container and copy the code, 
requirements.txt and the freebase data dump in zipped or unzipped format to `/usr/src` directory in the docker.

Run the following scripts in docker:
```
cd /usr/src

sudo apt-get update ;
sudo apt-get install python3-pip ;

pip install --upgrade pip ;
pip3 install -U setuptools_scm==3.0.5 ;

python3 -m pip install --no-cache-dir -r requirements.txt ;

hadoop fs -copyFromLocal /usr/src<freebase_data_dump_name>
```
After these commands please restart your container and open `/data_load_and_filter/settings.py` and set the right path 
to the freebase data dump file and save the edited file. 

Please run the following commands:
```
export PYTHONIOENCODING=utf8 ;
export SPARK_HOME=/usr/local/spark ;
export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH ;
export PATH=$SPARK_HOME/bin:$SPARK_HOME/python:$PATH ;
PYSPARK_PYTHON=python3
```

Now you can run the Python files using the commands below.


## Run with following commands in docker

```
cd /usr/src

spark-submit data_load_and_filter/data_load_and_filter.py ;
hadoop fs -get /user/root/data /usr/src/data ;
spark-submit data_parse_and_index/data_parse_and_index.py ;
python3 ./data_search/data_search.py ;
```


# Code

The code itself is written in Python, and it is divided into three main parts. 
`data_load_and_filter` loads the data to pyspark Dataframe, by the declared schema it finds the columns
and filters out the unnecessary rows. The necessary rows are mentioned in the predicate section above. 
After the filtering, we save the data to apache hadoop filesystem in parquet format and clear the specific 
directory, where these files will be copied from hadoop.

To run the `data_load_and_filter` part use the following command:
```
spark-submit data_load_and_filter/data_load_and_filter.py ;
```

After running this part, it is necessary to run the following command to copy the parquet files into 
your filesystem:

```
hadoop fs -get /user/root/data /usr/src/data
```

The next part is the `data_parse_and_index`, where we first load the parquet files from the filesystem
and create the schema for indexing using Whoosh. After loading the data, we iterate through every row
and by regex we parse the needed data. Based on ID of the rows, we know which information belongs
to one specific person. From the rows of the person we need the name of the and the birthday 
in the first place. If this information was not available, we ignore this person. If we have these two 
information, then we parse the death date, place of birth and place where the person lived if available.
The data is then saved into index.

To run the `data_parse_and_index` part use the following command:
```
spark-submit data_parse_and_index/data_parse_and_index.py ;
```

The `data_search` part loads the index from the filesystem and reads the users input from the console.
The input contains two names which will be looked up. If the people are found, the mentioned 
information about them will be printed to the console. On the other side, if something is not found,
the user will be informed about it via a message.

To run the `data_search` part use the following command:
```
python3 ./data_search/data_search.py
```


# Example outputs

The user writes the names to the console as shown below.

```
search for first name:Dietrich Rusche
search for second name:Margit Schaumäker


Dietrich Rusche
born: 1936-09-13
death: None
birth place id: m.0156q
place lived id: None


Margit Schaumäker
born: 1925-05-12
death: None
birth place id: m.0156q
place lived id: None

YES, they could have met by fetched time
YES, they have the same birthplace
NO, I have no information about one or both persons place they lived
```

Sometimes the dates in Freebase are stored only as years. In that case, the program works with
the first day of the given year. There is an example below where we only know the year 
of the birth and death of Hans Siemens.

```
search for first name:hans
search for second name:julie


Hans Siemens
born: 1818
death: 1867
birth place id: None
place lived id: None


Julie Wiggen
born: 1965-05-23
death: None
birth place id: m.05b4w
place lived id: None

NO, they could not have met by fetched time
NO, I have no information about one or both persons birthplace
NO, I have no information about one or both persons place they lived
```
