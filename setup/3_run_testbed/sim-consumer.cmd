@ECHO OFF

SETLOCAL

REM Load the setup for the examples.
CALL "%~DP0\..\setup.cmd"

REM Path to class implementing the main routine.
REM SET FMUSIM=at.ac.ait.lablink.clients.fmusim.DynamicFmuModelExchangeAsync
SET FMUSIM=at.ac.ait.lablink.clients.fmusim.FixedStepFmuModelExchangeAsync

REM Data point bridge configuration.
SET FMU_DIR=-DfmuDir=%SETUP_ROOT_DIR%

REM Logger configuration.
SET LOGGER_CONFIG=-Dlog4j.configurationFile=%LLCONFIG%ait.all.log4j2

REM Data point bridge configuration.
SET CONFIG_FILE_URI=%LLCONFIG%ait.test.detbsim.sim.consumer.config

REM Add directory with FMI++ shared libraries to system path.
SET PATH=%FMIPP_DLL_DIR%;%PATH%

REM Run the example.
"%JAVA_HOME%\bin\java.exe" %LOGGER_CONFIG% %FMU_DIR% -cp "%FMUSIM_JAR_FILE%" %FMUSIM% -c %CONFIG_FILE_URI%

PAUSE