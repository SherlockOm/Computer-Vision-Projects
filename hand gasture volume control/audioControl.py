from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np

class AudioControl():
    def __init__(self):
        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = self.interface.QueryInterface(IAudioEndpointVolume)

    def mute(self):
        self.volume.SetMasterVolumeLevel(-65, None)

    def setVolume(self, decibels):
        # if decibels < 0.1 : decibels = 0
        # if decibels > 1: decibels = 1
        # volume = 65.25*decibels - 65.25;
        volume = np.interp(decibels, [0,100], [-65.25, 0])
        self.volume.SetMasterVolumeLevel(volume, None)

