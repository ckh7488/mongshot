/* Dimensional envelope check. Never treats photo estimates as measurements. */
(()=>{'use strict';
const $=id=>document.getElementById(id), get=id=>Number($(id).value);
function check(){
 const ids=['fit-width','fit-upper','fit-lower','fit-depth','fit-rfid-w','fit-rfid-h','fit-rfid-d','fit-amp-w','fit-amp-h','fit-amp-d'];
 const out=$('fit-result');
 if(ids.some(id=>!Number.isFinite(get(id))||get(id)<=0)){out.className='fit-result bad';out.textContent='모든 치수를 양수 mm로 입력하세요.';return;}
 const limits=[['유효 폭',get('fit-width'),400],['상부 높이',get('fit-upper'),260],['하부 높이',get('fit-lower'),650],['유효 깊이',get('fit-depth'),120]];
 const fail=limits.filter(x=>x[1]<x[2]).map(x=>`${x[0]} ${x[2]-x[1]}mm 부족`);
 for(const [id,max,name] of [['fit-rfid-w',260,'RFID 폭'],['fit-rfid-h',180,'RFID 높이'],['fit-rfid-d',90,'RFID 깊이'],['fit-amp-w',180,'앰프 폭'],['fit-amp-h',90,'앰프 높이'],['fit-amp-d',50,'앰프 깊이']])if(get(id)>max)fail.push(`${name} 확보 검토값보다 ${get(id)-max}mm 큼`);
 out.className='fit-result '+(fail.length?'bad':'conditional');
 out.textContent=fail.length?'현재 배치 수정 필요 · '+fail.join(' / '):'입력한 치수에서는 확보 영역 조건 충족 · 실측/관통구/방열 확인 전 설치 확정 아님';
}
document.querySelectorAll('.fit-inputs input').forEach(el=>el.addEventListener('input',check));check();
})();
