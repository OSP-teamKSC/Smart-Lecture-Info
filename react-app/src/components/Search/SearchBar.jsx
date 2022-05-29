import React from "react";

//미완성
//enter만 눌러도 조회되도록

const onClick = () => {
    //검색을 함, 즉 submit
}

const onKeyPress = (e) => {
    if (e.key == 'Enter') { onClick(); }
}

const SearchBar = () => {
    //이것도 셀렉트에 따라서 옵션 바뀌어 뜨도록
    //너무 sy.knu.ac.kr 복붙인가? 어떻게 바꾸지
    return <div className="search-bar">
        <select>
            <option value="">선택</option>
            <option>교과목코드</option>
            <option>교과목명</option>
            <option>담당교수</option>
            <option>건물명</option>
            <option>교과목구분</option>
            <option>수업시간</option>
        </select>
        
        <input className="searchInput"
        name="searchingInput"
        type="text"
        placeholder="검색"
        />

    </div>;
}

export default SearchBar;