"""드라이브의 마크다운 정본을 읽어 index.html을 생성한다. 원고를 고치면 다시 실행한다."""
# sanitize: allow-file 원고 정본이 놓인 Google Drive 마운트 지점을 찾는 것이 이 스크립트의 기능이라 경로를 일반화할 수 없다
import re
from pathlib import Path
import markdown

# 원고 정본은 같은 Google Drive를 윈도우와 맥에서 각각 다른 지점으로 마운트한다.
_REL = "KHY/Lectures/261102 울산시교육청 시각장애 교원 역량 강화 연수/4. 강의 원고/김헌용_강의원고.md"
_ROOTS = [Path(r"G:\내 드라이브")]                                   # Windows
_ROOTS += sorted((Path.home() / "Library/CloudStorage").glob("GoogleDrive-*/My Drive"))  # macOS
SRC = next((r / _REL for r in _ROOTS if (r / _REL).is_file()), None)
if SRC is None:
    raise SystemExit("원고 정본을 찾지 못했습니다. Google Drive가 마운트돼 있는지 확인하세요.")
OUT = Path(__file__).with_name("index.html")

# 본문에 그대로 적힌 URL을 새 탭 링크로 바꾼다. 링크의 접근 가능한 이름에는 URL만 둔다.
# 스크린 리더 가상 커서는 접근 가능한 이름을 복사하므로 보충 텍스트가 복사본에 섞인다.
URL_RE = re.compile(r"""(?:^|(?<=[>\s]))(https?://[^\s<>"']+?)(?=[.,)\]]*(?:\s|<|$))""", re.M)


def linkify(body: str) -> str:
    return URL_RE.sub(
        lambda m: f'<a href="{m.group(1)}" target="_blank" rel="noopener">{m.group(1)}</a>', body)


# 지시문 블록 바로 위(<pre> 바깥)에 복사 버튼을 단다. 안에 넣으면 버튼 글자가 복사본에 섞인다.
CODE_BLOCK = re.compile(r'<pre><code[^>]*>(.*?)</code></pre>', re.S)


def add_copy_buttons(body: str) -> str:
    return CODE_BLOCK.sub(
        lambda m: '<button type="button" class="copy" data-copy>복사</button>' + m.group(0), body)


# 목록 항목 안의 ``` 펜스는 fenced_code가 처리하지 못하므로 8칸 들여쓰기로 바꿔 넣는다.
INDENTED_FENCE = re.compile(r'^([ \t]+)```[^\n]*\n(.*?)^[ \t]*```[ \t]*$', re.M | re.S)


def unfence_in_lists(text: str) -> str:
    def repl(m):
        indent, inner = m.group(1), m.group(2)
        lines = [l[len(indent):] if l.startswith(indent) else l.lstrip()
                 for l in inner.rstrip('\n').split('\n')]
        return '\n' + '\n'.join(' ' * 8 + l if l.strip() else '' for l in lines) + '\n'
    return INDENTED_FENCE.sub(repl, text)


text = SRC.read_text(encoding="utf-8")
text = re.sub(r"^# .*\n", "", text, count=1)                        # 제목은 템플릿 h1이 대신함
text = re.sub(r"^\*\*김헌용\*\*\s*\n\s*\n?\(서울 신명중학교 교사\)\s*\n", "", text, flags=re.M)  # 머리말 줄이 대신함
text = unfence_in_lists(text)


# 원고의 단계 번호는 한글 원고 기호 `1)`이라 마크다운 목록이 아니다. 줄이 이어지면 한 문단으로
# 합쳐지므로 단계마다 문단을 띄우고, 바로 아래 들여쓴 불릿도 목록으로 인식되게 빈 줄을 넣는다.
def separate_steps(text: str) -> str:
    out, prev, in_code = [], "", False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            in_code = not in_code
        if in_code or line.lstrip().startswith("```"):
            out.append(line)
            prev = line
            continue
        is_step = re.match(r"^\d+\) ", line)
        is_bullet = re.match(r"^\s*- ", line)
        if (is_step or (is_bullet and not re.match(r"^\s*- ", prev))) and prev.strip():
            out.append("")
        out.append(re.sub(r"^\s+- ", "- ", line) if is_bullet else line)
        prev = line
    return "\n".join(out)


text = separate_steps(text)
body = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])
body = add_copy_buttons(body)
body = body.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
body = linkify(body)

template = Path(__file__).with_name("template.html").read_text(encoding="utf-8")
OUT.write_text(template.replace("{{BODY}}", body), encoding="utf-8")
print("wrote", OUT, OUT.stat().st_size, "bytes")
