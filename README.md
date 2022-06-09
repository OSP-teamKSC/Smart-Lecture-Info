# 크누버스(knubus)
- 크누버스(knubus)는 knu + syllabus의 합성어로 기존의 경북대 강의 계획서의 불편한 점 개선
## 개발환경
- python @3.8.10
- mysql @8.0.29
- flask server
## 환경설정
```
# 가상환경 생성
$ python -m venv [your_virtual_environment]
$ source [your_virtual_environment]/bin/activate

# requirements install
$ pip install -r requirements.txt
```
## run(Linux)

## 기능
![강의선택](https://user-images.githubusercontent.com/101383098/172840533-c950950c-f0a8-440a-8cd9-4c1af32aa0ed.png)
### 1.시간표의 시각화
- 기존의 강의계획서는 시간표의 시각화가 이루어지지 않아 시간표를 짜는데 어려움이 있었다. 반면 크누버스는 간편하게 스케줄을 추가하여
시간표를 눈으로 확인해 볼 수 있다.
### 2. 겹치는 수업 자동제외
- 시간표의 시각화와 이어지는 부분으로 확정한 수업과 시간이 겹치면 시각적으로 표현하고 선택시 시간이 겹치는 수업을 제외시켜 준다.
### 3. 다중 필터링 적용
- 기존의 강의계획서보다 다양한 필터링을 적용하여서 학생들이 강의를 선택함에 있어 더욱 디테일한 부분까지 신경 쓸 수 있게된다.
