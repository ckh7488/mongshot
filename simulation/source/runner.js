/* SPDX-License-Identifier: MIT — MONG SHOT simulator integration */
(function(root,factory){
  if(typeof module==='object'&&module.exports) module.exports=factory(require('avr8js'));
  else root.MongshotAVR=factory(root.AVR8);
})(typeof globalThis!=='undefined'?globalThis:this,function(AVR){
  'use strict';
  const HZ=16000000;
  const PIN={8:['b',0],6:['d',6],12:['b',4],10:['b',2],9:['b',1],18:['c',4],4:['d',4],5:['d',5],16:['c',2],11:['b',3],17:['c',3],7:['d',7],13:['b',5]};
  class Runner{
    constructor(firmware){
      this.firmware=firmware;
      const flash=new Uint16Array(16384),bytes=new Uint8Array(flash.buffer);
      let upper=0;
      for(const line of firmware.hex.trim().split(/\r?\n/)){
        if(line[0]!==':')continue;
        const n=parseInt(line.slice(1,3),16),addr=parseInt(line.slice(3,7),16),type=parseInt(line.slice(7,9),16);
        if(type===4)upper=parseInt(line.slice(9,13),16)<<16;
        if(type===0)for(let i=0;i<n;i++)bytes[upper+addr+i]=parseInt(line.slice(9+i*2,11+i*2),16);
      }
      this.cpu=new AVR.CPU(flash);
      this.timers=[new AVR.AVRTimer(this.cpu,AVR.timer0Config),new AVR.AVRTimer(this.cpu,AVR.timer1Config),new AVR.AVRTimer(this.cpu,AVR.timer2Config)];
      this.ports={b:new AVR.AVRIOPort(this.cpu,AVR.portBConfig),c:new AVR.AVRIOPort(this.cpu,AVR.portCConfig),d:new AVR.AVRIOPort(this.cpu,AVR.portDConfig)};
      this.adc=new AVR.AVRADC(this.cpu,AVR.adcConfig);
      this.uart=new AVR.AVRUSART(this.cpu,AVR.usart0Config,HZ);
      this.serial=[];this.line='';this.events=[];
      this.uart.onByteTransmit=v=>{if(v===10){this.serial.push({ms:this.ms,text:this.line.replace(/\r/g,'')});this.line='';}else this.line+=String.fromCharCode(v);};
      this.inputs={frame:false,light:900,key:900,rfid:900,book:false,manual:false};
      this.ledShift=0;this.ledMask=0;this.ledLatches=0;
      if(firmware.frontpanel){
        this.ports.b.addListener((value,old)=>{if((value&32)&&!(old&32))this.ledShift=((this.ledShift<<1)|((value&8)?1:0))&255;});
        this.ports.d.addListener((value,old)=>{if((value&128)&&!(old&128)){this.ledMask=this.ledShift;this.ledLatches++;}});
      }
      this.setInputs(this.inputs);
    }
    get ms(){return this.cpu.cycles/HZ*1000;}
    word(name){const a=this.firmware.symbols[name];return a===undefined?0:(this.cpu.data[a]|(this.cpu.data[a+1]<<8));}
    get stage(){return this.word('pass');}
    get lightCount(){return this.word('count');}
    pin(pin){const [port,bit]=PIN[pin];const state=this.ports[port].pinState(bit);return state===AVR.PinState.High?1:state===AVR.PinState.Low?0:null;}
    setInputs(values){
      Object.assign(this.inputs,values);
      this.ports.b.setPin(0,!this.inputs.frame);
      this.ports.d.setPin(6,!this.inputs.book);
      if(this.firmware.frontpanel)this.ports.c.setPin(3,!this.inputs.manual);
      for(const [name,ch] of [['light',0],['key',1],['rfid',5]])this.adc.channelValues[ch]=Math.max(0,Math.min(1023,this.inputs[name]))*5/1024;
    }
    runMs(ms){
      const end=this.cpu.cycles+Math.round(ms*HZ/1000);
      while(this.cpu.cycles<end){AVR.avrInstruction(this.cpu);this.cpu.tick();}
      return this.snapshot();
    }
    snapshot(){return {ms:this.ms,stage:this.stage,phase:this.word('phase'),manualCount:this.word('manualCount'),ledMask:this.ledMask,lightCount:this.lightCount,pins:Object.fromEntries([12,10,9,18,4,5,16,11,17,7,13].map(p=>[p,this.pin(p)])),inputs:{...this.inputs}};}
  }
  return {Runner,HZ};
});
