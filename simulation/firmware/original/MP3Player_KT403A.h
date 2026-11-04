#pragma once
// SIMULATION ONLY: no audio, MP3 command-frame or UART response emulation.
#include <Arduino.h>
inline void SelectPlayerDevice(uint8_t) {}
inline void SetVolume(uint8_t) {}
inline void SpecifyMusicPlay(uint8_t, uint8_t) {}
inline void PlayNext() {}
