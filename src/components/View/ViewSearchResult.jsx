//Table 형태로 Searched result를 보여주고
import React, { useMemo, useState } from "react";
import

const columnData = [
    {accessor: SubjectName,
    Header :"과목명"},
    {accessor: SubjectCode,
    Header : "과목코드"},
    {accessor: EstablishedUniversity,
    Header : "개설대학"},
    {accessor: EstablishedDepartment,
    Header : "개설학과"}
]

const columns = useMemo( () => columnData, [] )

const [info, setInfo] = useState();

//test용
const data = useMemo(()=> [{
    SubjectName: "오픈소스프로그래밍",
    SubjectCode: "GLSO0215-003",
    EstablishedUniversity: "IT대학",
    EstablishedDepartment: "컴퓨터학부 글로벌SW융합전공"
}], [])

//서버에서 가져오려면 이 형태를 활용해야
//const data = useMemo(()=>info, [info]);

//const getInfo = () => { data.getInfo().then(item=>setInfo(item)); }

const ViewSearchResult = () => {
    return <div className="table-wrap">
        
    </div>;
}

export default ViewSearchResult;