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
    result = []
    for elem, score in elements.items():
        if score == 0:
            result.append(f"⚠️ {elem} 기운이 완전히 결핍되어 있음 → 이 영역에 주의 필요")
        elif score < 1.5:
            result.append(f"🔹 {elem} 기운이 약함 → 관련된 운(행동/재물/감정 등)이 약할 수 있음")
        elif score >= 3.5:
            result.append(f"🔥 {elem} 기운이 과다 → 과한 에너지로 인한 불균형 가능")
        else:
            result.append(f"✅ {elem} 기운이 안정됨 → 이 기운과 관련된 영역이 조화로움")
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

def get_filtered_pool(elements):
    pool = []
    for elem, score in elements.items():
        if score < 1.5:
            pool += number_map[elem][:3]
        elif score > 3.5:
            pool += number_map[elem][:1]
        else:
            pool += number_map[elem][:2]
    return pool

def generate_lotto_numbers(birthdate_str, birthtime_str=None, refdate_str=None):
    saju_chars = get_saju_8char(birthdate_str, birthtime_str)
    today_elements = get_element_score_from_date(refdate_str) if refdate_str else {'木': 0, '火': 0, '土': 0, '金': 0, '水': 0}
    base_elements = count_elements(saju_chars)
    combined_elements = {e: base_elements[e] + today_elements[e] for e in base_elements}
    filtered_pool = get_filtered_pool(combined_elements)
    if len(filtered_pool) == 0:
        return [], combined_elements, bool(birthtime_str)
    if len(filtered_pool) < 6:
        final_numbers = sorted(random.sample(filtered_pool, len(filtered_pool)))
    else:
        final_numbers = sorted(random.sample(filtered_pool, 6))
    return final_numbers, combined_elements, bool(birthtime_str)

# Streamlit 앱 UI
st.markdown("## 🎯 이수민의 사주 기반 로또 번호 생성기")

st.markdown("""
- 생년월일과 기준일을 입력하면, 사주 기반 오행을 분석해 로또 번호를 추천합니다.
- 출생 시간은 선택사항입니다.
""")

birth = st.text_input("🎂 생년월일 (예: 1989-12-08)")
time = st.text_input("⏰ 출생 시간 (예: 07:25) - 생략 가능", "")
ref = st.text_input("📅 기준 날짜 (예: 2025-04-21)")

if st.button("로또 번호 생성"):
    st.subheader("🔎 입력 정보")
    st.markdown(f"- **생년월일**: {birth}")
    st.markdown(f"- **출생시간**: {time if time else '미입력'}")
    st.markdown(f"- **기준일자**: {ref}")
    st.markdown("---")
    try:
        time_input = time if time.strip() else None
        numbers, elements, used_time = generate_lotto_numbers(birth, time_input, ref)

        st.subheader("📌 추천 로또 번호")
        st.markdown("🎱 " + ", ".join(str(n) for n in numbers))

        st.subheader("📊 오행 분포")
        for k in ['木', '火', '土', '金', '水']:
            st.markdown(f"- **{k}**: {elements[k]}")

        st.subheader("🧠 해석")
        for line in interpret_elements(elements).splitlines():
            st.markdown(line)

        if used_time:
            st.success("🕒 시주까지 포함하여 사주 8자를 정밀 분석했습니다.")
            st.markdown("---  \n👤 만든 사람: **천안 물주먹 이수민님**")
        else:
            st.warning("⚠️ 출생 시간이 입력되지 않아 시주는 포함되지 않았습니다.")
            st.markdown("---  \n👤 만든 사람: **천안 물주먹 이수민님**")

    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")
