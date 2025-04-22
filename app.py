import streamlit as st
st.set_page_config(page_title="천안 물주먹 이수민의 사주 기반 로또 번호 생성기", layout="centered")

import random
from datetime import datetime
from typing import Optional

# 오행 매핑
element_map = {
    '갑': '木', '을': '木', '甲': '木', '乙': '木',
    '병': '火', '정': '火', '丙': '火', '丁': '火',
    '무': '土', '기': '土', '戊': '土', '己': '土',
    '경': '金', '신': '金', '庚': '金', '辛': '金',
    '임': '水', '계': '水', '壬': '水', '癸': '水',
    '자': '水', '축': '土', '인': '木', '묘': '木',
    '진': '土', '사': '火', '오': '火', '미': '土',
    '신': '金', '유': '金', '술': '土', '해': '水'
}

zodiac_storage = {
    '자': ['癸'], '축': ['己', '癸', '辛'], '인': ['甲', '丙', '戊'], '묘': ['乙'],
    '진': ['戊', '乙', '癸'], '사': ['丙', '庚', '戊'], '오': ['丁', '己'], '미': ['己', '丁', '乙'],
    '신': ['庚', '壬', '戊'], '유': ['辛'], '술': ['戊', '辛', '丁'], '해': ['壬', '甲']
}

number_map = {
    '木': [3, 8, 13, 18, 23, 28, 33, 38, 43],
    '火': [2, 7, 12, 17, 22, 27, 32, 37, 42],
    '土': [5, 10, 15, 20, 25, 30, 35, 40, 45],
    '金': [1, 6, 11, 16, 21, 26, 31, 36, 41],
    '水': [4, 9, 14, 19, 24, 29, 34, 39, 44]
}

def interpret_elements(elements):
    messages = {
        '木': {
            'low': "🌑 나무가 시듬고 있습니다… 시작과 기획이 막이고 있군요.",
            'mid': "🌿 당산의 발벽에서 빠른가 자르고 있습니다. 운이 트입니다.",
            'high': "🌪️ 가지가 너무 자르어지였습니다. 방향을 잃은 용심은 재양이 됩니다."
        },
        '火': {
            'low': "❄️ 불이 끝었습니다. 에어전과 재물운이 엔 불에 떠어있군요.",
            'mid': "🔥 불꽃이 당산 안에서 태오르고 있습니다. 재물과 명여의 운이 기억됩니다.",
            'high': "☄️ 너무 강한 불은 모든 것을 태워낼 수 있습니다… 충돌을 피하세요."
        },
        '土': {
            'low': "🕳️ 기반이 약합니다. 사람을 믿지 마세요.",
            'mid': "⛰️ 땅이 단단합니다. 신력과 기획이 새어진 시기입니다.",
            'high': "🪨 너무 무겁습니다. 책임, 의미, 스트레스가 폭발할 수 있습니다."
        },
        '金': {
            'low': "🖠️ 무기가 없습니다. 판단력이 흐르고 있습니다.",
            'mid': "💫 당산 안의 칼람이 빛날고 있습니다. 결정의 순간입니다.",
            'high': "⚔️ 과한 날카로운은 사람을 상처내며, 동밀과 분열을 주의하세요."
        },
        '水': {
            'low': "🧷 물이 막히고 있습니다. 감정, 지혜, 인연이 붓기려 합니다.",
            'mid': "🌊 당산의 운이 흉내합니다. 지혜와 감정이 조화를 이루며 있습니다.",
            'high': "🌪️ 홍수가 몸보기입니다. 감정 폭발과  \ud 혼란에 주의하세요."
        }
    }

    result = []
    for elem, score in elements.items():
        if score < 1.5:
            result.append(messages[elem]['low'])
        elif score > 3.5:
            result.append(messages[elem]['high'])
        else:
            result.append(messages[elem]['mid'])
    return "\n".join(result)

def get_ganzhi_from_date(date_str):
    base_date = datetime.strptime("1984-02-02", "%Y-%m-%d")
    target_date = datetime.strptime(date_str, "%Y-%m-%d")
    diff = (target_date - base_date).days
    stems = ['갑','을','병','정','무','기','경','신','임','계']
    branches = ['자','축','인','묘','진','사','오','미','신','유','술','해']
    return stems[diff % 10], branches[diff % 12]

def get_element_score_from_date(date_str):
    stem, branch = get_ganzhi_from_date(date_str)
    score = {'木': 0, '火': 0, '土': 0, '金': 0, '水': 0}
    if stem in element_map:
        score[element_map[stem]] += 1
    if branch in element_map:
        score[element_map[branch]] += 1
    return score

