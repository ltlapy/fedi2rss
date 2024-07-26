# fedi2rss
Misskey의 내장 RSS 리더에서 특정 유저의 게시물 목록을 쉽게 볼 수 있도록 합니다

## Features
- [x] `http://example.com/@test@example.tld` 와 같이 AP 핸들로 유저 가져오기
  - 홈 게시물까지만 가져올 수 있음
  - CW가 없는 경우 본문을 ~~60자까지~~ 40자까지 제목으로 지정
- [X] Atom으로 반환

## TODO
- [ ] HTML 태그 제거 및 치환
- [ ] RSS으로 반환