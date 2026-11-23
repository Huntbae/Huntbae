# Huntbae GitHub 포트폴리오 분석 & 활용 전략

> 대상: https://github.com/Huntbae?tab=repositories (13개 레포)
> 작성: 2026-06-29 · 활용/스킬화/앱화 관점 정리

---

## 1. 한눈에 보는 포트폴리오 지도

| # | 레포 | 한 줄 정의 | 언어 | 공개 | 최근 업데이트 |
|---|------|-----------|------|------|--------------|
| 1 | **autodesign-llm** | 자연어 → 자동차 부품 CAD 설계 + 이론·표준·논문 근거 검증 + FEM/CFD | Python | 공개 | 2026-06 |
| 2 | **hermes-local** | 멀티모달 생성형 로컬 LLM 에이전트 (RAG + LoRA 자기학습 + 문서/CAD 생성) | Python | 비공개 | 2026-06 |
| 3 | **hermes-agent_one-click_kit** | Nous Hermes Agent 윈도우 원클릭 설치/실행 kit (KO/EN) | Batch | 공개 | 2026-06 |
| 4 | **claude-skills-hwp** | HWPX(한컴 한글) 공문서 생성·분석·검증 Claude 스킬 (무의존성, MIT) | Python | 공개 | 2026-04 |
| 5 | **linked-auto** | 링크드인 글 분석 → 바이럴 패턴 추출 → 재사용 스킬화 | (문서) | 공개 | 2026-06 |
| 6 | **clan-hunts-hub** | 커뮤니티 허브 | TypeScript | 비공개 | 2025-12 |
| 7 | **clan-hunts-social** | 소셜 레이어 | TypeScript | 비공개 | 2025-12 |
| 8 | **mobilitytoday** | 모빌리티 콘텐츠/뉴스 | JavaScript | 공개 | 2024-11 |
| 9 | **Huntbae** | 프로필 config + Claude 실험 샌드박스 (GEPA, WebLLM, notebook) | HTML/Py | 공개 | 2026-06 |
| 10 | **eDron** | 드론 제어 (초기 작업) | C++ | 공개 | 2018 |
| 11–13 | **desktop-tutorial / new / claude** | 튜토리얼·플레이스홀더·실험 | — | 공개 | 2026 |

---

## 2. 당신이 실제로 잘하는 것 (포트폴리오가 말해주는 강점)

코드 13개를 가로질러 보면 **반복되는 4가지 시그니처**가 보입니다. 이게 당신의 "무기"입니다.

1. **로컬·오픈소스 LLM 에이전트 운용** — 클라우드 의존을 줄이고 Hermes(Nous)/Ollama를 직접 돌립니다. (`hermes-local`, `one-click_kit`, `autodesign-llm`의 백엔드 추상화)
2. **도메인 특화 + 근거 검증** — "LLM이 그냥 답하기"가 아니라 *이론·표준·논문·공문 규칙*으로 검증하는 루프를 답니다. (`autodesign-llm`의 FEM/CFD 검증, `claude-skills-hwp`의 2025 공문 규칙 검증)
3. **비개발자도 쓰는 접근성** — `.bat` 원클릭, KO/EN 이중 문서, 무외부의존성. 기술을 "배포 가능한 제품"으로 포장합니다.
4. **Claude Skills를 1급 빌딩블록으로 사용** — 워크플로를 스킬로 굳혀 재사용합니다. (`claude-skills-hwp`, `linked-auto`)

> **전략적 결론:** 흩어진 13개가 아니라, *"근거로 검증하는 로컬 LLM 에이전트를 비개발자도 원클릭으로 쓰게 만든다"*는 하나의 제품 철학으로 수렴시킬 수 있습니다. 아래 통합/앱 제안은 모두 이 축을 따릅니다.

---

## 3. 레포별 "잘 쓰는 법" (Actionable)

### A. LLM 에이전트 코어 — 여기에 시간을 투자하세요

