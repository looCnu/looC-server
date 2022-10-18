# looC API 명세서

* 베이스 URL = JimNastycs.com:5000/looC

* 필수 헤더:
“Content-Type”: “application/json”
=> form 말고 json으로 파라미터 전달해야 함

## 1. 회원 가입
* 메소드 = POST
* URL = /sign-up
* 파라미터 = {

	student_id: str
  
	password: str
  
	name: str
  
	college: str
  
  }
* 리턴값 = http status

## 2. 로그인
* 메소드 = POST
* URL = /sign-in
* 파라미터 = {

	student_id: str
  
	password: str
  
  }
* 리턴값 = http status
* 로그인 성공 후 부터는 JWT가 쿠키에 포함됨, 이 쿠키를 통해서 사용자를 인증
