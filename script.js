
class Subject {
    constructor(dict, alt) {
        this.rates = [];
        this.Grade = 1;
        this.Gubun = dict['Gubun']
        this.University = dict['EstablishedUniversity']
        this.Department = dict['EstablishedDepartment']
        this.ClassID = dict['ClassCode']
        this.Name = dict['SubjectName']
        this.Credit = dict['Credit']
        this.Professor = dict['ProfessorNames'].split(',');
        this.Schedule = scheduleFromString(dict['Schedule'],alt);
        this.TotalStudent = dict['ApplicantsMax'];
        this.CurrentStudent = dict['ApplicantsCurrent'];
        this.IsTact = (dict['IsUntact']==='Y')?"비대면":"대면";
        this.rates.push(parseInt(dict['Rate1']));
        this.rates.push(parseInt(dict['Rate2']));
        this.rates.push(parseInt(dict['Rate3']));
        this.rates.push(parseInt(dict['Rate4']));
        this.rates.push(parseInt(dict['Rate5']));
        this.rates.push(parseInt(dict['Rate6']));
        this.rates.push(parseInt(dict['Rate7']));
        this.rates.push(parseInt(dict['Rate8']));
        this.rates.push(parseInt(dict['Rate9']));
        this.PriorSubject = dict['PriorSubject'];
        this.SubsequentSubject = dict['SubsequentSubject'];
        this.Color = colorlist[colorIndex]
        colorIndex = (colorIndex + 1) % colorlist.length;
    }
}

function SchedulesToString(sches) {
    let _s = '';
    for (_schedule of sches) {
        _s += _schedule.toString();
        _s += "<br>"
    }
    return _s;
}

function AddToSchedule() {
    if (addable === true) {
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

function AddRatio(ratio, tooltip, color){
    let _span = document.createElement('span');
    _span.classList.add('ratioBar');
    _span.style.background = color;
    _span.style.width = ratio+'%';
        _span.innerHTML = ratio;
    let _tooltip = document.createElement('span');
    _tooltip.innerHTML = tooltip;
    _tooltip.classList.add('tooltiptext');

    EvaluationRatioPanel.appendChild(_span);
    _span.appendChild(_tooltip);
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
        if (_t.checkOverrideWithSchedule(savedSchedules) === true) {
            _t.fillColor(overlapColor, sb.Name);
            addable = false;
        } else {
            _t.fillColor('#DD5555', sb.Name);
        }
    }
}

function ColorTable(day, time, color, text='') {
    let k = ScheduleTable.children[time]
    if (time % 2 === 0) {
        k.children[day + 1].style.background = color;
        k.children[day + 1].innerHTML = text;
    } else {
        k.children[day].style.background = color;
        k.children[day].innerHTML = text;
    }
}

function ClearTable(day, time) {
    let k = ScheduleTable.children[time]
    if (time % 2 === 0) {
        k.children[day + 1].style.background = backColor
        k.children[day + 1].innerHTML = '';
    } else {
        k.children[day].style.background = backColor;
        k.children[day].innerHTML = '';
    }
}

function AddTableD(_tr, _s) {
    let _Td = document.createElement('td')
    _Td.innerHTML = _s;
    _tr.appendChild(_Td);
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
        SetDetails(subject);
    }
    newTr.ondblclick = AddToSchedule
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
    AddTableD(newTr, subject.TotalStudent+'/'+subject.CurrentStudent)
    AddTableD(newTr, subject.IsTact)
}

function TestLoad(){
    _result = []
    for (d of glsos) {
        sb = new Subject(d,false)
        override = false;
        for (t of sb.Schedule) {
            if (t.checkOverrideWithSchedule(savedSchedules)) {
                override = true;
                break;
            }
        }
        if (!override)
            _result.push(sb)
    }
    return _result
}

function ReloadTable(datas) {
    while (subjects.length > 0)
        subjects.pop();
    while (TableBody.children.length > 0)
        TableBody.children[0].remove();

    for (_subject of datas) {
        subjects.push(_subject)
        AddTableRow(_subject);
    }

    DrawAll();
}

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

function SetDetails(sbject){
    while (EvaluationRatioPanel.children.length > 0)
        EvaluationRatioPanel.children[0].remove();
    for(let i = 0;i<9;i++){
        if(sbject.rates[i]!==0){
            AddRatio(sbject.rates[i],evalTypes[i],evalColors[i]);
        }
    }

    details.children[3].innerHTML = '권장 선수 과목 : ' + sbject.PriorSubject;
    details.children[4].innerHTML = '권장 후수 과목 : ' + sbject.SubsequentSubject;
}

function hideAndShowOption(){
    
}
