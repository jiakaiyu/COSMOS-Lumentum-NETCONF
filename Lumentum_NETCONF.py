""" Lumemtum ROADM 20 Control

Author:   Jiakai Yu (jiakaiyu@email.arizona.edu)
Created:  2018/09
Version:  3.0

Last modified by Jiakai: 2021/03/11
"""


import logging
import xmltodict
from ncclient import manager
from ncclient.xml_ import to_ele

logging.basicConfig(level=log_level)

USERNAME = "***"
PASSWORD = "***"


class Lumentum(object):

    def __init__(self, IP_addr, usrname=USERNAME, psswd=PASSWORD):
        self.m = manager.connect(host=IP_addr, port=830, username=usrname, password=psswd, hostkey_verify=False)

    def __del__(self):
        self.m.close_session()

    def edfa_status(self):

        filter_edfa = '''
        <filter>
          <edfas xmlns="http://www.lumentum.com/lumentum-ote-edfa" xmlns:lotee="http://www.lumentum.com/lumentum-ote-edfa">
          </edfas>
        </filter>

        '''
        try:
            edfa = self.m.get(filter_edfa)
            edfa_details = xmltodict.parse(edfa.data_xml)

            control_mode1 = str(edfa_details['data']['edfas']['edfa'][0]['config']['lotee:control-mode'])
            gain_mode1 = str(edfa_details['data']['edfas']['edfa'][0]['config']['lotee:gain-switch-mode'])
            target_gain1 = str(edfa_details['data']['edfas']['edfa'][0]['config']['lotee:target-gain'])
            target_power1 = str(edfa_details['data']['edfas']['edfa'][0]['config']['lotee:target-power'])
            input_power1 = str(edfa_details['data']['edfas']['edfa'][0]['state']['input-power'])
            output_power1 = str(edfa_details['data']['edfas']['edfa'][0]['state']['output-power'])
            voa_input_power1 = str(edfa_details['data']['edfas']['edfa'][0]['state']['voas']['voa']['voa-input-power'])
            voa_output_power1 = str(edfa_details['data']['edfas']['edfa'][0]['state']['voas']['voa']['voa-input-power'])
            voa_attenuation1 = str(edfa_details['data']['edfas']['edfa'][0]['state']['voas']['voa']['voa-attentuation'])
            status1 = str(edfa_details['data']['edfas']['edfa'][0]['config']['lotee:maintenance-state'])

            control_mode2 = str(edfa_details['data']['edfas']['edfa'][1]['config']['lotee:control-mode'])
            gain_mode2 = str(edfa_details['data']['edfas']['edfa'][1]['config']['lotee:gain-switch-mode'])
            target_gain2 = str(edfa_details['data']['edfas']['edfa'][1]['config']['lotee:target-gain'])
            target_power2 = str(edfa_details['data']['edfas']['edfa'][1]['config']['lotee:target-power'])
            input_power2 = str(edfa_details['data']['edfas']['edfa'][1]['state']['input-power'])
            output_power2 = str(edfa_details['data']['edfas']['edfa'][1]['state']['output-power'])
            voa_input_power2 = str(edfa_details['data']['edfas']['edfa'][1]['state']['voas']['voa']['voa-input-power'])
            voa_output_power2 = str(edfa_details['data']['edfas']['edfa'][1]['state']['voas']['voa']['voa-input-power'])
            voa_attenuation2 = str(edfa_details['data']['edfas']['edfa'][1]['state']['voas']['voa']['voa-attentuation'])
            status2 = str(edfa_details['data']['edfas']['edfa'][1]['config']['lotee:maintenance-state'])

            return {'PRE-AMP':
                        {'control mode': control_mode1,
                         'gain mode': gain_mode1,
                         'target gain': target_gain1,
                         'target power': target_power1,
                         'input power': input_power1,
                         'output power': output_power1,
                         'voa input power': voa_input_power1,
                         'voa output power': voa_output_power1,
                         'voa attenuation': voa_attenuation1,
                         'status': status1},

                    'BOOSTER':
                        {'control mode': control_mode2,
                         'gain mode': gain_mode2,
                         'target gain': target_gain2,
                         'target power': target_power2,
                         'input power': input_power2,
                         'output power': output_power2,
                         'voa input power': voa_input_power2,
                         'voa output power': voa_output_power2,
                         'voa attenuation': voa_attenuation2,
                         'status': status2},
                    }

        except Exception as e:
            print("Encountered the following RPC error!")
            print(e)
            return None

    def ALS_disable(self, module):

        service = '''<disable-alsxmlns="http://www.lumentum.com/lumentum-ote-edfa"><dn>ne=1;chassis=1;card=1;edfa=%sdn><timeout-period>600</timeout-period></disable-als>''' % (
            module)
        try:
            reply = self.m.dispatch(to_ele(service))
            return reply
        except Exception as e:
            print("Encountered the following RPC error!")
            print(e)
            return 0

    def edfa_config(self,
                    module,
                    ctrl_mode,
                    status,
                    gain_mode,
                    target_power,
                    target_gain,
                    tilt,
                    ALS
                    ):
        # self.module = module
        # self.ctrl_mode = ctrl_mode
        # self.status = status
        # self.gain_mode = gain_mode
        # self.target_power = target_power
        # self.target_gain = target_gain
        # self.tilt = tilt
        # self.ALS = ALS

        rpc_reply = 0
        self.edfa_data = self.edfa_status()

        #######out-of-service#######
        service0 = '''
          <xc:config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
            <edfas xmlns="http://www.lumentum.com/lumentum-ote-edfa" xmlns:lotee="http://www.lumentum.com/lumentum-ote-edfa">
              <edfa>
                <dn>ne=1;chassis=1;card=1;edfa=%s</dn>
                <config>
                  <maintenance-state>out-of-service</maintenance-state>
                </config>
              </edfa>
            </edfas>
          </xc:config>
              ''' % (module)

        #######configure#######
        service1 = '''
          <xc:config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
            <edfas xmlns="http://www.lumentum.com/lumentum-ote-edfa" 
            xmlns:lotee="http://www.lumentum.com/lumentum-ote-edfa">
              <edfa>
                <dn>ne=1;chassis=1;card=1;edfa=%s</dn>
                <config>
                  <maintenance-state>%s</maintenance-state>
                  <control-mode>%s</control-mode>
                  <gain-switch-mode>%s</gain-switch-mode>
                  <target-gain>%s</target-gain>
                  <target-power>%s</target-power>
                  <target-gain-tilt>%s</target-gain-tilt>
                </config>
              </edfa>
            </edfas>
          </xc:config>
              ''' % (module, status, ctrl_mode, gain_mode, target_gain, target_power, tilt)

        #######in-service#######
        service2 = '''
          <xc:config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
            <edfas xmlns="http://www.lumentum.com/lumentum-ote-edfa" xmlns:lotee="http://www.lumentum.com/lumentum-ote-edfa">
              <edfa>
                <dn>ne=1;chassis=1;card=1;edfa=%s</dn>
                <config>
                  <maintenance-state>in-service</maintenance-state>
                </config>
              </edfa>
            </edfas>
          </xc:config>
              ''' % (module)

        edfa_module = 'pre-amp' if int(module) == 0 else 'booster'
        if status == 'out-of-service':
            rpc_reply = self.m.edit_config(target='running', config=service0)

        elif self.edfa_data[edfa_module]['status'] == 'out-of-service':
            rpc_reply = self.m.edit_config(target='running', config=service1)

        elif status == 'in-service':
            if ctrl_mode == self.edfa_data[edfa_module]['control mode'] \
                    and gain_mode == self.edfa_data[edfa_module]['gain mode']:
                rpc_reply = self.m.edit_config(target='running', config=service1)
            else:
                rpc_reply0 = self.m.edit_config(target='running', config=service0)
                rpc_reply1 = self.m.edit_config(target='running', config=service1)

                rpc_reply_als = None
                if ALS:
                    rpc_reply_als = self.ALS_disable(module)
                if rpc_reply0 and rpc_reply1 and rpc_reply_als:
                    rpc_reply = 1
        return rpc_reply

    class WSSConnection(object):

        def __init__(self,
                     module,
                     connection_id,
                     operation,
                     blocked,
                     input_port,
                     output_port,
                     start_freq,
                     end_freq,
                     attenuation,
                     name
                     ):
            self.module = module
            self.connection_id = connection_id
            self.operation = operation
            self.blocked = blocked
            self.input_port = input_port
            self.output_port = output_port
            self.start_freq = start_freq
            self.end_freq = end_freq
            self.attenuation = attenuation
            self.name = name

    class WSSConnectionStatus(WSSConnection):
        def __init__(self,
                     module,
                     connection_id,
                     operation,
                     blocked,
                     input_port,
                     output_port,
                     start_freq,
                     end_freq,
                     attenuation,
                     name,
                     input_power,
                     output_power,
                     ne,
                     chassis,
                     card
                     ):
            super(Lumentum.WSSConnectionStatus, self).__init__(
                module,
                connection_id,
                operation,
                blocked,
                input_port,
                output_port,
                start_freq,
                end_freq,
                attenuation,
                name)
            self.input_power = input_power
            self.output_power = output_power
            self.ne = ne
            self.chassis = chassis
            self.card = card

        @classmethod
        def from_connection_details(cls, connection_details):
            return [
                cls(
                    connection_detail['dn'].split(';')[3].split('=')[1],
                    connection_detail['dn'].split(';')[4].split('=')[1],
                    connection_detail['config']['maintenance-state'],
                    connection_detail['config']['blocked'],
                    connection_detail['config']['input-port-reference'].split('port=')[1],
                    connection_detail['config']['output-port-reference'].split('port=')[1],
                    connection_detail['config']['start-freq'],
                    connection_detail['config']['end-freq'],
                    connection_detail['config']['attenuation'],
                    connection_detail['config']['custom-name'],
                    connection_detail['state']['input-channel-attributes']['power'],
                    connection_detail['state']['output-channel-attributes']['power'],
                    connection_detail['dn'].split(';')[0].split('=')[1],
                    connection_detail['dn'].split(';')[1].split('=')[1],
                    connection_detail['dn'].split(';')[2].split('=')[1]
                ) for connection_detail in connection_details['data']['connections']['connection'] if connection_detail
            ]

    def wss_add_connections(self, connections):

        def gen_connection_xml(wss_connection):
            return '''<connection>
              <dn>ne=1;chassis=1;card=1;module=%s;connection=%s</dn>
              <config>
                <maintenance-state>%s</maintenance-state>
                <blocked>%s</blocked>
                <start-freq>%s</start-freq>
                <end-freq>%s</end-freq>
                <attenuation>%s</attenuation>
                <input-port-reference>ne=1;chassis=1;card=1;port=%s</input-port-reference>
                <output-port-reference>ne=1;chassis=1;card=1;port=%s</output-port-reference>
                <custom-name>%s</custom-name>
              </config> 
            </connection>''' % (
                wss_connection.module,
                wss_connection.connection_id,
                wss_connection.operation,
                wss_connection.blocked,
                wss_connection.start_freq,
                wss_connection.end_freq,
                wss_connection.attenuation,
                wss_connection.input_port,
                wss_connection.output_port,
                wss_connection.name
            )

        new_line = '\n'
        services = '''<xc:config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <connections xmlns="http://www.lumentum.com/lumentum-ote-connection" 
        xmlns:lotet="http://www.lumentum.com/lumentum-ote-connection">
            %s
        </connections>
        </xc:config>''' % new_line.join([gen_connection_xml(connection) for connection in connections])

        try:
            reply = self.m.edit_config(target='running', config=services)
            if '<ok/>' in str(reply):
                print('Successfully Added Connections')
                return 1
            return 0
        except Exception as e:
            print("Encountered the following RPC error!")
            print(e)
            return 0

    def wss_delete_connection(self, module_id, connection_id):
        try:
            if connection_id == 'all':
                reply = self.m.dispatch(to_ele('''
                <remove-all-connections
                xmlns="http://www.lumentum.com/lumentum-ote-connection">
                <dn>ne=1;chassis=1;card=1;module=%s</dn>
                </remove-all-connections>
                ''' % module_id))
            else:
                reply = self.m.dispatch(to_ele('''
                <delete-connection xmlns="http://www.lumentum.com/lumentum-ote-connection">
                <dn>ne=1;chassis=1;card=1;module=%s;connection=%s</dn>
                </delete-connection>
                ''' % (module_id, connection_id)))
            if '<ok/>' in str(reply):
                print('Successfully Deleted Connection')
                return 1
            return 0
        except Exception as e:
            print("Encountered the following RPC error!")
            print(e)
            return 0

    def wss_get_connections(self):
        command = '''
                <filter>
                  <connections xmlns="http://www.lumentum.com/lumentum-ote-connection">
                  </connections>
                </filter>
                '''
        try:
            conn = self.m.get(command)
            connection_details = xmltodict.parse(conn.data_xml)
        except Exception as e:
            connection_details = None
            print("Encountered the following RPC error!")
            print(e)
        connections = Lumentum.WSSConnectionStatus.from_connection_details(
            connection_details) if connection_details else None
        return connections

    @staticmethod
    def gen_dwdm_connections(module, input_port, output_port, loss=0.0, channel_spacing=50.0, channel_width=50.0):
        """
        :param module:
        :param input_port:
        :param output_port:
        :param channel_spacing: in GHz
        :param channel_width: in GHz
        :return:
        """
        connections = []
        half_channel_width = channel_width / 2.0  # in GHz
        start_center_frequency = 191350.0  # in GHz
        for i in range(96):
            center_frequency = start_center_frequency + i * channel_spacing
            connection = Lumentum.WSSConnection(
                module,
                str(i + 1),
                'in-service',
                'false',
                input_port,
                output_port,
                str(center_frequency - half_channel_width),
                str(center_frequency + half_channel_width),
                loss,
                'CH' + str(i + 1)
            )
            connections.append(connection)
        return connections
    
    # NOT WORKING
    def wss_chnnl_leveling(self, module_id):
        connections = self.wss_get_connections()
        tunning_chnnls = []  # MonitorConnectionEvent
        tunning_chnnl_conns = []  # Lumentum.WSSConnection
        max_in = -30
        min_in = 5
        if connections:
            l = len(connections)
            for i in range(0, l):
                if connections[i].module != module_id:
                    continue
                if -30 < float(connections[i].input_power) < 5 and float(connections[i].input_power) < min_in:
                    min_in = connections[i].input_power
                if float(connections[i].input_power) > max_in:
                    max_in = connections[i].input_power
                if float(connections[i].attenuation) > 0 and float(connections[i].input_power) > -30:
                    conn = Custom_event.MonitorConnectionEvent()
                    conn.id = connections[i].connection_id
                    conn.module = connections[i].module
                    conn.name = connections[i].name
                    conn.status = connections[i].operation
                    conn.start_freq = connections[i].start_freq
                    conn.end_freq = connections[i].end_freq
                    conn.attenuation = connections[i].attenuation
                    conn.block = connections[i].blocked
                    conn.input_port = connections[i].input_port
                    conn.output_port = connections[i].output_port
                    conn.input_power = connections[i].input_power
                    conn.output_power = connections[i].output_power
                    tunning_chnnls.append(conn)
        for chnnl in tunning_chnnls:
            dif = max_in - float(chnnl.input_power)
            if 0.1 < dif <= float(chnnl.attenuation):
                chnnl.attenuation = format((float(chnnl.attenuation) - dif), '.1f')
            else:
                chnnl.attenuation = '0.0'
            connection = Lumentum.WSSConnection(str(chnnl.module), str(chnnl.id), str(chnnl.status), str(chnnl.block),
                                                str(chnnl.input_port), str(chnnl.output_port),
                                                str(chnnl.start_freq), str(chnnl.end_freq), str(chnnl.attenuation),
                                                str(chnnl.name))
            tunning_chnnl_conns.append(connection)
        if len(tunning_chnnl_conns) > 0: self.wss_add_connections(tunning_chnnl_conns)
        return max_in, min_in

