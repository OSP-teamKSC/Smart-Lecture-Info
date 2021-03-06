let colorIndex = 0;
let colorUsage = [false,false,false,false,false,false,false,false,false]
const colorlist = ['#8a8a8a','#EC5f67', '#AB7967', '#FAC863', '#C594C5', '#99C794', '#F99157', '#5FB3B3', '#6699CC'];

const evalTypes = ['출석','중간 시험','기말 시험','과제','발표','토론','안전 교육','안전 교육','기타'];
const evalColors = ['#d74949','#D6D6CE','#FFB547','#ADB17D','#5B8FA8','#D49464','#B1746F','#8A8B79','#725663'];

const overlapColor = 'rgb(199,0,0)';
const backColor = 'rgb(204, 204, 204)';
const selectNewColor = '#DD5555';
const selectScheduleColor = 'rgba(63,63,63,0.6)'

const TableBody = document.getElementById("tb")
const ScheduleTable = document.getElementById("schedule")
const defColor = schedule.children[0].children[0].style.background;
const SearchButton = document.getElementById('search')
const HideButton = document.getElementById('hide')
const HeaderPanel = document.getElementById('header')
const MainPanel = document.getElementById('mainwrapper')
const SearchOption = document.getElementById('searchOption')
const OptionPanel = document.getElementById('optionOverlay')
const OptionPanel2 = document.getElementById('optionPanel')
const EvaluationRatioPanel = document.getElementById('evalRatio')
const RemoveSubjectButton = document.getElementById('removeSchedule')
const DetailPanel = document.getElementById('details')

const TotalCreditLabel = document.getElementById('totalCredit')
const UnivAndDepartsLabel = document.getElementById('univAndDeparts')
const IsUntactLabel = document.getElementById('isUntactLabel')
const ApplicantsLabel = document.getElementById('applicantsLabel')
const ProfessorsLabel = document.getElementById('professors')
const PriorSubjLabel = document.getElementById('priorSubj')
const SubsequentSubjLabel = document.getElementById('subSubj')
const SubjNameLabel = document.getElementById('subjName')
const ClassCodeLabel = document.getElementById('classCode')


const Radio1 = document.getElementById('radio1');
const Radio2 = document.getElementById('radio2');
const RadioEnable = document.getElementById('onlyUntact');
const NoOverwhelmed = document.getElementById('exceptOverwhelmed');
const NoConflictWithSchedule = document.getElementById('noConflictWithSchedule');
const SearchTextExcept = document.getElementById('exceptText');
const ClassCodeText = document.getElementById('classCodefilter');
const NoFirstGrade = document.getElementById('except1st');
const SearchText = document.getElementById('searchText');

let checks = []
let nums = []
let opts = []
for (_i in [0,1,2,3,4,5]){
    checks.push(document.getElementById(_i+'check'))
    nums.push(document.getElementById(_i+'num'))
    nums[_i].disabled=true;
    opts.push(document.getElementById(_i+'sel'))
    opts[_i].disabled=true;
    const _t = _i;
    checks[_t].onchange = ()=>{nums[_t].disabled=!checks[_t].checked; opts[_t].disabled=!checks[_t].checked;}
}


RadioEnable.onchange= ()=>{
    if(RadioEnable.checked){
        Radio1.disabled=false;
        Radio2.disabled=false;
        Radio1.checked=true;
    }
    else{
        Radio1.disabled=true;
        Radio2.disabled=true;
        Radio1.checked=false;
        Radio2.checked=false;
    }
    Radio1.disabled= !RadioEnable.checked;Radio2.disabled= !RadioEnable.checked;
}
let isHidden = false;
let subjects = []
let selectedSubject = null;
let activatedSubject = null;
let selectedRow = null;
let savedSchedules = []
let addable = false;
let totalCredit = 0;

HideButton.onclick = ()=>{
    if (isHidden) {
        HideButton.style.transform = 'translate(-50%,0)'
        HideButton.innerHTML = '▲'
        HeaderPanel.style.marginTop = '5px';
        isHidden = false;
    }
    else {
        HideButton.style.transform = 'translate(-50%,-175px)'
        HideButton.innerHTML = '▼'
        HeaderPanel.style.marginTop = '-170px';
        isHidden = true;
    }
}

SearchOption.onclick = ()=> {
    if (OptionPanel.style.visibility === 'hidden'){
        OptionPanel.style.visibility = 'visible'
        OptionPanel.style.background = '#000000AA'
        OptionPanel.style.transition='background 0.2s ease-out'
        OptionPanel2.style.transition='transform 0.3s'


        OptionPanel2.style.transform = 'translate(-50%, -50%)'
        HeaderPanel.style.zIndex=-1;
        MainPanel.style.zIndex=-3;
        HideButton.style.zIndex=-2;
    }
}

RemoveSubjectButton.onclick = ()=>{
    let index= savedSchedules.indexOf(activatedSubject);
    if(index>-1) {
        colorUsage[colorlist.indexOf(activatedSubject.Color)]= false;
        for(_time of activatedSubject.Schedule){
            _time.clearScheduleCallback();
        }
        for (_time of activatedSubject.Schedule) {
            _time.clearColor();
        }

        totalCredit -= parseInt(savedSchedules[index].Credit);
        TotalCreditLabel.innerHTML = "총 학점 : "+totalCredit;
        savedSchedules.splice(index, 1);

    }
    DeselectSchedule();
}

SearchButton.onclick = Search;

document.getElementById('optionClose').onclick = ()=>{
    if (OptionPanel.style.visibility !== 'hidden') {
        OptionPanel.style.transition=''
        OptionPanel2.style.transition=''
        OptionPanel.style.background = '#00000000'
        OptionPanel2.style.transform = 'translate(-50%, -45%)'
        OptionPanel.style.visibility = 'hidden'
        HeaderPanel.style.zIndex=3;
        MainPanel.style.zIndex=1;
        HideButton.style.zIndex=2;
    }}

document.getElementById("addSchedule").onclick = AddToSchedule

document.getElementById("codeCopy").onclick = ()=>{
    if (!navigator.clipboard) {
        // Clipboard API not available
        let _t = ClassCodeLabel.innerHTML.replace('-','');

        let textArea = document.createElement("textarea");
        textArea.value = _t;

        // Avoid scrolling to bottom
        textArea.style.top = "0";
        textArea.style.left = "0";
        textArea.style.position = "fixed";

        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();

        try {
            let successful = document.execCommand('copy');
            let msg = successful ? 'successful' : 'unsuccessful';
            console.log('Fallback: Copying text command was ' + msg);
        } catch (err) {
            console.error('Fallback: Oops, unable to copy', err);
        }

        document.body.removeChild(textArea);
        return
    }
    navigator.clipboard.writeText(ClassCodeLabel.innerHTML.replace('-',''))
}

for(r of ScheduleTable.children){
    for(c of r.children){
        c.onclick = DeselectSchedule;
    }
}

RemoveSubjectButton.style.visibility = 'hidden'

