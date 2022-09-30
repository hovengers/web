# Getting Started

### 1. 내려받기
- `git clone https://github.com/hovengers/web.git` 
- 만약 프로젝트 폴더가 존재하면 `git pull origin dev`

### 2. 패키지 설치
- `pip install --no-cache-dir -r requirements.txt`

### 3. src/config.py 추가
- 파일은 비공개라 나에게 따로 받아야함.
- 데이터 연결부분은 user와 password 임의 변경

### 4. MySQL에서 db/db.sql 실행

### 5. 전처리 파일 실행
- `python src/data/kktpreprocessing.py`
- data는 카카오톡 대화 전처리 + 결과 dataframe을 mysql 테이블로 옮김. flask 서버 실행 전에 mysql 서버 연결을 확인하고, kktpreprocessing.py를 실행해야 함. 

### 6. 서버 실행
- `python src/app.py`

### 7. 기타 프로젝트 정보
- 리포지토리 이름을 웹이라고 했지만 사실 프론트 백엔드 등을 나누지 않음.
- 소스 코드는 src/ 안에...
- 프론트는 templates랑 static에서 파일 찾기 가능.
- 백엔드는 api에서 파일 찾기 가능.
- models는 데이터베이스 모델.