**`autodesign-llm` (가장 차별화된 자산)**
- 잘 쓰는 법: 현재 dry-run/Mock 백엔드 + Hermes로 end-to-end가 도는 상태. 다음 한 수는 **(1) 실제 FreeCAD/FEM 솔버를 의존성 주입으로 연결**해 "진짜 검증" 데모를 만들고, **(2) 검증 리포트를 HWPX 공문/PDF로 자동 출력**(→ `claude-skills-hwp` 재사용)하는 것.
- 차별화 포인트: "자연어→CAD"는 많지만 *표준·논문 근거 + FEM/CFD 검증 루프*까지 묶은 건 드뭅니다. 이걸 전면에 내세우세요.

**`hermes-local`**
- 잘 쓰는 법: `autodesign-llm`과 **LLM 추상화 레이어를 공유 라이브러리로 분리**하세요. 지금 두 레포가 비슷한 백엔드(Hermes/Ollama/Claude) 코드를 중복 보유할 가능성이 큽니다. `huntbae-llm-core` 같은 공통 패키지로 빼면 유지보수가 절반이 됩니다.
- LoRA 자기학습 + RAG는 "도메인 지식이 쌓일수록 좋아지는" 스토리. autodesign의 설계 이력을 학습 데이터로 순환시키면 강력한 차별점.

**`hermes-agent_one-click_kit`**
- 잘 쓰는 법: 이미 안정적. 이걸 **배포 채널**로 쓰세요 — 위 두 코어를 일반 사용자에게 전달하는 "런처". `hermes doctor` 진단 패턴은 다른 프로젝트에도 이식 가치가 높습니다(→ 스킬 후보).

### B. 스킬/자동화 — 이미 강한 영역, 더 굳히기

**`claude-skills-hwp`** — 완성도 높음. 한국 시장에서 *유일성 높은 자산*(공문 자동작성 + 2025 규칙 검증). 그대로 앱화 후보(아래 4번).

**`linked-auto`** — 코드가 아니라 "레시피/워크플로" 문서. → **이번에 실제 Claude 스킬로 패키징했습니다** (`skills/linkedin-viral/`, 4번 섹션 참고).

### C. 웹/소셜 — 통합 또는 정리 결정

- `clan-hunts-hub` + `clan-hunts-social`: 이름상 한 제품의 두 레이어. **모노레포로 합치는** 걸 권장(공유 타입·인증·디자인시스템 중복 제거). 둘 다 비공개라 상세 진단은 못 했으니, 원하면 접근 권한을 주시면 코드 레벨로 정리안을 드립니다.
- `mobilitytoday`(2024 이후 정지) / `eDron`(2018): 활성 계획이 없다면 **아카이브 처리**해 프로필을 깔끔하게. 핵심 4개(autodesign / hermes-local / hwp / linked) 위주로 프로필을 큐레이션하면 첫인상이 훨씬 강해집니다.

---

## 4. 스킬화 (Skillification)

### ✅ 이번에 실제로 만든 것: `linkedin-viral` 스킬

`linked-auto`의 "추출 → 분석 → 패턴 → 드래프트" 워크플로를 **드롭인 가능한 Claude Skill**로 패키징했습니다. 위치: [`skills/linkedin-viral/`](skills/linkedin-viral/)

- `SKILL.md` — Claude가 자동 호출하는 진입점 (분석/패턴추출/드래프트 3단계)
- `references/analysis-prompt.md` — 내 글 CSV를 넣으면 성과·패턴을 구조화 분석
- `references/recipe-template.md` — 바이럴 글을 "재현 가능한 레시피"로 고정하는 틀

설치: Claude Code/Cursor는 `~/.claude/skills/`(또는 프로젝트 `.claude/skills/`)에 폴더째 복사, Claude.ai는 ZIP 업로드.

### 추가 스킬화 후보 (권장, 미구현)

