# Choi, EunJung — 개인 소개 페이지

금융감독원에서 근무하며 DFMBA 8기 과정을 함께 듣고 있는 최은정의 개인 소개 페이지입니다.
프론트엔드(화면)와 백엔드(API)를 나눠 구성하고, 실시간 API 호출로 연동을 시연합니다.

## 구성

| 계층 | 역할 | 배포 |
|---|---|---|
| 프론트엔드 | 소개 화면 (HTML/CSS/JS) | Vercel |
| 백엔드 | REST API (FastAPI) | Render |

## 배포 주소

- Vercel (개인 소개 페이지): https://my-intro-one-chi.vercel.app
- Swagger UI (API 문서·테스트): https://my-intro-6i2d.onrender.com/docs

## 주요 API

| 메서드 | 경로 | 설명 |
|---|---|---|
| GET | `/weather` | 외부 날씨 API(Open-Meteo) 연동, 실패 시 재시도 후 안전하게 처리 |
| GET | `/hobbies` | 취미 목록 반환 |
| GET | `/routine` | 하루 루틴 반환 |
| GET, POST | `/guestbook` | 방명록 등록·조회 (DB 연동 실습용) |

## 프론트엔드·백엔드 연동

페이지 접속 시 프론트엔드가 Render에 배포된 백엔드 `/weather`를 자동으로 호출해 실시간 날씨를 표시합니다. CORS는 Render 환경변수 `ALLOWED_ORIGINS`로 Vercel 주소만 허용하도록 설정했습니다.