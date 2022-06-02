const days = ['월', '화', '수', '목', '금', '토'];
class Time {
    constructor(day, starttime, endtime) {
        this.Day = day;
        this.StartTime = starttime;
        this.EndTime = endtime + 1;
    }

    checkOverride(time) {
        if (this.Day != time.Day)
            return false;
        if (this.EndTime >= time.StartTime) {
            if (this.StartTime <= time.EndTime) {
                return true;
            }
            return false;
        }
    }

    checkOverrideWithSchedule(_schedule) {
        for (var _sche of _schedule) {
            for (var _t of _sche.Schedule) {
                if (this.checkOverride(_t))
                    return true;
            }
        }
        return false;
    }

    fillColor(color,text='') {
        for (var i = this.StartTime; i < this.EndTime; i++) {
            if(i==this.StartTime)
                ColorTable(this.Day, i, color,text)
            else
                ColorTable(this.Day, i, color,'')
        }
    }

    clearColor() {
        for (var i = this.StartTime; i < this.EndTime; i++) {
            ClearTable(this.Day, i)
        }
    }

    toString() {
        let s = days[this.Day];
        s += ' ';
        s += (this.StartTime < 2) ? ("09") : (parseInt(this.StartTime / 2 + 9));
        s += ":" + ((this.StartTime % 2 == 0) ? "00" : "30") + " - "
        s += (this.EndTime < 2) ? ("09") : (parseInt(this.EndTime / 2 + 9));
        s += ":" + ((this.EndTime % 2 == 0) ? "00" : "30");
        return s;
    }

}
function scheduleFromString(s) {
    times = []
    var day = -1
    var tStart = -1;
    var tEnd = -1;
    var last = 0;
    var str;
    for (var i = 0; i < s.length; i++) {
        if (s[i] == ',' && s[i + 2] == ' ') {
            str = s.substr(last, i-last)
            _day = days.indexOf(str.split(' ')[0]);
            spl = str.split(' ')[1].split(',')
            
            let splsize = spl.length - 1
            let t1 = parseInt(spl[0].substr(0, spl[0].length - 1) * 2 - 2)
            if (spl[0][spl[0].length - 1] == 'B')
                t1 += 1;
            let t2 = parseInt(spl[splsize].substr(0, spl[splsize].length - 1) * 2 - 2)
            if (spl[splsize][spl[splsize].length - 1] == 'B')
                t2 += 1;

            if (day == _day && t1 == tEnd + 1) {
                tEnd = t2;
            } else {
                if (day != -1) {
                    times.push(new Time(day,tStart,tEnd))
                }
                day =_day;
                tStart = t1;
                tEnd = t2;
            }

            last = i + 1;
        }
    }

    str = s.substr(last, s.length - last)
    day = days.indexOf(str.split(' ')[0]);
    spl = str.split(' ')[1].split(',')
    let t1 = parseInt(spl[0].substr(0, spl[0].length - 1) * 2 - 2)
    if (spl[0][spl[0].length - 1] == 'B')
        t1 += 1;
    let splsize = spl.length - 1
    let t2 = parseInt(spl[splsize].substr(0, spl[splsize].length - 1) * 2 - 2)
    if (spl[splsize][spl[splsize].length - 1] == 'B')
        t2 += 1;
    
    if (day == _day && t1 == tEnd + 1) {
        tEnd = t2;
        times.push(new Time(day,tStart,tEnd))
    } else {
        if (day != -1) {
            times.push(new Time(day,tStart,tEnd))
        }
        day =_day;
        tStart = t1;
        tEnd = t2;
        times.push(new Time(day,tStart,tEnd))
    }


    return times;
}
