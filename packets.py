#-*- coding: utf-8 -*-
import ctypes

class PackedLittleEndianStructure(ctypes.LittleEndianStructure):
    _pack_ = 1


class PacketHeader(PackedLittleEndianStructure):

    _fields_ = [
        ("packetFormat", ctypes.c_uint16),
        ("gameMajorVersion", ctypes.c_uint8),
        ("gameMinorVersion", ctypes.c_uint8),
        ("packetVersion", ctypes.c_uint8),
        ("packetId", ctypes.c_uint8),
        ("sessionUID", ctypes.c_uint64),
        ("sessionTime", ctypes.c_float),
        ("frameIdentifier", ctypes.c_uint32),
        ("playerCarIndex", ctypes.c_uint8),
        ("secondaryPlayerCarIndex", ctypes.c_uint8)
    ]

class CarMotionData(PackedLittleEndianStructure):
    _fields_ = [
        ("worldPositionX", ctypes.c_float),
        ("worldPositionY", ctypes.c_float),
        ("worldPositionZ", ctypes.c_float),
        ("worldVelocityX", ctypes.c_float),
        ("worldVelocityY", ctypes.c_float),
        ("worldVelocityZ", ctypes.c_float),
        ("worldForwardDirX", ctypes.c_int16),
        ("worldForwardDirY", ctypes.c_int16),
        ("worldForwardDirZ", ctypes.c_int16),
        ("worldRightDirX", ctypes.c_int16),
        ("worldRightDirY", ctypes.c_int16),
        ("worldRightDirZ", ctypes.c_int16),
        ("gForceLateral", ctypes.c_float),
        ("gForceLongitudinal", ctypes.c_float),
        ("gForceVertical", ctypes.c_float),
        ("yaw", ctypes.c_float),
        ("pitch", ctypes.c_float),
        ("roll", ctypes.c_float),
    ]


class PacketMotionData(PackedLittleEndianStructure):
    _fields_ = [
        ("header", PacketHeader),
        ("carMotionData", CarMotionData * 22),
        # Extra player car ONLY data
        ("suspensionPosition", ctypes.c_float * 4),
        ("suspensionVelocity", ctypes.c_float * 4),
        ("suspensionAcceleration", ctypes.c_float * 4),
        ("wheelSpeed", ctypes.c_float * 4),
        ("wheelSlip", ctypes.c_float * 4),
        ("localVelocityX", ctypes.c_float),
        ("localVelocityY", ctypes.c_float),
        ("localVelocityZ", ctypes.c_float),
        ("angularVelocityX", ctypes.c_float),
        ("angularVelocityY", ctypes.c_float),
        ("angularVelocityZ", ctypes.c_float),
        ("angularAccelerationX", ctypes.c_float),
        ("angularAccelerationY", ctypes.c_float),
        ("angularAccelerationZ", ctypes.c_float),
        ("frontWheelsAngle", ctypes.c_float),
    ]


class MarshalZone(PackedLittleEndianStructure):

    _fields_ = [
        ("zoneStart", ctypes.c_float),
        ("zoneFlag", ctypes.c_int8)
    ]


class WeatherForecastSample(PackedLittleEndianStructure):

    _fields_ = [
        ("sessionType", ctypes.c_uint8),
        ("timeOffset", ctypes.c_uint8),
        ("weather", ctypes.c_uint8),
        ("trackTemperature", ctypes.c_int8),
        ("trackTemperatureChange", ctypes.c_int8),
        ("airTemperature", ctypes.c_int8),
        ("airTemperatureChange", ctypes.c_int8),
        ("rainPercentage", ctypes.c_uint8),
    ]


