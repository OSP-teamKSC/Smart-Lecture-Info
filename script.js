
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
            _t.fillColor(selectNewColor, sb.Name);
        }
    }
}

function AddToSchedule() {
    if (addable === true) {
        let _color;
        for(let i =8;i>=0;i--){
            if(colorUsage[i]===false){
                _color = i;
                break;
            }
        }
        selectedSubject.Color = colorlist[_color];
        colorUsage[_color] = true;
        savedSchedules.push(selectedSubject);
        for (_t of selectedSubject.Schedule) {
            _t.setScheduleCallback(selectedSubject)
        }
        addable = false;
        SelectFromSchedule(selectedSubject);
    }
}

function GetScheduleCell(row,col){
    if (row % 2 === 0) {
        return ScheduleTable.children[row].children[col + 1]
    } else {
        return ScheduleTable.children[row].children[col]
    }
}

function ColorTable(day, time, color, text='') {
    let k = GetScheduleCell(time,day)
    k.style.background = color;
    k.innerHTML = text;
}

function SetTableOnclick(day, time, func=()=>{DeselectSchedule();},schedule=null) {
    let k = GetScheduleCell(time,day)
    if(schedule==null){
        k.onclick = () =>{ DeselectSchedule();};
    }
    else {
        k.onclick = () => {
            func(schedule);
        }
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

function AddTableD(_tr, _s,color = '#000000',isbold=false) {
    let _Td = document.createElement('td')
    _Td.style.color = color;
    if(isbold)
        _Td.style.fontWeight = 'bold';
    _Td.innerHTML = _s;
    _tr.appendChild(_Td);
}

function AddTableRow(subject) {
    let newTr = document.createElement('tr')
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
    if(parseInt(subject.CurrentStudent)<=parseInt(subject.TotalStudent)) {
        AddTableD(newTr, subject.TotalStudent + '/' + subject.CurrentStudent,'#FF0000',true)
    }
    else{
        AddTableD(newTr, subject.TotalStudent + '/' + subject.CurrentStudent)
    }
    AddTableD(newTr, subject.IsTact)
}

function TestLoad(){
    let _result = []
    for (d of glsos) {
        let sb = new Subject(d,true)
        _result.push(sb)
    }
    return _result
}

function ReloadTable(datas) {
    SearchQuery = []

    if(RadioEnable.checked){
        if(Radio1.checked){
            SearchQuery.push((sch)=>{return sch.IsTact==='대면';})
        }
        else{
            SearchQuery.push((sch)=>{return sch.IsTact==='비대면';})
        }
    }
    if(NoConflictWithSchedule.checked){
        SearchQuery.push((sch)=>{
            for (t of sch.Schedule) {
                if (t.checkOverrideWithSchedule(savedSchedules)) {
                    return false;
                }
            }
            return true;
        })
    }
    if(NoOverwhelmed.checked){
        SearchQuery.push((sch)=>{
            return(parseInt(sch.TotalStudent)<parseInt(sch.CurrentStudent));
        })
    }
    if(SearchTextExcept.value!=null &&SearchTextExcept.value.replace(' ','')!==''){
        let _replaced =SearchTextExcept.value.replace(' ','');
        SearchQuery.push((sch)=>{
            if(sch.Name.replace(' ','').includes(_replaced))
                return false;
            return true;
        })
    }
    if(SearchText.value!=null&&SearchText.value.replace(' ','')!==''){
        let _replaced =SearchText.value.replace(' ','');
        SearchQuery.push((sch)=>{
            if(sch.Name.replace(' ','').includes(_replaced))
                return true;
            return false;
        })
    }

    while (subjects.length > 0)
        subjects.pop();
    while (TableBody.children.length > 0)
        TableBody.children[0].remove();

    for (_subject of datas) {
        let pass = false;
        for(test of SearchQuery){
            if(!test(_subject)) {
                pass = true;
            }
        }
        if(!pass){
            subjects.push(_subject)
            AddTableRow(_subject);
        }
    }
    DeselectSchedule();
}

function addSelect(s1, json) {
    let newselect = document.createElement('select')
    let _top = document.createElement('option')
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

function SelectFromSchedule(sbject){
    DeselectSchedule()
    for(sc of sbject.Schedule){
        sc.fillColor(selectScheduleColor,sbject.Name)
    }
    SetDetails(sbject)
    activatedSubject = sbject;
    RemoveSubjectButton.style.visibility = 'visible'
}

function DeselectSchedule(){
    activatedSubject = null;
    RemoveSubjectButton.style.visibility = 'hidden'
    if(selectedSubject!=null) {
        for (sc of selectedSubject.Schedule) {
            sc.clearColor();
        }
    }
    selectedSubject = null;
    ClearDetails();
    DrawAll();
}

function SetDetails(sbject){
    while (EvaluationRatioPanel.children.length > 0)
        EvaluationRatioPanel.children[0].remove();
    for(let i = 0;i<9;i++){
        if(sbject.rates[i]!==0){
            AddRatio(sbject.rates[i],evalTypes[i],evalColors[i]);
        }
    }
    ClassCodeLabel.innerText = sbject.ClassID;
    SubjNameLabel.innerHTML = sbject.Name;
    PriorSubjLabel.innerHTML = sbject.PriorSubject;
    SubsequentSubjLabel.innerHTML = sbject.SubsequentSubject;
}

function ClearDetails(){
    while (EvaluationRatioPanel.children.length > 0)
        EvaluationRatioPanel.children[0].remove();
    ClassCodeLabel.innerText = '';
    SubjNameLabel.innerHTML = '';
    PriorSubjLabel.innerHTML = '';
    SubsequentSubjLabel.innerHTML = '';

}

function hideAndShowOption(){

}
