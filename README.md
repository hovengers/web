# web
- 리포지토리 이름을 웹이라고 했지만 사실 프론트 백엔드 등을 나누지 않음.
- 소스 코드는 src/ 안에...
- 프론트는 templates랑 static에서 파일 찾기 가능.
- 백엔드는 api에서 파일 찾기 가능.
- models는 데이터베이스 모델.
- data는 카카오톡 대화 전처리 + 결과 dataframe을 mysql 테이블로 옮김. flask 서버 실행 전에 mysql 서버 연결을 확인하고, kktpreprocessing.py를 실행해야 함. 
- src/config.py라는 비공개 파일 존재함.