class PacketSessionData(PackedLittleEndianStructure):

    _fields_ = [
        ("header", PacketHeader),
        ("weather", ctypes.c_uint8),
        ("trackTemperature", ctypes.c_int8),
        ("airTemperature", ctypes.c_int8),
        ("totalLaps", ctypes.c_uint8),
        ("trackLength", ctypes.c_uint16),
        ("sessionType", ctypes.c_uint8),
        ("trackId", ctypes.c_int8),
        ("formula", ctypes.c_uint8),
        ("sessionTimeLeft", ctypes.c_uint16),
        ("sessionDuration", ctypes.c_uint16),
        ("pitSpeedLimit", ctypes.c_uint8),
        ("gamePaused", ctypes.c_uint8),
        ("isSpectating", ctypes.c_uint8),
        ("spectatorCarIndex", ctypes.c_uint8),
        ("sliProNativeSupport", ctypes.c_uint8),
        ("numMarshalZones", ctypes.c_uint8),
        ("marshalZones", MarshalZone * 21),
        ("safetyCarStatus", ctypes.c_uint8),
        ("networkGame", ctypes.c_uint8),
        ("numWeatherForecastSamples", ctypes.c_uint8),
        ("weatherForecastSamples", WeatherForecastSample * 56),
        ("forecastAccuracy", ctypes.c_uint8),
        ("aiDifficulty", ctypes.c_uint8),
        ("seasonLinkIdentifier", ctypes.c_uint32),
        ("weekendLinkIdentifier", ctypes.c_uint32),
        ("sessionLinkIdentifier", ctypes.c_uint32),
        ("pitStopWindowIdealLap", ctypes.c_uint8),
        ("pitStopWindowLatestLap", ctypes.c_uint8),
        ("pitStopRejoinPosition", ctypes.c_uint8),
        ("steeringAssist", ctypes.c_uint8),
        ("brackingAssist", ctypes.c_uint8),
        ("gearboxAssist", ctypes.c_uint8),
        ("pitAssist", ctypes.c_uint8),
        ("pitReleaseAssist", ctypes.c_uint8),
        ("ERSAssist", ctypes.c_uint8),
        ("DRSAssist", ctypes.c_uint8),
        ("dynamicRacingLain", ctypes.c_uint8),
        ("dynamicRacingLineType", ctypes.c_uint8),
        ("gameMode", ctypes.c_uint8),
        ("ruleSet", ctypes.c_uint32),
        ("sessionLength", ctypes.c_uint8),
    ]

class LapData(PackedLittleEndianStructure):

    _fields_ = [
        ("lastLapTime", ctypes.c_uint32),
        ("currentLapTime", ctypes.c_uint32),
        ("sector1TimeInMS", ctypes.c_uint16),
        ("sector2TimeInMS", ctypes.c_uint16),
        ("lapDistance", ctypes.c_float),
        ("totalDistance", ctypes.c_float),
        ("safetyCarDelta", ctypes.c_float),
        ("carPosition", ctypes.c_uint8),
        ("currentLapNum", ctypes.c_uint8),
        ("pitStatus", ctypes.c_uint8),
        ("numPitStops", ctypes.c_uint8),
        ("sector", ctypes.c_uint8),
        ("currentLapInvalid", ctypes.c_uint8),
        ("penalties", ctypes.c_uint8),
        ("warnings", ctypes.c_uint8),
        ("numUnservedDriveThroughPens", ctypes.c_uint8),
        ("numUnservedStopGoPens", ctypes.c_uint8),
        ("gridPosition", ctypes.c_uint8),
        ("driverStatus", ctypes.c_uint8),
        ("resultStatus", ctypes.c_uint8),
        ("pitLaneTimerActive", ctypes.c_uint8),
        ("pitLaneTimeInLaneInMS", ctypes.c_uint16),
        ("pitStopTimerInMS", ctypes.c_uint16),
        ("pitStopShouldServePen", ctypes.c_uint8),
    ]

class PacketLapData(PackedLittleEndianStructure):

    _fields_ = [
        ("header", PacketHeader),  # Header
        ("lapData", LapData * 22),
        ("timeTrialPBCarIdx", ctypes.c_uint8),
        ("timeTrialRivalCarIdx", ctypes.c_uint8),
    ]
class CarTelemetryData(PackedLittleEndianStructure):

    _fields_ = [
        ("speed", ctypes.c_uint16),
        ("throttle", ctypes.c_float),
        ("steer", ctypes.c_float),
        ("brake", ctypes.c_float),
        ("clutch", ctypes.c_uint8),
        ("gear", ctypes.c_int8),
        ("engineRPM", ctypes.c_uint16),
        ("drs", ctypes.c_uint8),
        ("revLightsPercent", ctypes.c_uint8),
        ("revLightsBitValue", ctypes.c_uint16),
        ("brakesTemperature", ctypes.c_uint16 * 4),
        ("tyresSurfaceTemperature", ctypes.c_uint8 * 4),
        ("tyresInnerTemperature", ctypes.c_uint8 * 4),
        ("engineTemperature", ctypes.c_uint16),
        ("tyresPressure", ctypes.c_float * 4),
        ("surfaceType", ctypes.c_uint8 * 4)
    ]
