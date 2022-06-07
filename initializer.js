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
const SearchOption = document.getElementById('searchOption')
const OptionPanel = document.getElementById('optionPanel')
const EvaluationRatioPanel = document.getElementById('evalRatio')
const RemoveSubjectButton = document.getElementById('removeSchedule')
const DetailPanel = document.getElementById('details')

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
const SearchText = document.getElementById('searchText');



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
    if (OptionPanel.style.display === 'none')
        OptionPanel.style.display = 'block'}

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
        savedSchedules.splice(index, 1);
    }
    DeselectSchedule();
}

SearchButton.onclick = Search;

document.getElementById('optionClose').onclick = ()=>{
    if (OptionPanel.style.display !== 'none')
        OptionPanel.style.display = 'none'}

document.getElementById("addSchedule").onclick = AddToSchedule

document.getElementById("codeCopy").onclick = ()=>{
    if (!navigator.clipboard) {
        // Clipboard API not available
        let _t = ClassCodeLabel.innerHTML.replace('-','');

        let textArea = document.createElement("textarea");
        textArea.value = text;

        // Avoid scrolling to bottom
        textArea.style.top = "0";
        textArea.style.left = "0";
        textArea.style.position = "fixed";

        document.body.appendChild(_t);
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