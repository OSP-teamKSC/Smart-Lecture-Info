let colorIndex = 0;
const colorlist = ['#034C8C', '#70735D', '#F2B705', '#F29F05', '#F28705', '#959DE8', '#E687D2'];

const evalTypes = ['출석','중간 시험','기말 시험','과제','발표','토론','안전 교육','안전 교육','기타'];
const evalColors = ['#d74949','#D6D6CE','#FFB547','#ADB17D','#5B8FA8','#D49464','#B1746F','#8A8B79','#725663'];

const overlapColor = 'rgb(255, 0, 0)';
const backColor = 'rgb(204, 204, 204)';
const selectNewColor = '#DD5555';
const selectScheduleColor = 'rgba(30,169,133,0.6)'

const TableBody = document.getElementById("tb")
const ScheduleTable = document.getElementById("schedule")
const defColor = schedule.children[0].children[0].style.background;
const Selects = document.getElementById('selects')
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
        HideButton.innerHTML = '▲'
        HeaderPanel.style.marginTop = '5px';
        isHidden = false;
    }
    else {
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
        for (time of activatedSubject.Schedule) {
            time.clearColor();
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
        return
    }
    navigator.clipboard.writeText(ClassCodeLabel.innerHTML.replace('-',''))
}

addSelect('-대학-', univs);

addSelect('-대학-', ituniv);

for(r of ScheduleTable.children){
    for(c of r.children){
        c.onclick = DeselectSchedule;
    }
}

RemoveSubjectButton.style.visibility = 'hidden'