#!/usr/bin/env bash
# ============================================================
#  Huntbae MV Studio — one-click setup (macOS / Linux)
#  Installs: comfyui-mcp (Claude Code MCP), music-video skills,
#            ffmpeg / whisper / demucs, and runs a health check.
#  Usage:
#    curl -fsSL https://raw.githubusercontent.com/Huntbae/Huntbae/claude/github-repo-analysis-hv7y94/setup-mv.sh | bash
# ============================================================
set -u

BRANCH="claude/github-repo-analysis-hv7y94"
REPO_TARBALL="https://codeload.github.com/Huntbae/Huntbae/tar.gz/refs/heads/${BRANCH}"
SKILLS_DIR="${HOME}/.claude/skills"
OK=0; WARN=0

say()  { printf '\n\033[1;36m[MV-SETUP]\033[0m %s\n' "$1"; }
good() { printf '  \033[1;32m✔\033[0m %s\n' "$1"; OK=$((OK+1)); }
warn() { printf '  \033[1;33m⚠\033[0m %s\n' "$1"; WARN=$((WARN+1)); }

say "1/6 필수 도구 확인 (Node.js ≥ 22, Claude Code CLI)"
if command -v node >/dev/null 2>&1; then
  NODE_MAJOR=$(node -v | sed 's/v\([0-9]*\).*/\1/')
  if [ "${NODE_MAJOR}" -ge 22 ]; then good "Node.js $(node -v)"; else
    warn "Node.js가 v22 미만입니다($(node -v)). 업그레이드: brew install node"
  fi
else
  warn "Node.js 없음 → 설치: brew install node  (macOS) / https://nodejs.org"
fi
if command -v claude >/dev/null 2>&1; then good "Claude Code CLI 발견"; else
  warn "claude CLI 없음 → npm install -g @anthropic-ai/claude-code 후 이 스크립트 재실행"
fi

say "2/6 ComfyUI MCP 서버를 Claude Code에 등록"
if command -v claude >/dev/null 2>&1; then
  if claude mcp list 2>/dev/null | grep -q '^comfyui'; then
    good "이미 등록되어 있음 (comfyui)"
  elif claude mcp add --scope user comfyui -- npx -y comfyui-mcp >/dev/null 2>&1; then
    good "등록 완료: claude mcp add comfyui → npx -y comfyui-mcp"
  else
    warn "자동 등록 실패 → 수동으로: claude mcp add --scope user comfyui -- npx -y comfyui-mcp"
  fi
else
  warn "claude CLI가 없어 MCP 등록을 건너뜀 (1단계 해결 후 재실행)"
fi

say "3/6 뮤직비디오 스킬 설치 → ${SKILLS_DIR}"
TMP=$(mktemp -d)
if curl -fsSL "${REPO_TARBALL}" | tar -xz -C "${TMP}" 2>/dev/null; then
  SRC=$(find "${TMP}" -maxdepth 1 -type d -name 'Huntbae-*' | head -1)
  mkdir -p "${SKILLS_DIR}"
  for s in suno-music-video colab-gpu-run linkedin-viral; do
    if [ -d "${SRC}/skills/${s}" ]; then
      rm -rf "${SKILLS_DIR:?}/${s}"
      cp -R "${SRC}/skills/${s}" "${SKILLS_DIR}/"
      good "스킬 설치: ${s}"
    fi
  done
else
  warn "레포 다운로드 실패 → 수동: git clone -b ${BRANCH} https://github.com/Huntbae/Huntbae && cp -R Huntbae/skills/* ~/.claude/skills/"
fi
rm -rf "${TMP}"

say "4/6 편집 도구 (ffmpeg / whisper / demucs)"
if command -v ffmpeg >/dev/null 2>&1; then good "ffmpeg $(ffmpeg -version 2>/dev/null | head -1 | awk '{print $3}')"; else
  if command -v brew >/dev/null 2>&1; then
    brew install ffmpeg >/dev/null 2>&1 && good "ffmpeg 설치 완료" || warn "ffmpeg 설치 실패 → brew install ffmpeg"
  else
    warn "ffmpeg 없음 → macOS: brew install ffmpeg / Linux: sudo apt install ffmpeg"
  fi
fi
if command -v pip3 >/dev/null 2>&1; then
  python3 -c "import whisper" 2>/dev/null && good "whisper 있음" || {
    pip3 install -q openai-whisper 2>/dev/null && good "whisper 설치 완료" || warn "whisper 설치 실패(선택사항) → pip3 install openai-whisper"; }
  python3 -c "import demucs" 2>/dev/null && good "demucs 있음" || {
    pip3 install -q demucs 2>/dev/null && good "demucs 설치 완료" || warn "demucs 설치 실패(선택사항) → pip3 install demucs"; }
else
  warn "pip3 없음 → whisper/demucs(가사 타이밍·보컬분리)는 나중에 설치 가능"
fi

say "5/6 로컬 AI 엔진 상태"
if curl -s -m 2 "http://127.0.0.1:8188/system_stats" >/dev/null 2>&1; then
  good "ComfyUI 실행 중 (포트 8188)"
else
  warn "ComfyUI 미실행 — comfy.org 데스크톱 앱 설치/실행 후 다시 확인"
fi
if curl -s -m 2 "http://127.0.0.1:7860" >/dev/null 2>&1; then
  good "Draw Things API 실행 중 (포트 7860)"
else
  warn "Draw Things API 꺼짐 (선택사항 — 앱 설정에서 API Server ON)"
fi

say "6/6 결과"
printf '  성공 %d개 · 확인 필요 %d개\n' "${OK}" "${WARN}"
cat <<'NEXT'

────────────────────────────────────────────
다음 단계:
 1) ComfyUI 앱을 켠 상태에서 새 터미널 → claude 실행
 2) 테스트:  "석양 지는 바닷가 이미지 하나 만들어줘"
 3) 성공하면 폴더 만들기:
      mv-project/ ← song.mp3(SUNO) + lyrics.txt + photos/
 4) Claude에게: "mv-project 폴더의 SUNO 곡으로 뮤직비디오 만들어줘.
                 photos/me.jpg가 내 사진이야. 시네마틱, 16:9로."
문제 발생 시 Claude에게 "설치 상태 점검해줘"라고 하면
suno-music-video 스킬의 setup.md 체크리스트로 진단합니다.
────────────────────────────────────────────
NEXT
