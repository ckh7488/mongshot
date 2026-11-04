const assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path');
const {Runner}=require('../simulation/source/runner.js');
const firmware=require('./firmware-data.json');
const results=[];
function test(name,fn){fn();results.push({name,pass:true});console.log('PASS',name);}
const boot=()=>{const r=new Runner(firmware.frontpanel);r.runMs(1200);return r;};
const hold=(r,ms=2100)=>{r.setInputs({manual:true});r.runMs(ms);};
const release=r=>{r.setInputs({manual:false});r.runMs(50);};
test('Real 74HC595 latch has one current-stage LED',()=>{const r=boot();assert.equal(r.stage,0);assert.equal(r.ledMask,1);assert.ok(r.ledLatches>0);r.setInputs({frame:true});r.runMs(80);assert.equal(r.stage,1);assert.equal(r.ledMask,2);});
test('Brief manual press and contact bounce do not advance',()=>{const r=boot();hold(r,1200);release(r);assert.equal(r.stage,0);for(let i=0;i<10;i++){r.setInputs({manual:true});r.runMs(10);r.setInputs({manual:false});r.runMs(10);}assert.equal(r.stage,0);assert.equal(r.word('manualCount'),0);});
test('Two-second hold advances once, continuing hold never repeats',()=>{const r=boot();hold(r);assert.equal(r.stage,1);assert.equal(r.word('manualCount'),1);assert.equal(r.pin(12),1);r.runMs(6000);assert.equal(r.stage,1);assert.equal(r.word('manualCount'),1);});
test('Manual advances preserve every normal output and timed delay',()=>{
 const r=boot();hold(r);release(r);hold(r);assert.equal(r.stage,1);assert.equal(r.word('phase'),3);assert.equal(r.pin(10),0);
 release(r);r.runMs(19800);assert.equal(r.pin(10),0);r.runMs(350);assert.equal(r.stage,2);assert.equal(r.pin(10),1);assert.equal(r.ledMask,4);
 hold(r);assert.equal(r.stage,3);assert.deepEqual([r.pin(4),r.pin(5),r.pin(16)],[1,0,1]);release(r);
 hold(r);assert.equal(r.stage,4);assert.equal(r.pin(18),1);r.runMs(1100);release(r);
 hold(r);assert.equal(r.stage,5);assert.equal(r.pin(9),0);r.runMs(250);assert.equal(r.pin(9),1);r.runMs(10200);assert.equal(r.word('phase'),9);assert.equal(r.ledMask,32);assert.equal(r.word('manualCount'),5);
});
test('A hold during timed wait is consumed, not queued for the next stage',()=>{
 const r=boot();r.setInputs({frame:true});r.runMs(70);for(let i=0;i<3;i++){r.setInputs({light:0});r.runMs(70);if(i<2){r.setInputs({light:900});r.runMs(70);}}
 assert.equal(r.word('phase'),3);hold(r);r.runMs(18300);assert.equal(r.stage,2);assert.equal(r.word('manualCount'),0);r.runMs(3000);assert.equal(r.stage,2);
});
test('Original sensor sequence works with front panel and nonblocking waits',()=>{
 const r=boot();r.setInputs({frame:true});r.runMs(70);for(let i=0;i<3;i++){r.setInputs({light:0});r.runMs(70);if(i<2){r.setInputs({light:900});r.runMs(70);}}r.runMs(20100);assert.equal(r.stage,2);
 r.setInputs({key:0});r.runMs(70);assert.equal(r.stage,3);r.setInputs({rfid:0});r.runMs(70);assert.equal(r.stage,4);r.runMs(1100);r.setInputs({book:true});r.runMs(70);assert.equal(r.stage,5);r.runMs(10400);assert.equal(r.word('phase'),9);assert.equal(r.word('manualCount'),0);
});
fs.writeFileSync(path.join(__dirname,'frontpanel-verification.json'),JSON.stringify({engine:'avr8js@0.21.1',target:'ATmega328P / 16MHz',mp3:'simulation stub',results},null,2));
console.log(JSON.stringify({passed:results.length,total:results.length}));
