function Search(ReloadTable){
    const searchFilter = {
        'Season': IdSeme.value,
        'Gubun': IdUniv.value,
        'SearchUniversity': IdCollege.value,
        'SearchDepartment': IdCore.value === '' ? IdMajor.value : IdCore.value,
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