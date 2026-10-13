# CLAUDE.md

> 이 파일은 Claude Code(claude.ai/code)가 이 저장소에서 작업할 때 참고하는 가이드다.

## 개요

「2026학년도 울산시교육청 시각장애 교원 역량 강화 연수」(2026-11-02, 90분) 김헌용 강의의 참가자 배포용 웹 강의안. 참가자가 센스리더로 읽으며 따라 하는 **원고 열람 페이지**이며 슬라이드덱이 아니다. 원고가 한 편이라 메뉴 없이 본문을 바로 보여 준다.

- 저장소: https://github.com/Engccer/ulsan-ai-training-2611
- 배포 URL: https://engccer.github.io/ulsan-ai-training-2611/ (main 브랜치 루트에서 GitHub Pages)
- 콘텐츠 정본: `G:\내 드라이브\KHY\Lectures\261102 울산시교육청 시각장애 교원 역량 강화 연수\4. 강의 원고\김헌용_강의원고.md`. 이 저장소는 그 내용을 옮긴 것이다. <!-- sanitize: allow 원고 정본 위치. 이 저장소의 존재 이유라 일반화 불가 -->

## 구조

- `build.py`: 드라이브의 마크다운을 읽어 `index.html`을 생성한다. 원고를 고치면 `python build.py` 후 commit·push. 정본 폴더는 윈도우와 맥에서 마운트 지점이 달라 `_ROOTS`에서 존재하는 쪽을 고른다.
- `template.html`: 페이지 골격·CSS·JS. `{{BODY}}`를 build.py가 채운다.
- `index.html`: 생성물. 직접 편집하지 않는다.
- `AGENTS.md`: `CLAUDE.md` 본문을 그대로 붙인 형제 문서. `CLAUDE.md`를 고치면 함께 갱신한다.

### build.py의 표시 단계 변환

정본 마크다운은 손대지 않고 여기서만 바꾼다.

- 제목·성명·소속 줄 제거: 템플릿의 h1과 머리말 줄이 대신한다.
- `separate_steps`: 원고의 단계 번호 `1)`은 한글 원고 기호라 마크다운 목록이 아니다. 단계마다 문단을 띄우고, 들여쓴 하위 불릿을 목록으로 인식되게 한다.
- `unfence_in_lists`·`add_copy_buttons`·`linkify`: 종로 과정 저장소(`jongno-ai-training-2608`)와 같은 구현. 복사 버튼은 `<pre>` 바깥, 링크 이름은 URL만.

## 접근성

글로벌 접근성 헌장(`~/.claude/ACCESSIBILITY.md`)을 따른다. landmark는 `<main>` 하나, heading 계층(h1 페이지 → h2 원고 `##` → h3 원고 `###`)으로 탐색한다. 복사 결과는 페이지에 하나뿐인 polite live region(`#say`)으로 알리고 포커스는 버튼에 남긴다. 새 탭 안내는 머리말에 한 번만 둔다(링크 이름에 보충 텍스트를 넣으면 센스리더 복사본에 섞인다). <!-- sanitize: allow 준수 기준 문서 참조. 경로가 곧 기준의 이름 -->
