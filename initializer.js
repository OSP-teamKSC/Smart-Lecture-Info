let colorIndex = 0;
const colorlist = ['#034C8C', '#70735D', '#F2B705', '#F29F05', '#F28705', '#959DE8', '#E687D2'];

const evalTypes = ['출석','중간 시험','기말 시험','과제','발표','토론','안전 교육','안전 교육','기타'];
const evalColors = ['#800000','#D6D6CE','#FFB547','#ADB17D','#5B8FA8','#D49464','#B1746F','#8A8B79','#725663'];

const overlapColor = 'rgb(255, 0, 0)';
const backColor = 'rgb(204, 204, 204)';

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
const DetailPanel = document.getElementById('details')

let isHidden = false;
let subjects = []
let selectedSubject = null;
let selectedRow = null;
let savedSchedules = []
let addable = false;

HideButton.onclick = function () {
    if (isHidden) {
        HideButton.innerHTML = '숨기기'
        HeaderPanel.style.marginTop = '5px';
        isHidden = false;
    }
    else {
        HideButton.innerHTML = '보이기'
        HeaderPanel.style.marginTop = '-125px';
        isHidden = true;
    }
}

SearchOption.onclick = function () {
    if (OptionPanel.style.display === 'none')
        OptionPanel.style.display = 'block'
    else
        OptionPanel.style.display = 'none'

}

SearchButton.onclick = function(){
    ReloadTable(TestLoad());
}


document.getElementById("addSchedule").onclick = AddToSchedule


addSelect('-대학-', univs);
addSelect('-대학-', ituniv);
