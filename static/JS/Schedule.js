//대학 목록
const UnivList = {'인문대학': ['고고인류학과', '국어국문학과', '노어노문학과', '독어독문학과', '문화콘텐츠개발융합전공', '북방문화통상융합전공', '불어불문학과', '사학과', '영어영문학과', '인문대학', '일어일문학과', '중어중문학과', '철학과', '한문학과'], '사회과학대학': ['IT정치융합전공', '디지털정보관리융합전공', '문헌정보학과', '미디어커뮤니케이션학과', '사회복지거시전공', '사회복지미시전공', '사회복지학부', '사회학과', '심리정보융합전공', '심리학과', '정치외교학과', '지리학과'], '자연과학대학': ['물리학과', '생명공학전공', '생물학전공', '수학과', '지구시스템과학부', '지질학전공', '천문대기과학전공', '통계학과', '해양학전공', '핵심과학융합전공', '화학과'], '경상대학': ['경영학부', '경영학부A', '경영학부B', '경영학부C', '경제통상학부', '경제통상학부A', '경제통상학부B', '경제통상학부C', '비즈니스인텔리전스융합전공'], '공과대학': ['건축공학전공', '건축학전공', '고분자공학과', '공간정보융합전공', '금속신소재공학전공', '기계공학부A', '기계공학부B', '기계공학부C', '기계공학전공', '기계설계학전공', '섬유시스템공학과', '신소재공학부A', '신소재공학부B', '신재생에너지전공', '에너지공학부', '에너지변환전공', '응용화학과', '응용화학전공', '전자재료공학전공', '토목공학과', '화학공학과', '화학공학전공', '환경공학과'], '농업생명과학대학': ['농산업학과', '농업토목.생물산업공학부', '농업토목공학전공', '바이오섬유소재학과', '북한농업개발융합전공', '산림과학.조경학부', '생물산업기계공학전공', '생물정보학융합전공', '스마트팜공학융합전공', '식물생명과학전공', '식품공학부', '식품생물공학전공', '식품소재공학전공', '식품응용공학전공', '식품자원경제학과', '원예과학과', '원예식품융합전공', '응용생명과학부', '응용생물학전공', '임산공학전공', '임학전공', '조경학전공', '환경생명화학전공'], '예술대학': ['국악학과', '디자인학과', '미술학과', '음악학과'], '사범대학': ['가정교육과', '교육학과', '국어교육과', '기술·가정교육전공', '독어교육전공', '물리교육과', '불어교육전공', '사범대학', '생물교육과', '수학교육과', '역사교육과', '영어교육과', '윤리교육과', '일반사회교육과', '지구과학교육과', '지리교육과', '체육교육과', '통합과학교육전공', '통합사회교육전공', '화학교육과'], '수의과대학': ['수의예과', '수의학과'], '생활과학대학': ['식품영양학과', '아동가족학전공', '아동학부', '아동학전공', '의류학과'], '간호대학': ['간호학과'], '자율전공부': ['인문사회자율전공', '자연과학자율전공'], '의과대학': ['의예과', '의학과'], '치과대학': ['치의예과', '치의학과'], 'IT대학': ['건설IT전공', '글로벌소프트웨어융합전공', '데이터과학전공', '모바일공학전공', '미디어아트전공', '빅데이터전공', '인공지능컴퓨팅전공', '전기공학과', '전자공학부', '전자공학부 A', '전자공학부 B', '전자공학부 C', '전자공학부 D', '전자공학부 E', '전자공학부 F', '전자공학부 H', '컴퓨터학부', '플랫폼소프트웨어전공', '핀테크전공'], '약학대학': ['약학과', '약학과'], '행정학부': ['공공관리전공', '공공정책전공', '행정학부'], '융합학부': ['로봇및스마트시스템공학전공', '수소및신재생에너지전공', '의생명융합공학전공', '인공지능전공'], '[상주캠퍼스]생태환경대학': ['곤충생명과학과', '관광학과', '레저스포츠학과', '말/특수동물학과', '산림환경자원전공', '생물응용전공', '생태관광전공', '생태환경시스템학부', '식물자원환경전공', '축산생명공학과', '축산학과'], '[상주캠퍼스]과학기술대학': ['건설방재공학부', '건설방재공학전공', '건설환경공학전공', '나노소재공학부', '섬유공학전공', '소프트웨어학과', '식품외식산업학과', '신소재공학전공', '에너지화공전공', '융복합시스템공학부', '자동차공학부', '정밀기계공학과', '지능형자동차전공', '치위생학과', '친환경자동차전공', '패션디자인전공', '플랜트시스템전공', '항공위성시스템전공']};
const GEList = {'첨성인기초': ['독서와토론', '사고교육', '글쓰기', '실용영어', '소프트웨어'], '첨성인소양': ['예술과문화', '사상과제도', '지역과세계', '자연과기술', '생활과건강', '진로와취업'], '첨성인핵심': {'인문.사회': ['언어와문학', '사상과가치', '역사와문화', '사회와제도', '외국어'], '자연과학': ['수리', '기초과학', '자연과환경']}};

const Subject = {"NULL": null,"UN": UnivList, "GE": GEList};
const sub_btn = document.querySelector("#submit");

function setCollage(e)          //단과대학 selelct 생성
{
    const target = document.getElementById("Collage");
    let collageList;

    //하위 카테고리 초기화
    target.options.length = 0;
    document.getElementById("Major").options.length = 0;

    //insert options
    if(e.value!=="NULL")
    {
        collageList = Object.keys(Subject[e.value]);
        categoryChange(target, collageList);
    }

}

function setMajor(e)    //전공 select 생성
{
    const UpperTarget = document.getElementById("Subject");
    const target = document.getElementById("Major");
    const course = Subject[UpperTarget.value][e.value];
    //초기화
    target.options.length = 0;
    //insert options
    if(e.value !== "NULL")
    {
        categoryChange(target, course);
    }

}

function categoryChange(target, List)       //select 생성
{
    //초기값 insert
    let opt = document.createElement("option");
    opt.value = "NULL";
    opt.innerHTML = "선택";
    target.appendChild(opt);
    for(let x = 0; x < List.length; x++)
    {
        let opt = document.createElement("option");
        opt.value = List[x];
        opt.innerHTML = List[x];
        target.appendChild(opt);
    }
}
//검색하기 버튼 클릭 시
sub_btn.addEventListener('click', ()=> {
        const year = document.getElementById("year").value;
        const semester = document.getElementById("semester").value;
        const Collage = document.getElementById("Collage").value;
        const Major = document.getElementById("Major").value;

        const Json = new Object();
        Json.year = year;
        Json.semester = semester;
        Json.Collage = Collage;
        Json.Major = Major;

        //XMLHttpRequest 객체 생성
        const xhr = new XMLHttpRequest();
        //요청을 보낼 방식, url, 비동기여부 설정

                           //서버 주소
        xhr.open('post', 'http://192.168.1.103:8080/request', true);

        //HTTP 요청 헤더 설정
        xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        //요청 전송
        xhr.send(`data=${JSON.stringify(Json)}`);

       //Response Type을 Json으로 사전 정의
	    xhr.responseType = "json";

        //Callback
        xhr.onload = () => {
            if (xhr.status == 200) {
            	//success
                console.log(xhr.response);
            } else {
                //failed
            }
        }
    });
