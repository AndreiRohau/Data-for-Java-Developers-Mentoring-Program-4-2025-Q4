# Step 1 NeonDB setup

NeonDB

a.rohau.work

https://console.neon.tech/app/projects/still-pine-43384528

https://console.neon.tech/app/projects/still-pine-43384528/branches/br-autumn-feather-a4vu1uh1/

---
Dev branch
connection string
```

jdbc:postgresql://ep-crimson-mode-a4uljk4s-pooler.us-east-1.aws.neon.tech/metrics?user=neondb_owner&password=**************&sslmode=require&channelBinding=require
```
passwordless auth
```
psql -h pg.neon.tech
```
![img_3.png](img_3.png)

---
Install NeonDB Cli

```shell
npm install -g neonctl
neonctl --version
neon auth
```
```commandline
INFO: Awaiting authentication in web browser.
INFO: Auth Url: https://oauth2.neon.tech/oauth2/auth?scope=openid....
INFO: Auth complete
```

Auth data is saved here: ```C:\Users\<user>\.config\neonctl\credentials.json```


Project 'metrics' id 'still-pine-43384528'
![img_1.png](img_1.png)
Organization 'Andrei' id 'org-sweet-hall-92621226'
![img_2.png](img_2.png)



```commandline
neonctl branches create --name Dev --org-id org-sweet-hall-92621226 --project-id still-pine-43384528
OR
neonctl branches create --name Dev --organization-id org-sweet-hall-92621226 --project-id still-pine-43384528
```




---
# Step 2 Airflow project setup

- install Astro CLI 
- - https://github.com/astronomer/astro-cli/releases
- - located: "C:\localprogs\astronomer" as astro.exe and astro_1.38.1_windows_amd64.exe
- - addede env var: ASTRONOMER_HOME and path %ASTRONOMER_HOME%
- - Close IDEA (restart doesnt work)
- validate astro version
- - in cmd "astro version" -> 1.38.1



Initialization: go to project root dir
```commandline
mkdir airflow
cd airflow
astro dev init
```
![img_4.png](img_4.png)

Modify Dockerfile to allow testing of the connection
```
FROM quay.io/astronomer/astro-runtime:12.2.0
# Set environment variables
ENV AIRFLOW__CORE__TEST_CONNECTION=Enabled
```


Modify requirement.txt and include dbt-cloud
```
apache-airflow-providers-dbt-cloud==3.10.0
```

#### Run Airflow
- put a sample DAG to the `dags` folder - for example, use [this snippet](https://github.com/sungchun12/airflow-dbt-cloud/blob/main/dags/example-dag.py)
- from the root folder of you project, execute the following command: `astro dev start`
- wait until all the images are downloaded and Airflow is started - may take up to 10 minutes for the first time
- test that Airflow admin UI is available at `localhost:8080`
- try running your sample DAG
- keep in mind the following [Astro CLI command reference](https://www.astronomer.io/docs/astro/cli/reference)

---
# Step 3 - Airflow-NeonDB integration

```
cd /home/arohau/vscode_space/learn/big-data-run/Data-for-Java-Developers-Mentoring-Program-4-2025-Q4/module-4-task/airflow-project-setup/airflow && astro dev start
```

### Create a role for Airflow:

- open NeonDB SQL editor - make sure to choose your Dev branch and metrics DB
- create a airflow-agent role
- make sure to grant it the CREATE privileges on the metrics schema

```
CREATE ROLE "airflow-agent" WITH PASSWORD 'agent_password#007' LOGIN CREATEDB CREATEROLE;
CREATE SCHEMA IF NOT EXISTS metrics;
GRANT USAGE ON SCHEMA metrics TO "airflow-agent";
GRANT CREATE ON SCHEMA metrics TO "airflow-agent";
```

### Create a DB connection in Airflow

#### Steps to Create NeonDB Connection in Airflow UI:
1. Open Airflow UI at http://localhost:8080 in your Windows Chrome browser
2. Login with admin / admin
3. Navigate to Connections:
    - Click on **Admin** in the top menu
    - Select **Connections** from the dropdown
4. Add a New Connection - Click the + (plus) button
5. Fill in the Connection Details:
    - Connection Id: neon_db (or your preferred name)
    - Connection Type: Select Postgres from the dropdown
    - Host: Your NeonDB hostname (from Neon console, looks like: xxx-xxx-xxx.neon.tech)
    - Schema: Your database name (e.g., neondb or main)
    - Login: airflow-agent (the role name you created)
    - Password: The password for your airflow-agent role
    - Port: 5432 (default PostgreSQL port)
    - Extra: (Optional) Add SSL settings:
    ```
    {"sslmode": "require"}
    ```
6. Test the Connection:
    - Click the Test button at the bottom
    - Make sure you see a success message with no errors
7. Save the connection


![alt text](image.png)

Generate dag, prepare sqls

```
SELECT tablename
FROM pg_tables
WHERE schemaname = 'metrics';
```

---
# Step 4 - data ingestion setup






