@ECHO OFF

REM =============================================================
REM Edit the following variables to comply with your local setup.
REM =============================================================

REM Connection string for configuration server.
SET LLCONFIG=http://localhost:10101/get?id=

REM Root directory of this Lablink setup (only change this if you really know what you are doing).
SET SETUP_ROOT_DIR=%~DP0..

REM Path to Java JAR file of the OPC UA client package.
SET OPCUA_CLIENT_JAR_FILE=%SETUP_ROOT_DIR%\target\dependency\opcuaclient-0.0.3-jar-with-dependencies.jar

REM Directory with FMI++ shared libraries.
SET FMIPP_DLL_DIR=%SETUP_ROOT_DIR%\target\natives

REM Path to Java JAR file of FMUSim client.
SET FMUSIM_JAR_FILE=%SETUP_ROOT_DIR%\target\dependency\fmusim-0.0.3-jar-with-dependencies.jar

REM Path to Java JAR file of data plotter.
SET PLOT_JAR_FILE=%SETUP_ROOT_DIR%\target\dependency\plotter-0.0.4-jar-with-dependencies.jar

REM Path to Java JAR file of data point bridge.
SET DPB_JAR_FILE=%SETUP_ROOT_DIR%\target\dependency\dpbridge-0.0.2-jar-with-dependencies.jar

REM Path to Java JAR file of config server.
SET CONFIG_JAR_FILE=%SETUP_ROOT_DIR%\target\dependency\config-0.1.1-jar-with-dependencies.jar

REM Check if environment variable JAVA_HOME has been defined.
IF NOT DEFINED JAVA_HOME (
    ECHO WARNING: environment variable JAVA_HOME not has been defined!
    PAUSE
)
