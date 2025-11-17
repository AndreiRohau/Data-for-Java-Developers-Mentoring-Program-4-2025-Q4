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
INFO: Auth Url: https://oauth2.neon.tech/oauth2/auth?scope=openid+offline+offline_access+urn%3Aneoncloud%3Aprojects%3Acreate+urn%3Aneoncloud%3Aprojects%3Aread+urn%3Aneoncloud%3Aprojects%3Aupdate+urn%3Aneoncloud%3Aprojects%3Adelete+urn%3Aneoncloud%3Aorgs%3Acreate+urn%3Aneoncloud%3Aorgs%3Aread+urn%3Aneoncloud%3Aorgs%3Aupdate+urn%3Aneoncloud%3Aorgs%3Adelete+urn%3Aneoncloud%3Aorgs%3Apermission&state=3_Vmv7WiZjoobZLT5e87DS4aNNuMfIdYD39eI2IGUAI&code_challenge=cJTz3LVCDhZVt4EMwBVUmBopHqGGDOPuRVEIdpP9zqU&code_challenge_method=S256&redirect_uri=http%3A%2F%2F127.0.0.1%3A63951%2Fcallback&client_id=neonctl&response_type=code
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