class PacketCarTelemetryData(PackedLittleEndianStructure):

    _fields_ = [
        ("header", PacketHeader),
        ("carTelemetryData", CarTelemetryData * 22),
        ("mfdPanelIndex", ctypes.c_uint8),
        ("mfdPanelIndexSecondaryPlayer", ctypes.c_uint8),
        ("suggestedGear", ctypes.c_int8)
    ]

class CarStatusData(PackedLittleEndianStructure):

    _fields_ = [
        ("tractionControl", ctypes.c_uint8),
        ("antiLockBrakes", ctypes.c_uint8),
        ("fuelMix", ctypes.c_uint8),
        ("frontBrakeBias", ctypes.c_uint8),
        ("pitLimiterStatus", ctypes.c_uint8),
        ("fuelInTank", ctypes.c_float),
        ("fuelCapacity", ctypes.c_float),
        ("fuelRemainingLaps", ctypes.c_float),
        ("maxRPM", ctypes.c_uint16),
        ("idleRPM", ctypes.c_uint16),
        ("maxGears", ctypes.c_uint8),
        ("drsAllowed", ctypes.c_uint8),
        ("drsActivationDistance", ctypes.c_uint16),
        ("actualTyreCompound", ctypes.c_uint8),
        ("visualTyreCompound", ctypes.c_uint8),
        ("tyresAgeLaps", ctypes.c_uint8),
        ("vehicleFiaFlags", ctypes.c_int8),
        ("ersStoreEnergy", ctypes.c_float),
        ("ersDeployMode", ctypes.c_uint8),
        ("ersHarvestedThisLapMGUK", ctypes.c_float),
        ("ersHarvestedThisLapMGUH", ctypes.c_float),
        ("ersDeployedThisLap", ctypes.c_float),
        ("networkPaused", ctypes.c_uint8)
    ]

class PacketCarStatusData(PackedLittleEndianStructure):

    _fields_ = [
        ("header", PacketHeader),
        ("carStatusData", CarStatusData * 22)
    ]

class CarDamageData(PackedLittleEndianStructure):

    _fields_ = [
        ("tyresWear", ctypes.c_float * 4),
        ("tyresDamage", ctypes.c_uint8 * 4),
        ("brakesDamage", ctypes.c_uint8 * 4),
        ("frontLeftWingDamage", ctypes.c_uint8),
        ("frontRightWingDamage", ctypes.c_uint8),
        ("rearWingDamage", ctypes.c_uint8),
        ("floorDamage", ctypes.c_uint8),
        ("diffuserDamage", ctypes.c_uint8),
        ("sidepodDamage", ctypes.c_uint8),
        ("drsFault", ctypes.c_uint8),
        ("ersFault", ctypes.c_uint8),
        ("gearBoxDamage", ctypes.c_uint8),
        ("engineDamage", ctypes.c_uint8),
        ("engineMGUHWear", ctypes.c_uint8),
        ("engineESWear", ctypes.c_uint8),
        ("engineCEWear", ctypes.c_uint8),
        ("engineICEWear", ctypes.c_uint8),
        ("engineMGUKWear", ctypes.c_uint8),
        ("engineTCWear", ctypes.c_uint8),
        ("engineBlown", ctypes.c_uint8),
        ("engineSeized", ctypes.c_uint8)
    ]
class PacketCarDamageData(PackedLittleEndianStructure):

    _fields_ = [
        ("header", PacketHeader),
        ("CarDamageData", CarDamageData * 22)
    ]

PacketType = {
    (2022, 1, 0): PacketMotionData,
    (2022, 1, 1): PacketSessionData,
    (2022, 1, 2): PacketLapData,
    (2022, 1, 6): PacketCarTelemetryData,
    (2022, 1, 7): PacketCarStatusData,
    (2022, 1, 10): PacketCarDamageData
}


def unpack_udp_packet(packet: bytes):
    header = PacketHeader.from_buffer_copy(packet)
    key = (header.packetFormat, header.packetVersion, header.packetId)
    if key not in PacketType:
        return 0
    else:
        packet_type = PacketType[key]
        return packet_type.from_buffer_copy(packet)

