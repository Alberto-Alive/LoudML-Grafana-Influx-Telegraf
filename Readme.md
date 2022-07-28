# LoudML-Grafana-Influx-Telegraf

As of 21.06.2022 : updated by Alberto, any queries email me `alberto-alive@outlook.com`
Watch this YouTube tutorial: https://www.youtube.com/watch?v=A2-GN5T52rs

This tutorial is for InfluxDB version 1.x. 
LoudML supports InfluxDB version 1.x and 2.x. LoudML also supports Grafana version 8.x.
For your project you only need to get the docker-compose file and LoudMLData folder, and modify it to suit your requirements.


## Stage I ENVIRONMENT

- Windows 10 Enterprise version 21H2
- Docker version 20.10.13, build a224086
- Influx version 1.8.10
- Telegraf version 1.22.4
- Grafana version 7.5.8
- LoudML version 1.7.2


## Stage II WINDOWS-DOCKER SETUP

`WINDOWS`
1. Enable HYPER-V in windows features: https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/quick-start/enable-hyper-v
2. Install WSL2: https://www.omgubuntu.co.uk/how-to-install-wsl2-on-windows-10

Visualise:
![image](https://user-images.githubusercontent.com/63293696/172639073-ed240188-bd36-4c24-a096-9ef1b94d0261.png)

`Docker`

Visualise:
![image](https://user-images.githubusercontent.com/63293696/172639961-ab026550-c581-46d8-9e9a-e60db502d3f6.png)

Run docker-compose command:
```bat 
docker-compose up
```

## Stage III DOCKER-COMPOSE.YML FILE
1. Create a file called 'docker-compose.yml' using below structure:

```yaml
# This is a Docker Compose file to work with Loud ML and an InfluxDB stack.
version: "3.6"
services:
    loudml:
    influxdb:
    telegraf:
    grafana:
volumes:
```
2. Service loudml:

```yaml
  loudml:
    image: loudml/loudml:addVersionExample1.6.0
    container_name: addName 
    restart: always 
    volumes: 
      - addYourPcPathToConfigFile/loudml/config.yml:/etc/loudml/config.yml:ro 
      - var_loudml:map/to/some/folder/in/loudml/container
    environment: 
      influx: http://addParameterThatIsExactlyTheServiceNameOfInfluxDBFoundInDockerComposeFile:addDockerPortOfInfluxDBServiceFoundInDockerComposeFile
      influx_database: addNameForADatabaseToBeCreatedOnInfluxDB 
    ports:
      - "addPortToBeOpenedOnYourNetworkDefault8077:addPortToBeOpenedOnDockerNetworkDefault8077" 
    depends_on:
      - addNameOfTheInfluxDBServiceFoundInDockerComposeFile
```
3. Service influx:

```yaml
influx:
    image: influxdb:addVersionExample1.8.10 
    container_name: addName
    restart: always
    environment:
      - INFLUX_USERNAME=addUserName 
      - INFLUX_PASSWORD=addPassword
      - INFLUXDB_HTTP_SHARED_SECRET=addToken
    ports:
      - "addPortToBeOpenedOnYourNetworkDefaul8086:addPortToBeOpenedOnDockerNetworkDefault8086"
    volumes:
      - addYourPcPathToConfigFile/influxdb/config/influxdb.conf:/var/lib/influxdb/influxdb.conf 
      - addYourPcPathToDataFolder/influxdb/data:/var/lib/influxdb/data
      - var_influxdb:map/to/some/folder/in/influxdb/container
```
4. Service telegraf:

```yaml
  telegraf:
    image: telegraf:addVersionExample1.22.4
    container_name: addName
    restart: always
    volumes:
      - "addYourPcPathToConfigFile/telegraf/telegraf.conf:/etc/telegraf/telegraf.conf:ro" 
    depends_on:
      - influxdb
    links: 
      - "influxdb:addAlternativeNameToAccessInfluxdbBy"
```
5. Service grafana:

```yaml
 grafana:
    image: grafana/grafana-enterprise:addVersion
    container_name: addName
    restart: always
    ports:
      - addPortToBeOpenedOnYourNetworkDefaul3000:addPortToBeOpenedOnDockerNetworkDefault3000
    user: '104'
    environment:
    - GF_INSTALL_PLUGINS=addPluginUrlExample>>http://www.github.com/vsergeyev/loudml-grafana-app/blob/master/loudml-grafana-app-1.7.2.zip?raw=true;loudml-grafana-app
    volumes:
      - addYourPcPathToConfigFile/grafana/grafana.ini:/etc/grafana/grafana.ini:rw 
      - var_grafana:map/to/some/folder/in/grafana/container
    depends_on:
      - influxdb
    links: 
      - "influxdb:addAlternativeNameToAccessInfluxdbBy"
```
6. Volumes:

```yaml
volumes:
  var_loudml:
    external: if-set-to-FALSE-docker-compose-will-create-the-volumes
  var_influxdb:
    external: if-set-to-TRUE-docker-compose-will-check-for-external-volumes-already-created
  var_grafana:
    external: false
```

Stage IV GRAFANA SETUP

LogOn using default username == password: admin
1. Allow grafana to use unsigned plugins, to be able to use LoudML, by adding this line into grafana.ini, and then enable it.

```ini
[plugins]
allow_loading_unsigned_plugins = true
```
- Enable LoudML plugin: Grafana >> Configuration >> Plugins >> LoudML >> Config >> Click 'Enable' button. Reminder: ensure StageIV-Step1 is complete!
2. Setup Influx datasource : data to apply machine learning algorithm on!

- Query Language : InfluxQL

- HTTP
  - URL : http://influxdb:8086 (http://`<nameOfInfluxServiceInDockerComposeFile>:<numberOfPortInfluxServiceOnDockerComposeFile>`)
  - Access: Server(Default)

- Custom HTTP Headers
  - Header: Authorization Value: Token addNameOfYourTokenFromInfluxDB (Leave a space between 'Token' and 'yourActualToken')

- InfluxDB Details
  - Database: _internal (Add any database/bucket you have created on Influx; '_internal' is the default database created by InfluxV1)
  - Username: admin (The username for Influx service defined in docker-compose file or influxdb.conf file)
  - Password: admin (The password for Influx service defined in docker-compose file or influxdb.conf file) || addNameOfYourTokenFromInfluxDB (The token you have           specified in docker-compose.yml file >> influxdb >> INFLUXDB_HTTP_SHARED_SECRET=WhateverToken! which is also specified in influxdb.conf >> [http] >> shared-secret     = "WhateverToken!"
  - HTTP Method: GET
  
  Click 'Save and Test' >> If it works, a green label pops up: Data source is working. >>If it doesn't work, most likely you have some other authentication method checked or/and your url doesn't have the service name of influxdb specified in docker-compose as it's domain name.
  
3. Setup Influx datasource : database where predictions will be stored

- Query Language : InfluxQL

- HTTP
  - URL : http://influxdb:8086 (http://`<nameOfInfluxServiceInDockerComposeFile>:<numberOfPortInfluxServiceOnDockerComposeFile>`)
  - Access: Server(Default)

- Custom HTTP Headers
  - Header: Authorization Value: Token addNameOfYourTokenFromInfluxDB (Leave a space between 'Token' and 'yourActualToken')

- InfluxDB Details
  - Database: _internal (Add any database/bucket you have created on Influx; '_internal' is the default database created by InfluxV1)
  - Username: admin (The username for Influx service defined in docker-compose file or influxdb.conf file)
  - Password: admin (The password for Influx service defined in docker-compose file or influxdb.conf file) || addNameOfYourTokenFromInfluxDB (The token you have           specified in docker-compose.yml file >> influxdb >> INFLUXDB_HTTP_SHARED_SECRET=WhateverToken! which is also specified in influxdb.conf >> [http] >> shared-secret     = "WhateverToken!"
  - HTTP Method: GET
  
  Click 'Save and Test' >> If it works, a green label pops up: Data source is working. >>If it doesn't work, most likely you have some other authentication method       checked or/and your url doesn't have the service name of influxdb specified in docker-compose as it's domain name.


4. Setup LoudML datasource
- HTTP
  - Loud ML Server URL : http://loudml:8077 (http://`<nameOfLoudMLServiceInDockerComposeFile>:<numberOfPortLoudMLServiceOnDockerComposeFile>`)
  - Access : Server (Default)
Click 'Save and Test'>> If it works, a green label pops up: Data source is working. >>If it doesn't work, most likely your loudml.yml file is not set up correctly since it is the only thing that you have to adapt to your use case.

5. Setup Model on LoudML
    - Name : addAnyName
    - Model type : donut
    - Bucket : readYourData (this is the bucket name specified in the loudml.yml for the influx database from where you get your data to apply the ML model on : if you see the example provided here note that the first bucket on the buckets list is for the database from where you get the data to train you model, whereas, the second bucket on the lsit is where the trained data goes based on which your predictions are made)
    - Max training hyper-params iterantions : 10 (number of variable parameters)
    - GroupedBy bucket interval : 5s (setting the interval to 1s for the model - I believe - should be the same or close to the one set on the telegraf (5s in our case - in telegraf.conf) for querying the data to influxdb)
    - Span : 100 (number of training iterations (100 times 5s over 60 = approx 8mins to train), adjust as you need but you should need more than 100 to train your model)

    - Feature
      - Name : addAnyName
      - Measurement : cpu  (add the value you inserted in the 'select measurement' field in the dashboard)
      - Field : usage_user (add the value inserted in the 'field' field in the dashboard)
      - Metric : mean (collects the mean values)
      - Default : 0 (when there are missing value replace with 0, missing values can also occur this model reads data quicker (every 5s) than data is written by telegraf to influxdb (every 5s))

    - Predictions 
      - Interval : 5s (intervall for predictions, you probably want your predictions to be of the same interval with the frequency with which telegraf writes data to influxdb (every 5s))
      - Offset : 5s (An offset is a per-row “bias value” that is used during model training)

    - Anomalies
      - Min threshold : 0 (what goes below this value is considered anomaly, stored into the 'annotation_db: youAnnotationsEnterHere' and is excluded from your training data)
      - Max threshold : 0 (what goes above this value is considered anomaly, stored into the 'annotation_db: youAnnotationsEnterHere' and is excluded from your training data)

5. Dashboard setup InfluxDB and LoudML
- Simple explanation:
    - [ ] Query influxdb_internal to display your data : Result >> data will be displayed on the graph
    ![InfluxDB_internal](https://user-images.githubusercontent.com/63293696/180089553-a18e9945-d20c-46aa-9043-20e63f309caa.png)

    - [ ] Setup LoudML visualisation panel : Result >> LoudML 'Create Baseline' button will be able to work as expected
    ![LoudML-Visualisation-Grafana](https://user-images.githubusercontent.com/63293696/180089642-4503b2b1-89b7-44e3-822a-793ae7e1e274.png)
    
    - [ ] Create model using 'Create Baseline' button : Result >> A model will be automatically created and trained
    ![CreateModel-LoudML](https://user-images.githubusercontent.com/63293696/180090861-6c18232c-63d0-4e99-8424-7bc45dccf408.png)

    - [ ] Play the model and make predictions : Result >> Model will be available and predictions will be saved in the bucket your specified as output in loudml.yml
    ![Play-Forecast_LoudML](https://user-images.githubusercontent.com/63293696/180091890-8c2bdb6e-ad6f-44ed-8625-23d3e511fee6.png)

    - [ ] Query influxdb_predict to display predictions : Result >> predictions will be displayed along with the data on the graph
    ![Show-Predictions-LoudML](https://user-images.githubusercontent.com/63293696/180092770-5ba57d52-a687-432f-9752-c8e750781621.png)

- Query 
  - InfluxDB (From the top left dropdown, select the name set for Influx as datasource on Grafana)
    ![Screenshot 2022-06-21 173615](https://user-images.githubusercontent.com/63293696/174856028-35982c24-5ea0-4ed1-85e2-15334e5c54b7.png)

- Annotations query: 
```yml
SELECT "text" FROM "autogen"."annotations" WHERE $timeFilter
```
- Train loudml model query: 
  - --from now-30d --to now will take data starting 30days ago (from current date 'now' substract '30days' until the current date 'now')
```yml
loudml -e "train-model --from now-30d --to now _internal_cpu_mean_usage_system__time_5s"
```
![TrainModelExplanation](https://user-images.githubusercontent.com/63293696/180093233-74525464-9e43-4cd9-89af-3523d5d7ac2b.png)


- Panel 
  - Visualization
    - Loud ML Graph
  - Display 
    - Loud ML Server : Loud ML Datasource (Select the name set for LoudML as datasource on Grafana)
    - Input Bucket : readYourData (add the name of the input bucket in loudml.yml)
    - Output Bucket : yourPredictionsEnterHere  (add the name of the output database, located under the output bucket 'readYourPrediction' in loudml.yml)
    - Visualise:
    ![LoudML-Visualisation-Grafana](https://user-images.githubusercontent.com/63293696/180089776-3dce0661-47c0-4bd6-8221-690681467474.png)

    
6. LoudML CLI commands
- create model: 

Visualise:
- Grafana : Datasource :  Influx : InfluxDB_internal
   ![internal](https://user-images.githubusercontent.com/63293696/174865708-91080165-7e0c-46b8-b188-bc2250ff5bb8.png)
   
- Grafana : Datasource : Influx : InfluxDB_predict
   ![predict](https://user-images.githubusercontent.com/63293696/174866511-48d4858f-3257-483a-b785-501dd74c3dbf.png)

- Grafana : Datasource : Influx : InfluxDB-annotations
   ![annot](https://user-images.githubusercontent.com/63293696/174866522-ac1d4db0-8ff9-40e4-8811-e23b3adbc96e.png)

- Grafana : Datasource: LoudML : LoudML Datasource
   ![loudml](https://user-images.githubusercontent.com/63293696/174865920-5e8680c0-c694-48f9-92e2-cf09bc99074b.png)

- Grafana : Setup : Annotations
![anno1](https://user-images.githubusercontent.com/63293696/174867306-e77ea6ea-a96b-4dda-9498-c2be86170e24.png)
![anno2](https://user-images.githubusercontent.com/63293696/174867321-c5faaa71-e2e9-4174-8ed8-c4c50bc29603.png)

- Grafana : LoudML : Model
    ![loudml model](https://user-images.githubusercontent.com/63293696/174865996-96b1589b-6f25-43be-be23-4eebd8276e29.png)

- Grafana : LoudML: Dashboard Setup
  ![Grafana-Panel-Setup](https://user-images.githubusercontent.com/63293696/180094647-be17b234-2d60-40bd-b820-e545137b893b.png)


- Influx: Databases
  - Query if there is any data in the database:  
  ```sh
  select count(*) from /.*/
  ```
  - This database (chronograf) is created automatically by loudml to store annotations (unless you set it up yourself, LoudML will always try to create a database to store these annotations) but they should be stored in yourAnnotationsEnterHere. It means something was       not set up correctly for annotations to be stored where we want them! It could be because when seting up the Visualisation Panel to use LoudML we didn't specify the name of the output bucket as it is mentioned in loudml.yml ('readYourPrediction') where we already define the database to deal with annotations ('annotation_db: youAnnotationsEnterHere')
    ![Screenshot 2022-06-22 155650](https://user-images.githubusercontent.com/63293696/175062693-d40c2bcc-350c-4426-a8e1-dea562048f04.png)

    


