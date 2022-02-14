@ECHO OFF

SETLOCAL

START "Data Point Bridge" dpb.cmd

TIMEOUT 5

START "Mass Flow Plotter" plot-mflow.cmd
START "Heat Flow Plotter" plot-qflow.cmd
START "Data Exchange Plotter" plot-data-exchange.cmd

TIMEOUT 5

START "DH Network Sim" sim-dhnetwork.cmd
START "Test Stand Sim" opcua-teststand.cmd
START "Single Consumer Sim" sim-consumer.cmd

PAUSE
