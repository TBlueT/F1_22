from struct import unpack


class ForzaDataPacket:
    sled_format = '<iIfffffffffffffffffffffffffffffffffffffffffffffffffffiiiii'
    dash_format = '<iIfffffffffffffffffffffffffffffffffffffffffffffffffffiiiiifffffffffffffffffHBBBBBBbbb'

    ## The names of the properties in the V2 format called 'car dash'
    sled_props = [
        'is_race_on', 'timestamp_ms',
        'engine_max_rpm', 'engine_idle_rpm', 'current_engine_rpm',
        'acceleration_x', 'acceleration_y', 'acceleration_z',
        'velocity_x', 'velocity_y', 'velocity_z',
        'angular_velocity_x', 'angular_velocity_y', 'angular_velocity_z',
        'yaw', 'pitch', 'roll',
        'norm_suspension_travel_FL', 'norm_suspension_travel_FR',
        'norm_suspension_travel_RL', 'norm_suspension_travel_RR',
        'tire_slip_ratio_FL', 'tire_slip_ratio_FR',
        'tire_slip_ratio_RL', 'tire_slip_ratio_RR',
        'wheel_rotation_speed_FL', 'wheel_rotation_speed_FR',
        'wheel_rotation_speed_RL', 'wheel_rotation_speed_RR',
        'wheel_on_rumble_strip_FL', 'wheel_on_rumble_strip_FR',
        'wheel_on_rumble_strip_RL', 'wheel_on_rumble_strip_RR',
        'wheel_in_puddle_FL', 'wheel_in_puddle_FR',
        'wheel_in_puddle_RL', 'wheel_in_puddle_RR',
        'surface_rumble_FL', 'surface_rumble_FR',
        'surface_rumble_RL', 'surface_rumble_RR',
        'tire_slip_angle_FL', 'tire_slip_angle_FR',
        'tire_slip_angle_RL', 'tire_slip_angle_RR',
        'tire_combined_slip_FL', 'tire_combined_slip_FR',
        'tire_combined_slip_RL', 'tire_combined_slip_RR',
        'suspension_travel_meters_FL', 'suspension_travel_meters_FR',
        'suspension_travel_meters_RL', 'suspension_travel_meters_RR',
        'car_ordinal', 'car_class', 'car_performance_index',
        'drivetrain_type', 'num_cylinders'
    ]

    ## The additional props added in the 'car dash' format
    dash_props = ['position_x', 'position_y', 'position_z',
                  'speed', 'power', 'torque',
                  'tire_temp_FL', 'tire_temp_FR',
                  'tire_temp_RL', 'tire_temp_RR',
                  'boost', 'fuel', 'dist_traveled',
                  'best_lap_time', 'last_lap_time',
                  'cur_lap_time', 'cur_race_time',
                  'lap_no', 'race_pos',
                  'accel', 'brake', 'clutch', 'handbrake',
                  'gear', 'steer',
                  'norm_driving_line', 'norm_ai_brake_diff']

    def __init__(self, data):
        patched_data = data[:232] + data[244:323]
        for prop_name, prop_value in zip(self.sled_props + self.dash_props,
                                         unpack(self.dash_format,
                                                patched_data)):
            setattr(self, prop_name, prop_value)

    @classmethod
    def get_props(cls):
        '''
        Return the list of properties in the data packet, in order.
        :param packet_format: which packet format to get properties for,
                one of either 'sled' or 'dash'
        :type packet_format: str
        '''

        return (cls.sled_props + cls.dash_props)

    def to_list(self, attributes):
        '''
        Return the values of this data packet, in order. If a list of
        attributes are provided, only return those.
        :param attributes: the attributes to return
        :type attributes: list
        '''
        if attributes:
            return ([getattr(self, a) for a in attributes])

        return ([getattr(self, prop_name) for prop_name in self.sled_props + self.dash_props])

import socket
import time
import ctypes
import threading

from packets import unpack_udp_packet, PacketCarTelemetryData, CarTelemetryData
class Process2(threading.Thread):
    def __init__(self, parent=None):
        threading.Thread.__init__(self)
        self.Working = True

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', 2077))

        self.PCTD = PacketCarTelemetryData()
        self.PCTD.header.packetFormat = 2020
        self.PCTD.header.packetVersion = 1
        self.PCTD.header.packetId = 6
        self.PCTD.header.playerCarIndex = 1

    def run(self):
        while self.Working:
            data, addr = self.sock.recvfrom(3000)
            # print(addr)
            FPD = ForzaDataPacket(data)
            pack = FPD.to_list(["speed", "current_engine_rpm", "gear", "engine_max_rpm", "tire_temp_FL", "tire_temp_FR", "tire_temp_RL", "tire_temp_RR"])
            speed = ctypes.c_uint16(int(pack[0] * 3.6))
            power = ctypes.c_uint16(int(pack[1]))
            gear = ctypes.c_int8(int(pack[2]))
            engine_max_rpm = pack[3]

            tire_temp_FL = ctypes.c_uint8(int(pack[4]))
            tire_temp_FR = ctypes.c_uint8(int(pack[5]))
            tire_temp_RL = ctypes.c_uint8(int(pack[6]))
            tire_temp_RR = ctypes.c_uint8(int(pack[7]))

            gear = -1 if gear == 0 else gear

            a = pack[1] - engine_max_rpm/4*3
            a = a if a > 0 else 0
            revLightsPercent = int(self.map(a, 0, 2300, 0, 100))
            revLightsPercent = revLightsPercent if revLightsPercent < 100 else 100
            revLightsPercent = ctypes.c_uint8(revLightsPercent)


            self.PCTD.carTelemetryData[self.PCTD.header.playerCarIndex].speed = speed
            self.PCTD.carTelemetryData[self.PCTD.header.playerCarIndex].engineRPM = power
            self.PCTD.carTelemetryData[self.PCTD.header.playerCarIndex].gear = gear
            self.PCTD.carTelemetryData[self.PCTD.header.playerCarIndex].revLightsPercent = revLightsPercent
            self.PCTD.carTelemetryData[self.PCTD.header.playerCarIndex].tyresInnerTemperature[0] = tire_temp_FL
            self.PCTD.carTelemetryData[self.PCTD.header.playerCarIndex].tyresInnerTemperature[1] = tire_temp_FR
            self.PCTD.carTelemetryData[self.PCTD.header.playerCarIndex].tyresInnerTemperature[2] = tire_temp_RL
            self.PCTD.carTelemetryData[self.PCTD.header.playerCarIndex].tyresInnerTemperature[3] = tire_temp_RR

    def map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
class Process:
    def __init__(self):
        self.Working = True
        self.th = Process2(self)
        self.th.start()
    def run(self):
        while self.Working:

            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(self.th.PCTD, ("192.168.1.8", 20777))
            time.sleep(0.05)

if __name__ == "__main__":
    P = Process()
    P.run()