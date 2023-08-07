# 동국대학교 멋쟁이사자처럼 2023 해커톤 세나개팀 blink 백엔드 repository

## 초기 셋팅
### 가상환경 생성
    windows : python -m venv {가상 환경 이름}
    mac : python 3 -m venv {가상 환경 이름}
    * 가상 환경 이름은 venv로 통일

### 가상환경 실행
    windows : source venv/Scripts/activate
    mac : source venv/bin/activate


### 라이브러리 설치
    windows : pip install -r requirements.txt
    mac : (추가바람)

    * 추가된 pip 어쩌구 있으면 'pip freeze > requirements.txt' 명령어 꼭 사용

### db 마이그레이션 진행
    * manage.py 파일이 있는 위치로 이동 후
    python manage.py makemigrations
    python manage.py migrate

### 서버 실행
    python manage.py runserver