# Entry4.0-EntrySystem

## About this service

## Technical Stack
Entry4.0-EntrySystem 은 **2020학년도 대덕SW마이스터고등학교 입학전형**을 진행하는 서비스 입니다.

이 서비스는 학생들이 입학 원서를 작성할 때 사용하는 서비스로, 원서 작성품 제공, 미리보기, 출력 기능을 주로 합니다.  

EntrySystem Backend 는 다음과 같은 페이지를 서빙합니다.
1. 전형요강 소개(SelectionInfo)
2. 시스템 소개(IntroduceEntry)
3. 원서 작성(WriteApplication)
    1. 본인 인증
    2. 전형 구분
    3. 인적 사항
    4. 성적 입력
    5. 자기소개서 & 학업계획서
    6. 원서 미리보기
4. 마이 페이지



### Main Language & Framework
    - Python 
    - Flask

### WGSI
    - Gunicorn

### Database
    - MySQL
    - Redis 
    
### Logging
    - InfluxDB
    - Grafana
    
### API Architecture
    - REST(HTTP) API
    
### API Document
    - Swagger
    
### CI & CD
    - Circle CI
    - codecov
    - docker
    - docker registry

### Test 
    - unittest


### Infra Stack
    - AWS EC2
    - Nginx
    - Route53
