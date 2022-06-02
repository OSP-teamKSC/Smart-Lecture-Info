let colorIndex = 0;
const colorlist = ['#034C8C', '#70735D', '#F2B705', '#F29F05', '#F28705', '#959DE8', '#E687D2'];

class Subject {
    constructor(dict) {
        this.Grade = 1;
        this.Gubun = dict['Gubun']
        this.University = dict['EstablishedUniversity']
        this.Department = dict['EstablishedDepartment']
        this.ClassID = dict['ClassCode']
        this.Name = dict['SubjectName']
        this.Credit = dict['Credit']
        this.Professor = dict['ProfessorNames'].split(',');
        this.Schedule = scheduleFromString(dict['Schedule']);
        this.TotalStudent = dict['ApplicantsMax'];
        this.CurrentStudent = dict['ApplicantsCurrent'];
        this.Box = "Y";
        this.IsTact = dict['IsUntact'] == 'Y' ? "비대면" : "대면";
        this.Color = colorlist[colorIndex]
        colorIndex = (colorIndex + 1) % colorlist.length;
    }

}

let isHidden = false;
let subjects = []

var selectedSubject = null;
var selectedRow = null;

var savedSchedules = []
var addable = false;

const overlapColor = 'rgb(255, 0, 0)';
const backColor = 'rgb(204, 204, 204)';

const TableBody = document.getElementById("tb")
const ScheduleTable = document.getElementById("schedule")
const defColor = schedule.children[0].children[0].style.background;
const Selects = document.getElementById('selects')
const SearchButton = document.getElementById('search')
const HideButton = document.getElementById('hide')
const HeaderPanel = document.getElementById('header')


function SchedulesToString(sches) {
    let _s = '';
    for (_schedule of sches) {
        _s += _schedule.toString();
        _s += "<br>"
    }
    return _s;
}

function AddToSchedule() {
    if (addable == true) {
        savedSchedules.push(selectedSubject);
        addable = false;
        selectedSubject = null;
        DrawAll();
    }
}

function DrawAll() {
    for (_schedule of savedSchedules) {
        for (_t of _schedule.Schedule) {
            _t.fillColor(_schedule.Color, _schedule.Name)
        }
    }
}

function ProfessorsToString(professors) {
    let _s = '';
    for (_profs of professors) {
        _s += _profs;
        _s += "<br>";
    }
    return _s;
}

function AddTableD(_tr, _s) {
    var _Td = document.createElement('td')
    _Td.innerHTML = _s;
    _tr.appendChild(_Td);
}

function SubjectDetail(sb) {
    if (selectedSubject != null) {
        for (time of selectedSubject.Schedule) {
            time.clearColor();
        }
    }
    DrawAll();
    selectedSubject = sb;
    addable = true;
    for (_t of sb.Schedule) {
        if (_t.checkOverrideWithSchedule(savedSchedules) == true) {
            _t.fillColor(overlapColor, sb.Name);
            addable = false;
        } else {
            _t.fillColor('#DD5555', sb.Name);
        }
    }
}

function ColorTable(day, time, color, text='') {
    let k = ScheduleTable.children[time]
    if (time % 2 == 0) {
        k.children[day + 1].style.background = color;
        k.children[day + 1].innerHTML = text;
    } else {
        k.children[day].style.background = color;
        k.children[day].innerHTML = text;
    }
}

function ClearTable(day, time) {
    let k = ScheduleTable.children[time]
    if (time % 2 == 0) {
        k.children[day + 1].style.background = backColor
        k.children[day + 1].innerHTML = '';
    } else {
        k.children[day].style.background = backColor;
        k.children[day].innerHTML = '';
    }
}

function AddTableRow(subject) {
    var newTr = document.createElement('tr')
    newTr.classList.add('row')
    newTr.onclick = function() {
        if (selectedRow != null) {
            selectedRow.style.background = ''
        }
        newTr.style.background = '#888888';
        selectedRow = newTr;
        SubjectDetail(subject);
    }
    TableBody.appendChild(newTr)
    AddTableD(newTr, subject.Grade)
    AddTableD(newTr, subject.Gubun)
    AddTableD(newTr, subject.University)
    AddTableD(newTr, subject.Department)
    AddTableD(newTr, subject.ClassID)
    AddTableD(newTr, subject.Name)
    AddTableD(newTr, subject.Credit)
    AddTableD(newTr, ProfessorsToString(subject.Professor))
    AddTableD(newTr, SchedulesToString(subject.Schedule))
    AddTableD(newTr, subject.TotalStudent)
    AddTableD(newTr, subject.CurrentStudent)
    AddTableD(newTr, subject.Box)
    AddTableD(newTr, subject.IsTact)
}

function ReloadTable(data) {
    while (subjects.length > 0)
        subjects.pop();

    //data json
    for(i in data)
    {
        console.log(data[i]);
    }

    for (d of glsos) {
        console.log(d);
        sb = new Subject(d)
        override = false;
        for (t of sb.Schedule) {
            if (t.checkOverrideWithSchedule(savedSchedules)) {
                override = true;
                break;
            }
        }
        if (!override)
            subjects.push(sb)
    }
    while (TableBody.children.length > 0)
        TableBody.children[0].remove();
    for (_subject of subjects)
        AddTableRow(_subject);

    DrawAll();
}

SearchButton.onclick = function(){
    const searchFilter = {
    'semester': IdSeme.value,
    'university': IdUniv.value,
    'college': IdCollege.value,
    'major': IdMajor.value,
    'Core': IdCore.value,
    };

    //XMLHttpRequest 객체 생성
    const xhr = new XMLHttpRequest();
    //요청을 보낼 방식, url, 비동기여부 설정
                        //서버 주소
    xhr.open('post', 'http://192.168.1.103:8080/request', true);
     //HTTP 요청 헤더 설정
    xhr.setRequestHeader('Content-type', 'application/json');
    //요청 전송
    xhr.send(JSON.stringify(searchFilter));
    //Response Type을 Json으로 사전 정의
    xhr.responseType = "json";
     //Callback
    xhr.onload = () => {
        if (xhr.status == 200) {
            //success
            //console.log(JSON.stringify(xhr.response));
            ReloadTable(xhr.response);
        } else {
            //failed
        }
    }
}
// ReloadTable();

document.getElementById("addSchedule").onclick = AddToSchedule


function addSelect(s1, json) {
    var newselect = document.createElement('select')
    var _top = document.createElement('option')
    _top.selected = true;
    _top.innerHTML = s1;
    newselect.appendChild(_top)
    for (_t of json) {
        var _opt = document.createElement('option')
        _opt.innerHTML = _t['name'];
        newselect.appendChild(_opt)
    }
    selects.appendChild(newselect)
}
HideButton.onclick = function(){
    if(isHidden){
        HideButton.innerHTML = '숨기기'
        HeaderPanel.style.marginTop = '5px';
        isHidden = false;
    }
    else{
        HideButton.innerHTML = '보이기'
        HeaderPanel.style.marginTop = '-125px';
        isHidden = true;        
    }
}
