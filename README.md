# FastAPI Course Records API

## 실행 방법

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## API

- GET `/courses`: 전체 수강기록 조회
- POST `/courses`: 새 수강기록 추가

## POST body 예시

```json
{
  "course_name": "인간로봇상호작용",
  "year": "2026",
  "semester": "2",
  "grade": "A+"
}
```