| 후보 | 출처 | 왜 스킬인가 | 비고 |
|------|------|-----------|------|
| **engineering-report → HWPX** | autodesign-llm × hwp | 설계 검증 결과를 한국 공문/보고서로 자동 출력 | 기존 hwp 스킬에 "엔지니어링 리포트" 워크플로 1개 추가 |
| **hermes-doctor** | one-click_kit | 로컬 LLM 환경 자가진단(파이썬/노드/모델/포트) 체크리스트 | bat 로직을 스킬 절차로 일반화 |
| **design-review (근거검증)** | autodesign-llm | 임의 설계 사양을 표준·논문 근거로 사전 검토 | 솔버 없이도 동작하는 "리뷰" 단계만 스킬화 |

> 스킬로 **만들지 말 것**: `hermes-local`/`autodesign-llm`의 코어(솔버·LoRA·RAG)는 무거운 런타임이라 스킬이 아니라 **앱/서비스**가 맞습니다(아래).

---

## 5. 앱화 제안 (Product Proposals)

우선순위 순. 모두 기존 레포를 재활용하므로 0부터 시작이 아닙니다.

### 🥇 제안 1 — "원클릭 엔지니어링 어시스턴트" 데스크톱 앱
**= autodesign-llm(두뇌) + hermes-local(로컬 런타임) + one-click_kit(배포)**
- 흐름: *자연어 사양 → CAD 생성 → 표준·논문 근거 검증 → FEM/CFD → HWPX/PDF 보고서*
- 왜: 당신의 3대 코어를 하나의 사용자 경험으로 묶는 가장 자연스러운 통합. 오프라인·로컬이라 **사내 보안 환경(제조/방산)** 세일즈 포인트가 명확.
- MVP: one-click 런처에 autodesign 데모를 얹고, 결과를 hwp 스킬로 보고서화. (전부 기존 코드 재사용)

### 🥈 제안 2 — 한국 공문서 SaaS / Claude 앱
**= claude-skills-hwp 기반**
- 흐름: 사용자가 내용 입력/마크다운 업로드 → 2025 공문 규칙 검증 → HWPX 다운로드, 버전 비교(diff)
- 왜: 한국 공공·교육·기업 시장에 **경쟁자 거의 없는** 니치. 무의존성이라 서버 비용도 낮음.
- 형태: 웹앱(빠른 검증) 또는 Claude.ai/Cursor 마켓 배포(스킬 그대로).

### 🥉 제안 3 — 링크드인 바이럴 콘텐츠 스튜디오
**= linked-auto + 신규 `linkedin-viral` 스킬**
- 흐름: Apify로 내 글 수집 → 분석 대시보드(어떤 포맷/앵글이 먹혔나) → 스킬로 새 글 드래프트
- 왜: 스킬은 이미 만들었으니 **얇은 웹 UI**만 얹으면 제품. 개인 브랜딩/세일즈 종사자 타깃.

### 보조 — clan-hunts 통합 플랫폼
- hub+social 모노레포화 후 정식 제품으로. (코드 접근 시 구체화 가능)

---

## 6. 다음 30일 추천 로드맵

1. **공통화**: `huntbae-llm-core`로 LLM 백엔드 추상화 분리 (autodesign ↔ hermes-local 중복 제거)
2. **연결**: autodesign 검증 결과 → `claude-skills-hwp`로 보고서 자동 출력 (스킬 2개 연동 데모)
3. **패키징**: `linkedin-viral` 스킬 실사용 → 피드백 → v2
4. **큐레이션**: 비활성 레포(eDron, mobilitytoday) 아카이브, 핵심 4개로 프로필 README 재구성
5. **제품화 결정**: 위 앱 제안 1·2 중 하나를 MVP로 착수

---

### 부록: 분석 방법 / 한계
- 공개 README를 직접 읽어 분석: `autodesign-llm`, `claude-skills-hwp`, `hermes-agent_one-click_kit`, `linked-auto`.
- **비공개 레포**(`hermes-local`은 검색 메타데이터만, `clan-hunts-hub/social`)는 README 본문 접근 불가 → 레포명·설명·언어 기반 추정. 정확한 진단을 원하면 해당 레포 접근 권한을 주세요.
