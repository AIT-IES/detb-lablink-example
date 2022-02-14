from opcua import ua, Server
from opcua.server.user_manager import UserManager
import threading, time, schedule
import fmipp
import os
from pathlib import Path


class DETBTeststandServer:
    '''
    A simple server providing an OPC-UA-compliant interface to a
    simulation model of a DH substation. This simulation model
    is realized as an FMU for Model Exchange and internally
    synchronized to real time with a fixed communication step size.
    '''

    # OPC-UA server user database.
    __users_db = {'LablinkTestUser': 'zQC37UiH6ou'}


    def init(self, fmu_work_dir, model_name, t_update=10):
        '''
        Initilaize the OPC-UA server and the internal simulation model.
        '''
        self.t_update = t_update
        self.__init_server()
        self.__init_sim(fmu_work_dir, model_name)


    def run(self):
        '''
        Run the OPC-UA server and synchronize the internal simulation model with real time.
        '''
        # Start the OPC-UA server
        self.server.start()

        # Schedule updates for the simulated model.
        schedule.every(self.t_update).seconds.do(self.__run_threaded, self.__sim)

        t_sleep = 1. if (self.t_update > 1.) else (0.5 * self.t_update)

        try:
            while True:
                schedule.run_pending()
                time.sleep(t_sleep)

        except KeyboardInterrupt:
            self.server.stop()


    def __init_server(self):
        '''
        Initialize the OPC-UA server.
        '''
        self.server = Server()

        self.server.set_server_name('Dummy Teststand Server')
        self.server.set_endpoint('opc.tcp://localhost:12345/teststand-server')

        self.server.set_security_policy([ua.SecurityPolicyType.NoSecurity])

        self.server.set_security_IDs(['Username'])
        self.server.user_manager.set_user_manager(self.__user_manager)

        idx = self.server.register_namespace('urn:detb:sim-test')

        folder_teststand_sim = self.server.nodes.objects.add_folder(idx, 'Teststand')

        str_nodeid_stub = 'ns={};s=Teststand/{};'

        #
        # Define attributes used as inputs to the internal simulation model (writable attributes).
        #
        self.T_return_secondary_set = folder_teststand_sim.add_variable(
            str_nodeid_stub.format(idx, 'T_return_secondary_set'),
            'T_return_secondary_set', 323.15, ua.VariantType.Double
            )
        self.T_return_secondary_set.set_writable()

        self.T_supply_primary_set = folder_teststand_sim.add_variable(
            str_nodeid_stub.format(idx, 'T_supply_primary_set'),
            'T_supply_primary_set', 353.15, ua.VariantType.Double
            )
        self.T_supply_primary_set.set_writable()

        self.m_flow_return_secondary = folder_teststand_sim.add_variable(
            str_nodeid_stub.format(idx, 'm_flow_return_secondary'),
            'm_flow_return_secondary', 0, ua.VariantType.Double
            )
        self.m_flow_return_secondary.set_writable()

        self.delta_p_secondary_set = folder_teststand_sim.add_variable(
            str_nodeid_stub.format(idx, 'delta_p_secondary_set'),
            'delta_p_secondary_set', 200000, ua.VariantType.Double
            )
        self.delta_p_secondary_set.set_writable()

        self.delta_p_primary_set = folder_teststand_sim.add_variable(
            str_nodeid_stub.format(idx, 'delta_p_primary_set'),
            'delta_p_primary_set', 0, ua.VariantType.Double
            )
        self.delta_p_primary_set.set_writable()

        self.T_supply_secondary_ctrl = folder_teststand_sim.add_variable(
            str_nodeid_stub.format(idx, 'T_supply_secondary_ctrl'),
            'T_supply_secondary_ctrl', False, ua.VariantType.Boolean
            )
        self.T_supply_secondary_ctrl.set_writable()

        #
        # Define attributes used as outputs of the internal simulation model (non-writable attributes).
        #
        self.T_supply_secondary = folder_teststand_sim.add_variable(
            str_nodeid_stub.format(idx, 'T_supply_secondary'),
            'T_supply_secondary', 0, ua.VariantType.Double
            )

        self.T_return_primary = folder_teststand_sim.add_variable(
            str_nodeid_stub.format(idx, 'T_return_primary'),
            'T_return_primary', 0, ua.VariantType.Double
            )

        self.m_flow_return_primary = folder_teststand_sim.add_variable(
            str_nodeid_stub.format(idx, 'm_flow_return_primary'),
            'm_flow_return_primary', 0, ua.VariantType.Double
            )

        self.substation_m1_flow = folder_teststand_sim.add_variable(
            str_nodeid_stub.format(idx, 'testStandDummy.substation.m1_flow'),
            'testStandDummy.substation.m1_flow', 0, ua.VariantType.Double
            )

        self.substation_m2_flow = folder_teststand_sim.add_variable(
            str_nodeid_stub.format(idx, 'testStandDummy.substation.m2_flow'),
            'testStandDummy.substation.m2_flow', 0, ua.VariantType.Double
            )

        self.substation_hex_Q2_flow = folder_teststand_sim.add_variable(
            str_nodeid_stub.format(idx, 'testStandDummy.substation.hex.Q2_flow'),
            'testStandDummy.substation.hex.Q2_flow', 0, ua.VariantType.Double
            )


    def __init_sim(self, fmu_work_dir, model_name):
        '''
        Initialize the simulation.
        '''
        # Extract FMU.
        path_to_fmu = os.path.join(fmu_work_dir, model_name + '.fmu')
        uri_to_extracted_fmu = fmipp.extractFMU(path_to_fmu, fmu_work_dir)

        # Configuration parameters for FMU wrapper.
        logging_on = False
        stop_before_event = False
        event_search_precision = 1e-6
        integrator_type = fmipp.bdf

        # Create FMU wrapper.
        self.fmu = fmipp.FMUModelExchangeV2(
            uri_to_extracted_fmu, model_name,
            logging_on, stop_before_event,
            event_search_precision, integrator_type
            )

        # Instantiate model.
        status = self.fmu.instantiate('teststand_model')
        assert status == fmipp.fmiOK # check status

        # Set initial values.
        self.fmu.setRealValue('T_return_secondary_set', self.T_return_secondary_set.get_value())
        self.fmu.setRealValue('T_supply_primary_set', self.T_supply_primary_set.get_value())
        self.fmu.setRealValue('m_flow_return_secondary', self.m_flow_return_secondary.get_value())
        self.fmu.setRealValue('delta_p_secondary_set', self.delta_p_secondary_set.get_value())
        self.fmu.setRealValue('delta_p_primary_set', self.delta_p_primary_set.get_value())
        self.fmu.setBooleanValue('T_supply_secondary_ctrl', self.T_supply_secondary_ctrl.get_value())

        # Initialize model.
        status = self.fmu.initialize()
        assert status == fmipp.fmiOK # check status

        self.sync_time = 0;
        self.step_size = self.t_update;
        self.next_sync_point = self.sync_time + self.step_size


    def __sim(self):
        '''
        Update the simulation model and write
        '''
        # Set inputs.
        self.fmu.setRealValue('T_return_secondary_set', self.T_return_secondary_set.get_value())
        self.fmu.setRealValue('T_supply_primary_set', self.T_supply_primary_set.get_value())
        self.fmu.setRealValue('m_flow_return_secondary', self.m_flow_return_secondary.get_value())
        self.fmu.setRealValue('delta_p_secondary_set', self.delta_p_secondary_set.get_value())
        self.fmu.setRealValue('delta_p_primary_set', self.delta_p_primary_set.get_value())
        self.fmu.setBooleanValue('T_supply_secondary_ctrl', self.T_supply_secondary_ctrl.get_value())

        #self.fmu.raiseEvent()
        self.fmu.handleEvents()

        # Compute timestamp of next synchronization point.
        self.next_sync_point = self.next_sync_point + self.step_size

        # In case an internal event is encountered, the integration stops. Therefore, the FMU model's
        # integration method may be called several times until next synchronization point is reached.
        while (self.sync_time < self.next_sync_point - 1e-4):
            self.sync_time = self.fmu.integrate(self.next_sync_point)

        # Update the outputs of the server with the latest simulation results.
        self.T_supply_secondary.set_value(self.fmu.getRealValue('T_supply_secondary'))
        self.T_return_primary.set_value(self.fmu.getRealValue('T_return_primary'))
        self.m_flow_return_primary.set_value(self.fmu.getRealValue('m_flow_return_primary'))
        self.substation_m1_flow.set_value(self.fmu.getRealValue('testStandDummy.substation.m1_flow'))
        self.substation_m2_flow.set_value(self.fmu.getRealValue('testStandDummy.substation.m2_flow'))
        self.substation_hex_Q2_flow.set_value(self.fmu.getRealValue('testStandDummy.substation.hex.Q2_flow'))


    def __user_manager(self, isession, username, password):
        '''
        Callback function for user access management.
        '''
        isession.user = UserManager.User
        login_ok = (username in self.__users_db) and (password == self.__users_db[username])
        print('Login attempt with username "{}": {}'.format(username, 'SUCCESS' if login_ok else 'FAILED'))
        return login_ok


    def __run_threaded(self, job):
        job_thread = threading.Thread(target=job)
        job_thread.start()


# Main routine.
if __name__ == '__main__':

    fmu_dir = fmu_work_dir = Path( Path( __file__ ).parent, '..', '..', 'fmu' ).resolve( strict = True )

    server = DETBTeststandServer()

    server.init(
        fmu_work_dir = fmu_dir,
        model_name = 'TeststandCtrl',
        t_update = 10
        )

    server.run()