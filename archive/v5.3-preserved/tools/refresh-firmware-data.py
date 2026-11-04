"""Prepare source wrappers or refresh embedded firmware from standard AVR ELF/HEX.
Only Python's standard library is needed. MP3 stubs are simulation-only.
"""
from pathlib import Path
import json,struct,sys
ROOT=Path(__file__).resolve().parents[1]
if '--prepare' in sys.argv:
    for mode,src in [('original','firmware/original/operating/operating.ino'),('candidate','firmware/candidate_10ms/candidate_10ms.ino'),('frontpanel','firmware/frontpanel/frontpanel.ino')]:
        folder=ROOT/'simulation/firmware'/mode
        folder.mkdir(parents=True,exist_ok=True)
        (folder/(mode+'.ino')).write_text('// Simulation entry point. See source.cpp.\n',encoding='utf-8')
        (folder/'source.cpp').write_text('#include <Arduino.h>\nvoid last();\n'+(ROOT/src).read_text(encoding='utf-8-sig'),encoding='utf-8')
        (folder/'MP3Player_KT403A.h').write_text('''#pragma once
// SIMULATION ONLY: no audio, MP3 command-frame or UART response emulation.
#include <Arduino.h>
inline void SelectPlayerDevice(uint8_t) {}
inline void SetVolume(uint8_t) {}
inline void SpecifyMusicPlay(uint8_t, uint8_t) {}
inline void PlayNext() {}
''',encoding='utf-8')
    print('Prepared simulation source wrappers')
    raise SystemExit(0)

def symbols_from_elf(path):
    data=path.read_bytes()
    assert data[:5]==b'\x7fELF\x01' and data[5]==1,'ELF32 little-endian required'
    head=struct.unpack_from('<16sHHIIIIIHHHHHH',data)
    shoff,shsize,shnum=head[6],head[11],head[12]
    sections=[struct.unpack_from('<IIIIIIIIII',data,shoff+i*shsize) for i in range(shnum)]
    found={}
    for section in sections:
        if section[1]!=2:continue
        strings=sections[section[6]]
        stringdata=data[strings[4]:strings[4]+strings[5]]
        for offset in range(section[4],section[4]+section[5],section[9]):
            name,value,size,info,other,shndx=struct.unpack_from('<IIIBBH',data,offset)
            text=stringdata[name:stringdata.find(b'\0',name)].decode(errors='replace')
            if text in ['pass','count','lastSampleMs','phase','manualCount']:found[text]=value-0x800000
    assert 'pass' in found and 'count' in found,'SRAM symbols unavailable'
    return found
firmware={}
for mode in ['original','candidate','frontpanel']:
    folder=ROOT/'simulation/firmware'
    firmware[mode]={'hex':(folder/(mode+'.hex')).read_text(),'symbols':symbols_from_elf(folder/(mode+'.elf')),'sampleMs':2 if mode=='original' else 10,'frontpanel':mode=='frontpanel','core':'arduino:avr@1.8.8','target':'arduino:avr:uno','mp3':'simulation stub'}
(ROOT/'simulation/source/firmware-data.js').write_text('window.MONGSHOT_FIRMWARE='+json.dumps(firmware,separators=(',',':'))+';\n',encoding='utf-8')
(ROOT/'tests/firmware-data.json').write_text(json.dumps(firmware,indent=2),encoding='utf-8')
print('Refreshed firmware and SRAM symbols')
