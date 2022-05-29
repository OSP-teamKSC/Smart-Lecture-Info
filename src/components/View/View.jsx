import React from "react";


//const table = createTable()

const View = () => {
    //서버에서 가져올 것. 지금은 강의 table.sql 참고
    //과목코드_분반명, 분반은 제외. 개설학기도 제외
    let columns = ["과목명", "과목코드", "개설대학",
    "개설학과", "수강총원", "수강인원", "비대면여부",
    "시간표", "학점"];

    return (
        <div>
            <p>View...later</p>
        </div>
    );
}

export default View;