def get_saju_8char(birth: str, time: Optional[str]):
    dt = datetime.strptime(birth + (" " + time if time else ""), "%Y-%m-%d %H:%M" if time else "%Y-%m-%d")
    stems = ['갑','을','병','정','무','기','경','신','임','계']
    branches = ['자','축','인','묘','진','사','오','미','신','유','술','해']

    ipchun = datetime(dt.year, 2, 4)
    year = dt.year - 1 if dt < ipchun else dt.year
    year_gz = get_ganzhi_from_date(f"{year}-01-01")

    month_boundaries = [
        (1, 6), (2, 4), (3, 6), (4, 5), (5, 6), (6, 6),
        (7, 7), (8, 8), (9, 8), (10, 8), (11, 7), (12, 7)
    ]
    month_idx = 11
    for i, (m, d) in enumerate(month_boundaries):
        if dt < datetime(dt.year, m, d):
            month_idx = (i - 1) % 12
            break
    month_ref = datetime(dt.year, *month_boundaries[month_idx])
    month_gz = get_ganzhi_from_date(month_ref.strftime("%Y-%m-%d"))

    day_gz = get_ganzhi_from_date(dt.strftime("%Y-%m-%d"))
    saju = list(year_gz + month_gz + day_gz)

    if time:
        hour = dt.hour
        day_stem = day_gz[0]
        gan_map = {
            '갑': ['갑','을','병','정','무','기','경','신','임','계','갑','을'],
            '을': ['병','정','무','기','경','신','임','계','갑','을','병','정'],
            '병': ['무','기','경','신','임','계','갑','을','병','정','무','기'],
            '정': ['경','신','임','계','갑','을','병','정','무','기','경','신'],
            '무': ['임','계','갑','을','병','정','무','기','경','신','임','계'],
            '기': ['임','계','갑','을','병','정','무','기','경','신','임','계'],
            '경': ['병','정','무','기','경','신','임','계','갑','을','병','정'],
            '신': ['무','기','경','신','임','계','갑','을','병','정','무','기'],
            '임': ['경','신','임','계','갑','을','병','정','무','기','경','신'],
            '계': ['갑','을','병','정','무','기','경','신','임','계','갑','을']
        }
        hour_block = 0 if hour in [23, 0] else ((hour + 1) // 2) % 12
        hour_branch = branches[hour_block]
        hour_stem = gan_map.get(day_stem, stems)[hour_block]
        saju += [hour_stem, hour_branch]

    return saju

def count_elements(saju_chars):
    elements = {'木': 0, '火': 0, '土': 0, '金': 0, '水': 0}
    weights = [0.6, 0.3, 0.1]
    for char in saju_chars:
        if char in element_map:
            elements[element_map[char]] += 1
        elif char in zodiac_storage:
            for i, stem in enumerate(zodiac_storage[char]):
                if stem in element_map:
                    elements[element_map[stem]] += weights[i]
    return elements

def generate_lotto_numbers(birthdate_str, birthtime_str=None, refdate_str=None):
    saju_chars = get_saju_8char(birthdate_str, birthtime_str)
    today_elements = get_element_score_from_date(refdate_str) if refdate_str else {'木': 0, '火': 0, '土': 0, '金': 0, '水': 0}
    base_elements = count_elements(saju_chars)
    combined_elements = {e: base_elements[e] + today_elements[e] for e in base_elements}

    avg = sum(combined_elements.values()) / 5
    target_elements = sorted([e for e in combined_elements if combined_elements[e] < avg], key=lambda x: combined_elements[x])

    pool = []
    for e in target_elements:
        numbers = number_map[e].copy()
        random.shuffle(numbers)
        pool += numbers[:3]

    random.shuffle(pool)
    return sorted(pool[:6]), combined_elements, bool(birthtime_str)

# --- Streamlit 앱 ---
st.title("🎯 천기누설급 로또 번호 생성기")

st.markdown("""
😎 당신의 생년월일과 기준일을 입력하면, 사주로 오행 기운을 분석해
**결핍된 운세를 보완하는 방식**으로 로또 번호를 추천합니다.

- 출생 시간은 선택사항입니다.
- 오늘 날짜도 바꿔 입력하면 미래 기준 추천도 가능합니다.
""")

birth = st.text_input("🎂 생년월일 (예: 1989-12-08)")
time = st.text_input("⏰ 출생 시간 (예: 07:25) - 생략 가능", "")
ref = st.text_input("📅 기준 날짜 (예: 2025-04-21)")

if st.button("로또 번호 생성"):
    st.subheader("🔍 입력 정보")
    st.markdown(f"- 생년월일: {birth}")
    st.markdown(f"- 출생시간: {time if time else '미입력'}")
    st.markdown(f"- 기준일자: {ref}")
    st.markdown("---")

    try:
        time_input = time if time.strip() else None
        numbers, elements, used_time = generate_lotto_numbers(birth, time_input, ref)

        st.subheader("🎱 추천 로또 번호")
        st.markdown(", ".join(map(str, numbers)))

        st.subheader("📊 오행 분포")
        for k in ['木', '火', '土', '金', '水']:
            st.markdown(f"- {k}: {round(elements[k], 2)}")

        st.subheader("🧠 운세 해석")
        for line in interpret_elements(elements).splitlines():
            st.markdown(line)

        st.markdown("---")
        if used_time:
            st.success("🕒 시주까지 포함하여 사주 8자를 정밀 분석했습니다.")
        else:
            st.info("⚠️ 출생 시간이 입력되지 않아 시주는 포함되지 않았습니다.")

        st.markdown("\n👤 만든 사람: 천안 물주먹 이수민")
    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")
