# LoudML-Grafana-Influx-Telegraf

As of 08.06.2022 : updated by Alberto, any queries email me `albertopopescu@outlook.com`

## Stage I REQUIREMENTS

- Windows 10 Enterprise version 21H2
- Docker version 20.10.13, build a224086
- Influx version 1.8.10
- Telegraf version 1.22.4
- Grafana version 7.5.8
- LoudML version 1.6.0


## Stage II WINDOWS-DOCKER SETUP

`WINDOWS`
1. Enable HYPER-V in windows features: https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/quick-start/enable-hyper-v
2. Install WSL2: https://www.omgubuntu.co.uk/how-to-install-wsl2-on-windows-10

Visualise:
![image](https://user-images.githubusercontent.com/63293696/172639073-ed240188-bd36-4c24-a096-9ef1b94d0261.png)

`Docker`

Visualise:
![image](https://user-images.githubusercontent.com/63293696/172639961-ab026550-c581-46d8-9e9a-e60db502d3f6.png)

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
      - var_loudml
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
      - var_influxdb
```
4. Service telegraf:

```yaml
  telegraf:
    image: telegraf:addVersionExample1.22.4
    container_name: addName
    restart: always
    volumes:
      - "addYourPcPathToConfigFile/telegraf/telegraf.conf:/etc/telegraf/telegraf.conf:ro" 
    environment: 
    - DOCKER_INFLUXDB_INIT_ORG=addNameOfOrganisation 
    - DOCKER_INFLUXDB_INIT_BUCKET=addNameOfYourBucket
    - DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=addTokenHereOrSetTokenInTelegrafConfigFile
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
      - var_grafana
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

1. Allow grafana to use unsigned plugins by adding this line into grafana.ini

```ini
[plugins]
allow_loading_unsigned_plugins = true
```

2. Setup Influx datasource

- Query Language : InfluxQL

- HTTP
  URL : http://influxdb:8086 (http://<nameOfInfluxServiceInDockerComposeFile>:<numberOfPortInfluxServiceOnDockerComposeFile>)
  Access: Server(Default)

- Custom HTTP Headers
  Header: Authorization Value: Token addNameOfYourTokenFromInfluxDB (Leave a space between 'Token' and 'yourActualToken')

- InfluxDB Details
  Database: _internal (Add any database/bucket you have created on Influx; '_internal' is the default database created by InfluxV1)
  Username: admin (The username for Influx service defined in docker-compose file or influxdb.conf file)
  Password: admin (the password for Influx service defined in docker-compose file or influxdb.conf file)
  HTTP Method: GET

Visualise:
    ![image](https://user-images.githubusercontent.com/63293696/172815599-334e69b7-0f33-4b0b-aecf-afb57944d74c.png)
