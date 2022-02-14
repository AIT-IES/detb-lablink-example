# DigitalEnergyTestbed Example Application

This project contains a [Lablink](https://ait-lablink.readthedocs.io) setup that implements a virtual testbed prototype developed as part of research project [DigitalEnergyTestbed](https://energieforschung.at/projekt/offene-testumgebung-zur-evaluierung-von-digitalisierungsloesungen-fuer-integrierte-strom-waermenetze/).

This setup includes the following components:

* A fully functional **digital twin of a distrcit heating substation test stand** is used for performing a preliminary assessment of the testbed performance.
  The digital twin comprises an OPC UA server, whose endpoints correspond to setpoints for and measurements from the test stand.
  These endpoints are linked to a thermo-hydraulic model of the test stand, which is executed internally and synchronized to  real time with a fixed communication step size.
  An [OPC UA client](https://ait-lablink.readthedocs.io/projects/ait-lablink-opc-ua-client) is used to connect the digital twin's OPC UA server with Lablink.
* Simulation models of a **district heating network** and a **heat consumer** (booster heat pump and building) are linked to the digital twin.
  [FMU simulator clients](https://ait-lablink.readthedocs.io/projects/ait-lablink-fmusim) are used to connect the the simulation models with Lablink.
* Several [plotters](https://ait-lablink.readthedocs.io/projects/ait-lablink-plotter) display status information of the models and data exchange with the digital twin in real time.

All simulation models used for this virtual testbed prototype are provided as [Functional Mock-up Units](https://en.wikipedia.org/wiki/Functional_Mock-up_Interface)(FMUs) an can be found in folder [fmu](./fmu).
They are compiled from the [Modelica](https://modelica.org/) models provided [here](https://github.com/AIT-IES/detb-models).


**NOTE**:
All following instructions are for **Windows**, using either the [command prompt](https://en.wikipedia.org/wiki/Cmd.exe) (``cmd.exe``) or by double-clicking batch scripts (files of type ``*.cmd``).
Running the setup on **Linux** works analogously, using the correspondig commands from a command shell.

## Prerequisites

You need to have the following software installed for running this setup:
 * **Java Development Kit**:
   for instance the [Oracle Java SE Development Kit 13](https://www.oracle.com/technetwork/java/javase/downloads/index.html) or the [OpenJDK](https://openjdk.java.net/)
 * **MQTT broker**:
   for instance [Eclipse Mosquitto](https://mosquitto.org/) or [EMQ](http://emqtt.io/)
 * **Python**:
   tested with [Python 3.8.5](https://www.python.org/downloads/release/python-385/)

Make sure that the ``JAVA_HOME`` environment variable is set and points to your JDK installation:
  * open the system properties (``WinKey`` + ``Pause`` or go to *Settings* => *System* => *About* => *System Info* => *Advanced System Settings*)
  * select the *Advanced* tab, then the *Environment Variables* button
  * select and edit the ``JAVA_HOME`` variable in the user variables, e.g., adding *C:\\Program Files\\Java\\jdk-13.0.2*.

## Installation

### Lablink packages download

All required Lablink packages are listed as dependencies in file ``pom.xml`` (a [Maven](https://maven.apache.org/) project configuration file).
To download all required Lablink packages, open the command prompt, change to the project's root directory and type:
```
  mvnw package
```

### OPC UA server installation

This setup uses a simple OPC UA server based on the [FreeOpcUa Python library](https://freeopcua.github.io/) for implementing a digital twin.
To install all required Python dependencies, open the command prompt, change to the project subdirectory [``setup\1_digital_twin``](./setup/1_digital_twin) and type:
```
  pip install -r requirements.txt
```

## Running the virtual testbed prototype

### Step 1: Starting the digital twin

To start the OPC UA server, open the command prompt, change to the project subdirectory [``setup\1_digital_twin``](./setup/1_digital_twin) and type:
```batch
  python teststand-opcua-server.py
```

### Step 2: Starting the Lablink config server

The configuration for all Lablink clients (incl. the CSV data for the CSV client) is contained in file [``setup\2_lablink_config\detb-sim-test-config.db``](./setup/2_lablink_config/detb-sim-test-config.db).
To start the Lablink config server, simply **double-click batch script** [``setup\2_lablink_config\run_config.cmd``](./setup/2_lablink_config/run_config.cmd).
Alternatively, you can open a new command prompt for each, change to the project subdirectory [``setup\3_run_testbed``](./setup/3_run_testbed) and type the script name.

**NOTE**:
Once the server is running, you can view the available configurations in a web browser via [http://localhost:10101](http://localhost:10101).

**NOTE**:
A convenient tool for viewing the content of the database file (and editing it for experimenting with the setup) is [DB Browser for SQLite](https://sqlitebrowser.org/).

### Step 3: Running the Lablink clients

All batch scripts for running the Lablink clients can be found in project subdirectory [``setup\3_run_testbed``](./setup/3_run_testbed).
To start all the Lablink clients, simply **double-click batch script**[``setup\3_run_testbed\run_testbed.cmd``](./setup/3_run_testbed/run_testbed.cmd).
Alternatively, you can open a new command prompt for each, change to the project subdirectory [``setup\3_run_testbed``](./setup/3_run_testbed) and type the script name.

**NOTE**:
You can start the Lablink clients in arbitrary order.
