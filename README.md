# 크누버스(knubus)
- KNU + Syllabus - 더 나은 경북대 강의 조회 서비스
## 개발환경
- python @3.8.10
- mysql @8.0.29
- flask server



# 기능
<img src='https://user-images.githubusercontent.com/101383098/172840533-c950950c-f0a8-440a-8cd9-4c1af32aa0ed.png' width = '1280'>
<img src='https://user-images.githubusercontent.com/54511614/172935281-4b6c105f-a8d3-4fe0-b5bc-5a0295c26cb5.png' width = '720'>
#### 시간표의 시각화
- 간편하게 스케줄을 추가하여 시간표를 눈으로 확인 가능
#### 필터링 기능
- 교수, 강의명, 인원 초과 여부, 평가 비중, 시간표 중복유무 등으로 필터링 적용 가능
#### 상세한 정보
- 미리 크롤링된 강의계획서 정보로 평가 비중, 권장 선행/후행 과목 확인 가능



# 실행법
## 쉘 스크립트 실행(Linux)

```
$ chmod +x ./run.sh
$ ./run.sh
```
- python 및 mysql 자동 설치 및 실행에 필요한 python 환경 자동 구축

- 환경 구축 이후 파이썬 코드 실행으로 서버 구동 가능
```
$ python3 flask-server/main.py
```

