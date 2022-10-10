# How to install and run PTT?
- [1. PTT: Package Testing Tool](#1.-ptt:-package-testing-tool)
    - [1.1 How to install?](#11-how-to-install)
    - [1.2 How to run?](#12-how-to-run)
    - [1.3 How it works?](#13-how-it-works)

    
## 1. PTT: Package Testing Tool


The *ptt* command line application is part of Evo SSIS testing infrastructure.  
The tools allow SSIS packages (but it's not limited to just SSIS packages) testing through the following simple process:  

* prepare the database environment for the ETL process execution (DB, input, etc.)
* run the SSIS packages
* compare the data on the test environment (DBs and filesystem) with static files (i.e. csv), tables, queries, regexp


Prerequisites:
* python 3.9
* SSIS component (from SQL Server installation DVD) must be installed locally
* python packages:
    * fire
    * aioodbc
    * pyyaml
    * jinja2
    * numpy
    * pandas

## 1.1 How to install

In order to install the tool in your **local environment** please follow these steps:
1. Clone the PTT project from [this](https://gitlab.evouser.com/etl/ssis-packages-test-tool.git) repository
2. Create your python virtual environment and then activate it (these instructions can vary based on your operating system)
```bash 
python -m venv venv
. ./venv/bin/activate
```
3. Install PTT and its prerequisites (python packages)
```bash 
python setup.py install
```
**Note:**
If you are developing the tool, remember to install the package using the `develop` command:  
Develop command helps you to edit and develop source code without having to re-install the tool itself and its packages after each modification, changes take effect immediately.
```bash
python setup.py develop
```


## 1.2 How to run
PTT is a command-line interface (CLI) and has a command named ```run``` which takes two parameters, the **test plan folder path**, and the **log output path**.  
In order to run the PTT please follow these steps:
1. Create your own config file:  
At the root of the project you can find a folder named ```config```, and you need to create a ```ptt.yml``` file in this folder. This file should contain a **connection string** to test DB and a path to the **dtexec tool**.
2. Prepare the test plan folder:   
A sample of test plans is located in [this](https://gitlab.evouser.com/etl/etl_v2/etl-common) repository.
You need to copy the ```tests``` folder of the etl-common repo into the root of the PTT project (or create your own test plans). This folder contains all you need to run PTT and test an SSIS package.
3. Run the tool:  
The first parameter provides the path of the test plan folder, and the second one locates the log of ispac executions.

```bash
python ./bin/ptt run [test plan folder path] [output log folder path]
```
## 1.3 How it works
A test plan contains all the rules needed for testing a package. The tool will pars test plan files and run actions found in the file.  
These rules can be set and config as below:  


- **Test plan variables**: (These variables will pass to the ispac file in its execution phase)
```yaml
variables:
  plan_name: testplan_cabinet
  database: teddy_input
  package_file: etl-common.ispac
  package_name: "cabinet common processing.dtsx"
  currency: EUR
```
- **Test plan setup and teardown**:  
Setup runs at the beginning of the execution and teardown will happen at the end, no matter how many test cases run in the middle of the execution phase.

- **Test cases**:  
**Setup**: This step runs at the beginning of the test case execution.  
**Teardown**: This step runs at the end of the test case execution.  
**Actions**: Actual test which evaluates and compares input file with the result of ingestion in the BD.  
