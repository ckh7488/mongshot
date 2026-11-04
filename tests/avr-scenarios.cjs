const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {Runner}=require('../simulation/source/runner.js');
const firmware=require('./firmware-data.json');
const results=[];
function record(name,run){const t=Date.now();run();results.push({name,pass:true,wallMs:Date.now()-t});console.log('PASS',name);}
record('Original 2ms accepts a 20ms frame pulse',()=>{const r=new Runner(firmware.original);r.runMs(1100);r.setInputs({frame:true});r.runMs(20);assert.equal(r.stage,1);});
record('Candidate 10ms rejects a 20ms pulse, accepts a sustained input',()=>{const r=new Runner(firmware.candidate);r.runMs(1100);r.setInputs({frame:true});r.runMs(20);r.setInputs({frame:false});r.runMs(80);assert.equal(r.stage,0);r.setInputs({frame:true});r.runMs(70);assert.equal(r.stage,1);assert.equal(r.pin(12),1);});
record('Approved D11/D17 removal leaves input pins; original drives them',()=>{for(const mode of ['original','candidate']){const r=new Runner(firmware[mode]);r.runMs(1100);assert.equal(r.pin(11),mode==='original'?0:null);assert.equal(r.pin(17),mode==='original'?1:null);}});
record('Real firmware completes all five puzzle stages and preserves delays',()=>{
 const r=new Runner(firmware.candidate);r.runMs(1100);
 assert.deepEqual([r.pin(4),r.pin(5),r.pin(16)],[0,1,1]);
 r.setInputs({frame:true});r.runMs(70);assert.equal(r.stage,1);
 for(let i=0;i<3;i++){r.setInputs({light:100});r.runMs(70);if(i<2){r.setInputs({light:900});r.runMs(70);}}
 assert.equal(r.lightCount,3);assert.equal(r.stage,2);assert.equal(r.pin(10),0);
 r.runMs(19800);assert.equal(r.pin(10),0);r.runMs(300);assert.equal(r.pin(10),1);
 r.setInputs({key:0});r.runMs(70);assert.equal(r.stage,3);assert.deepEqual([r.pin(4),r.pin(5),r.pin(16)],[1,0,1]);
 r.setInputs({rfid:0});r.runMs(70);assert.equal(r.stage,4);assert.equal(r.pin(18),1);
 r.runMs(1100);r.setInputs({book:true});r.runMs(70);assert.equal(r.stage,5);assert.equal(r.pin(9),0);
 r.runMs(250);assert.equal(r.pin(9),1);r.runMs(10200);assert.equal(r.stage,5);
 const before=r.snapshot();r.setInputs({frame:false,book:false,light:900,key:900,rfid:900});r.runMs(100);assert.equal(r.stage,before.stage);
});
const out={engine:'avr8js@0.21.1',target:'ATmega328P / 16MHz',core:'arduino:avr@1.8.8',mp3:'stubbed; not validated',results};
fs.writeFileSync(path.join(__dirname,'verification.json'),JSON.stringify(out,null,2));
console.log(JSON.stringify({passed:results.length,total:results.length}));
