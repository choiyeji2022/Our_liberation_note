![footer](https://capsule-render.vercel.app/api?section=footer&height=350&text=Our%20liberation%20note!&color=6FC7E1&desc=우리들의%20해방%20일지&)

## 목차 🎊
- 🏝 프로젝트 소개
- 💡 프로젝트 기획 의도
- ℹ️ 웹사이트 정보
- 🛠 기능 설명
- 🚀 Stacks
- 🧰 Stack 선택한 이유
- 🛢 Database ERD
- 🔗 Link
<br>
<br>


## 🏝 프로젝트 소개 
  - 친구들과의 여행 계획 및 사진첩 공유와 여행 루트를 짜주는 AI기능을 제공하는 시크릿 사이트!

<br>
<br>

## 💡 프로젝트 기획 의도
  - 여름에 맞춰 프로젝트 기획을 하던 도중 여행을 주제로 멤버끼리만 공유하는 시크릿 다이어리를 주제로 진행하였습니다!
  - 기획 진행하며 다이어리는 앱용이 적절하다는 의견이 있었고,


    그 부분을 보안하기 위해 웹사이트만의 장점을 살릴 수 있는
    MBTI 테스트와 AI 요소를 추가해 지금의 웹사이트가 탄생하게 되었습니다!
  - 사용자의 입장에서 바라보며 이목을 끌 수 있을만한 요소들을 팀원들과 다같이 고민하고 흥미로운 기능들을 넣기 위해 많은 노력을 했습니다!
  - 프라이빗함이 핵심 키워드이기 떄문에 저희 웹사이트의 기능을 온전히 즐기기 위해선 그룹 생성이 필수이기 때문에 가입과 동시에 그룹이 생성이 됩니다!
  - 그룹과 노트 생성 후 노트 상세 페이지로 이동하면 달력과 함께 여러가지 기능(일정추가, 사진첩 생성, AI랑 놀기, 계획표 전송, 해방 필름 등)을 만나 볼 수 있습니다!
  - 항목들을 삭제 시 휴지통으로 이동되며 휴지통 창에서 복원 또는 완전 삭제 선택이 가능합니다!


<br>


## ℹ️ 웹사이트 정보
![info1](https://github.com/Msgun7/Our_liberation_note/assets/125116878/efbd95e1-56f5-450d-a552-181e9885cdb4)
![info2](https://github.com/Msgun7/Our_liberation_note/assets/125116878/8da5b50b-e79c-44a6-8b14-ebb780fee1bd)


<br>
<br>


## 🛠 기능 설명 (중요도 ⭐️로 표시!)

<br>

<details>
  <summary>유저 (⭐️⭐️⭐️⭐️⭐️) - 정은</summary>
  
     - 일반 로그인 & 이메일 인증
     - 카카오, 구글, 네이버 소셜 로그인 ➡️ allauth 라이브러리 사용 X
</details>

<br>

<details>
  <summary>사진첩 (⭐️⭐️⭐️⭐️⭐️) - 제건</summary>
  
     - 사진 저장 및 메모 ( 사진 저장 시 위치도 같이 저장할 수 있음)
     - 사진 댓글
</details>

<br>

<details>
  <summary>계획기능 (⭐️⭐️⭐️⭐️⭐️) - 미영</summary>
  
     - 달력에 일정 저장 및 계획 결과물을 Email로 전송
     - email은 웹 특성상 알림보다 확인용이 맞을 것이라고 판단 -> 알림용❌ 확인용⭕️
</details>

 <br>

<details>
  <summary>여행 지도 스탬프기능 (⭐️⭐️⭐️⭐️) - 예린</summary>
  
     - 여행간 곳에 스탬프가 생기고 그 장소의 사진(or 스티커)를 한번에 모아 볼 수 있음
</details>

<br>

<details>
  <summary>기본기능 (⭐️⭐️⭐️⭐️⭐️) - 예지</summary>
  
     - 유저 마이페이지(노트들 모아두는 곳)
    - 노트 생성(페이지들을 묶어주는 요소)
</details>

<br>

<details>
  <summary>그룹 (⭐️⭐️⭐️⭐️⭐️) - 정은</summary>
  
    - 프라이빗한 주제에 맞게 다이어리 작성 전 그룹 생성
    - 그룹장이 팀원의 email을 저장하는 형식
</details>
 
 <br>

<details>
  <summary>여행 궁합 테스트 (⭐️⭐️⭐️⭐️) - 예린</summary>
  
    - 여행 mbti 테스트를 진행해 친구와 궁합을 맞춰 볼 수 있는 기능
    - 보너스 기능 → 유저가 아니여도 사용 가능
</details>

<br>

<details>
  <summary>알고리즘(국내용! 베타버전)(⭐️⭐️⭐️) - 미영</summary>
  
    - 여행지 코스를 고민하는 유저들을 위해 대신 계획 해주는 ai(장소의 좌표를 보고 최단거리로 순서대로 계획해줌)
    - 해당 장소를 지도에 스탬프 찍어서 모달에 보여주기
</details>

<br>

<details>
  <summary>여행사진을 인생네컷처럼  바꿔주기 (⭐️⭐️⭐️) - 예지</summary>

    - 유저의 흥미를 끌기 위한 기능 중 하나!
    - 가로 버전, 세로 버전 취향에 맞춰 선택 가능
</details>

<br>

<details>
  <summary>결제기능 (⭐️⭐️) - 미영</summary>

    - 코스 정해주는 ai 사용 가능
    - 가로 버전, 세로 버전 취향에 맞춰 선택 가능
</details>

<br>

<details>
  <summary>이미지 컨펌 기능! (⭐️⭐️⭐️) - 미영</summary>

    - 코스 정해주는 ai 사용 가능
    - 가로 버전, 세로 버전 취향에 맞춰 선택 가능
</details>

<br>

<details>
  <summary>휴지통 기능 (⭐️⭐️⭐️) - 예린</summary>

    - 그룹, 사진, 노트를 삭제하면 휴지통으로 이동
    - 휴지통에서 복원&삭제 선택 가능
</details>

<br>

<details>
  <summary>✨Front PM - 예지</summary>

    - 예술 팀장
</details>


 <br>

 
## 🚀 Stacks

![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=Django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/Django%20REST%20Framework-009688?style=for-the-badge&logo=Django&logoColor=white)](https://www.django-rest-framework.org/)

<br>


## 🌏 Deployment Tools
[![AWS](https://img.shields.io/badge/AWS-%23FF9900?style=for-the-badge&logo=Amazon-AWS&logoColor=white)](https://aws.amazon.com/)
[![EC2](https://img.shields.io/badge/EC2-%23F8991C?style=for-the-badge&logo=Amazon-EC2&logoColor=white)](https://aws.amazon.com/ec2/)
[![Route 53](https://img.shields.io/badge/Route_53-%233495DB?style=for-the-badge&logo=Amazon-Route-53&logoColor=white)](https://aws.amazon.com/route53/)
[![Load Balancer](https://img.shields.io/badge/Load_Balancer-%23967FF7?style=for-the-badge&logo=ElasticLoadBalancing&logoColor=white)](https://aws.amazon.com/elasticloadbalancing/)
![Jenkins](https://img.shields.io/badge/Jenkins-007ACC?style=for-the-badge&logo=Jenkins&logoColor=white)
[![Gunicorn](https://img.shields.io/badge/Gunicorn-FF0000?style=for-the-badge&logo=Gunicorn&logoColor=white)](https://gunicorn.org/)
<br>
[![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=Nginx&logoColor=white)](https://nginx.org/)
![GitHub Actions](https://img.shields.io/badge/GitHubActions-2088FF?style=for-the-badge&logo=GitHubActions&logoColor=white)
[![S3](https://img.shields.io/badge/S3-%23169BF7?style=for-the-badge&logo=Amazon-S3&logoColor=white)](https://aws.amazon.com/s3/)
[![CloudFront](https://img.shields.io/badge/CloudFront-%23F5851C?style=for-the-badge&logo=Amazon-CloudFront&logoColor=white)](https://aws.amazon.com/cloudfront/)





<br>


## 🛠  Tools
[![Figma](https://img.shields.io/badge/Figma-F24E1E?style=for-the-badge&logo=Figma&logoColor=white)](https://www.figma.com/)
[![ERDCloud](https://img.shields.io/badge/ERDCloud-2180F3?style=for-the-badge&logo=ERDCloud&logoColor=white)](https://www.erdcloud.com/)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white)
![KakaoTalk](https://img.shields.io/badge/kakaotalk-ffcd00.svg?style=for-the-badge&logo=kakaotalk&logoColor=000000)
![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)


<br>


## 👥  Collaboration
[![Slack](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=Slack&logoColor=white)](https://slack.com/)
![Notion](https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=notion&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)


<br>


<br>


## 🧰 Stack 선택한 이유
- 🍀 MYSQL
  - [관련링크](https://www.integrate.io/ko/blog/postgresql-vs-mysql-the-critical-differences-ko/#whydodeveloperschooseoneovertheother)↗️
  - 사용 이유
    - 초보자가 다루기 쉽고, 데이터를 다루는데 있어서 빠르고 안정성이 뛰어나기 때문입니다
    - **다루는 데이터 타입이 많지 않아서 postgresql을 사용하기 보다 빠르기 처리 가능한 MYSQL을 선택!**
  - 그 밖의 장점
    - 웹사이트와 온라인 트랜잭션에 적합합니다.
    - 기능이 많지 않기 때문에 [속도와 안정성](https://www.keycdn.com/blog/popular-databases)에 중점을 두었습니다.
    - LAMP 스택(Linux, Apache HTTP Server, MySQL, PHP로 [구성](https://www.digitalocean.com/community/tags/lamp-stack?type=tutorials)된 웹 애플리케이션의 오픈 소스 제품군)의 표준 구성 요소입니다.
    - 관계형 데이터베이스 구조 덕분에 대용량 데이터 세트를 빠르고 효율적으로 처리가 가능합니다.
   
- 🍀 Python
  - [관련링크](https://www.python.org/downloads/)↗️
  - 사용 이유
     - 최신 버전 중에서 Maintenance status가 security로 3.11(bugfix)보다 안정화된 것으로 판단했고, 최대한 오랜 기간 지원을 받기 위해 선택하게 되었습니다.
     - 3.11 버전은 최대 60% 속도가 향상 되었지만 비교적 최신 버전이기에 사용하는 library가 지원을 안 할 가능성이 있기 때문입니다.
   
- 🍀 Jenkin(Backend)
  - [관련링크](https://www.dongyeon1201.kr/9026133b-31be-4b58-bcc7-49abbe893044)↗️
  - 사용 이유
    - 배포의 자동화 : 테스트, 빌드, 배포 등의 과정을 자동화하여 수작업으로 인한 오류를 줄이고 효율성을 향상 시킬 수 있기 때문입니다.
    - 피드백 반영 : 피드백과 문제의 해결의 빠른 반영이 가능합니다.
    - 다양한 플러그인 제공 : 슬랙 등 다양한 플러그인을 제공하여 실시간으로 배포 상황을 확인이 가능하기 때문입니다.
    - 배포의 시각화
   
  ![imgage](https://github.com/Msgun7/Our_liberation_note/assets/125116878/320e4810-60be-460f-bed3-f89c7bfcd932)

- 🍀 GitGub Actions(Frontend)
  - [관련링크](https://hwasurr.io/git-github/github-actions/)↗️
  - 사용 이유
    - 통합성 : 깃허브 플랫폼에 내장되어 있기 때문에 별도의 통합 작업 없이 즉시 사용 가능하기 때문입니다.
    - 간단한 배포 : main.yml 파일을 작성하고, 관련 키를 등록해 주면 되기 때문에 jenkins보다 쉽고 빠르게 배포 가능합니다.
   
<p align="center">
  <img src="https://github.com/Msgun7/Our_liberation_note/assets/125116878/e68b975e-97f2-4b41-be2b-e3e8f4ac8775" alt="GitHub-Actions">
</p>


   
<br>


## 🛢 Database ERD
![ERD](https://github.com/Msgun7/Our_liberation_note/assets/125116878/4c5c6714-4caa-4e56-ae1d-ea7ec68f80a6)


<br>


## 🔗 Link
- [🌟Frontend Github](https://github.com/ORN-group/Our_liberation_note_front)↗️

- 참고 사이트
  - [카카오 Maps API](https://apis.map.kakao.com/web/sample/multipleMarkerEvent/)
 
- ⚙️ Developers
  - [❤️연제건(팀장)](https://github.com/Msgun7)
  - [💚김미영](https://github.com/kmy9810)
  - [💙김정은](https://github.com/Eunnylog)
  - [💜양예린](https://github.com/yell2023)
  - [💛최예지](https://github.com/choiyeji2022)
