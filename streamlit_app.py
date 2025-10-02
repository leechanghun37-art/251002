st.title("🎈 My new app")

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 전문적인 페이지 레이아웃 및 스타일
st.set_page_config(
    page_title="수학 함수 그래프 & ε-δ 연속성 시각화",
    page_icon="📈",
    layout="wide",
)

st.markdown("""
<style>
.main {
    background-color: #f7f7fa;
}
.stApp {
    font-family: 'Noto Sans KR', 'Roboto', Arial, sans-serif;
}
.stTitle, .stHeader, .stMarkdown h2 {
    color: #2a3f5f;
}
.stMarkdown code {
    background: #eaf1fb;
    color: #1a2b3c;
}
</style>
""", unsafe_allow_html=True)

st.title("수학 함수 그래프 & ε-δ 연속성 시각화")
st.markdown("""
이 페이지는 수학에서 자주 사용하는 주요 함수들의 그래프 개형과, 코시의 연속 정의(ε-δ)를 시각적으로 탐구할 수 있도록 설계되었습니다. 

**함수 종류를 선택하거나 직접 입력**하면, 해당 함수의 그래프와 연속성(δ, ε)을 직관적으로 확인할 수 있습니다. 

함수의 정의역, 불연속점, 점근선, 치역 등도 자동으로 반영됩니다. 

---
""")


# 주요 함수 종류별 대표 수식, 정의역, 그래프 스타일
func_types = {
    "상수함수 y=c": {"expr": "2", "domain": (-10, 10)},
    "일차함수 y=ax+b": {"expr": "x", "domain": (-10, 10)},
    "이차함수 y=ax^2+bx+c": {"expr": "x**2", "domain": (-10, 10)},
    "삼차함수 y=ax^3+...": {"expr": "x**3", "domain": (-10, 10)},
    "사차함수 y=ax^4+...": {"expr": "x**4", "domain": (-10, 10)},
    "유리함수 y=1/x": {"expr": "1/x", "domain": (-10, 10)},
    "무리함수 y=sqrt(x)": {"expr": "np.sqrt(x)", "domain": (0, 10)},
    "지수함수 y=exp(x)": {"expr": "np.exp(x)", "domain": (-3, 3)},
    "로그함수 y=log(x)": {"expr": "np.log(x)", "domain": (0.01, 10)},
    "사인함수 y=sin(x)": {"expr": "np.sin(x)", "domain": (-2*np.pi, 2*np.pi)},
    "코사인함수 y=cos(x)": {"expr": "np.cos(x)", "domain": (-2*np.pi, 2*np.pi)},
    "탄젠트함수 y=tan(x)": {"expr": "np.tan(x)", "domain": (-2*np.pi, 2*np.pi)},
    "절댓값함수 y=|x|": {"expr": "np.abs(x)", "domain": (-10, 10)},
    "계단함수 y=floor(x)": {"expr": "np.floor(x)", "domain": (-10, 10)},
    "가우스함수 y=exp(-x^2)": {"expr": "np.exp(-x**2)", "domain": (-4, 4)},
    "직접 입력": {"expr": None, "domain": (-10, 10)}
}

# 사이드바: 함수 선택 및 입력
with st.sidebar:
    st.header("함수 종류 및 입력")
    func_name = st.selectbox("함수 종류 선택", list(func_types.keys()))
    if func_types[func_name]["expr"] is None:
        func_str = st.text_input("함수 f(x) 직접 입력 (예: x**3 + 2*x)", value="x**2")
        domain = st.slider("그래프 x축 범위", min_value=-20.0, max_value=20.0, value=(-10.0, 10.0), step=0.1)
    else:
        func_str = func_types[func_name]["expr"]
        domain = func_types[func_name]["domain"]
    st.markdown("""
    - **상수함수**: y=c
    - **일차함수**: y=ax+b
    - **이차함수**: y=ax²+bx+c
    - **삼차/사차함수**: y=ax³+.../y=ax⁴+...
    - **유리함수**: y=1/x
    - **무리함수**: y=√x
    - **지수/로그함수**: y=exp(x), y=log(x)
    - **삼각함수**: y=sin(x), y=cos(x), y=tan(x)
    - **절댓값/계단/가우스**: y=|x|, y=floor(x), y=exp(-x²)
    """)


col1, col2 = st.columns([2,1])
with col2:
    st.subheader("연속성 판정 파라미터")
    a = st.slider("연속성 판정 점 a", min_value=float(domain[0]), max_value=float(domain[1]), value=float((domain[0]+domain[1])/2), step=0.1)
    epsilon = st.slider("ε 값 (양수)", min_value=0.001, max_value=2.0, value=0.1, step=0.001)

def f(x):
    try:
        return eval(func_str, {"x": x, "np": np, "__builtins__": {}})
    except Exception:
        return np.nan

with col1:
    st.subheader("함수 그래프 및 δ-ε 시각화")
    st.markdown("""
    - **파란 곡선**: 함수 $f(x)$의 그래프
    - **노란 영역**: $|f(x)-f(a)|<\epsilon$ 범위
    - **하늘색 영역**: $|x-a|<\delta$ 범위
    - **빨간 x**: 불연속점/정의불가
    - **초록선**: $f(a)$, **빨간선**: $a$
    """, unsafe_allow_html=True)
    if st.button("그래프 그리기 및 δ-ε 시각화"):
        # 모든 ε에 대해 δ(최대 δ) 값 계산
        epsilons = np.linspace(0.01, 2.0, 30)
        deltas = []
        fa = f(a)
        for eps in epsilons:
            delta_candidates = np.linspace(eps/2, 2*eps, 500)
            found_delta = None
            for delta in delta_candidates:
                x_left = np.linspace(a-delta, a, 50)
                x_right = np.linspace(a, a+delta, 50)
                x_vals = np.concatenate([x_left, x_right])
                fx_vals = f(x_vals)
                valid = np.isfinite(fx_vals)
                if np.all(valid) and np.all(np.abs(fx_vals[valid] - fa) < eps):
                    found_delta = delta
                    break
            deltas.append(found_delta if found_delta else np.nan)
        # 표로 δ-ε 관계 출력
        st.markdown("#### ε-δ 관계표")
        st.dataframe({"ε": epsilons, "δ(최대)": deltas})

        # 선택한 ε에 대한 δ 및 그래프 시각화
        delta_candidates = np.linspace(epsilon/2, 2*epsilon, 500)
        found_delta = None
        for delta in delta_candidates:
            x_left = np.linspace(a-delta, a, 50)
            x_right = np.linspace(a, a+delta, 50)
            x_vals = np.concatenate([x_left, x_right])
            fx_vals = f(x_vals)
            valid = np.isfinite(fx_vals)
            if np.all(valid) and np.all(np.abs(fx_vals[valid] - fa) < epsilon):
                found_delta = delta
                break
        x_plot = np.linspace(domain[0], domain[1], 1200)
        def safe_f(xx):
            try:
                vals = np.array([f(xi) for xi in xx])
            except Exception:
                vals = np.full_like(xx, np.nan)
            return vals
        y_plot = safe_f(x_plot)
        mask = np.isfinite(y_plot)
        fig, ax = plt.subplots(figsize=(9,5))
        ax.plot(x_plot[mask], y_plot[mask], label="$f(x)$", color='#1976d2', linewidth=2)
        if not np.all(mask):
            ax.scatter(x_plot[~mask], np.full(np.sum(~mask), 0), color='#d32f2f', marker='x', label='불연속/정의불가')
        ax.axvline(a, color='#c62828', linestyle='--', label='$a$', linewidth=2)
        ax.axhline(fa, color='#388e3c', linestyle='--', label='$f(a)$', linewidth=2)
        ax.fill_between(x_plot, fa-epsilon, fa+epsilon, color='#fffde7', alpha=0.5, label='$|f(x)-f(a)|<\epsilon$')
        # δ 범위
        if found_delta:
            ax.axvspan(a-found_delta, a+found_delta, color='#b3e5fc', alpha=0.4, label='$|x-a|<\delta$')
            st.success(f"적당한 δ 값: {found_delta:.6f}")
            st.info(f"모든 x∈({a-found_delta:.3f}, {a+found_delta:.3f})에서 |f(x)-f(a)|<{epsilon} 입니다.")
        else:
            st.error("해당 ε에 대해 δ를 찾을 수 없습니다. 함수 또는 입력값을 확인하세요.")
        ax.set_xlabel('x', fontsize=13)
        ax.set_ylabel('f(x)', fontsize=13)
        # y축 자동 스케일링
        if np.any(mask):
            y_min, y_max = np.nanmin(y_plot[mask]), np.nanmax(y_plot[mask])
            if y_max-y_min < 1e-6:
                ax.set_ylim(fa-1, fa+1)
            else:
                ax.set_ylim(y_min-(y_max-y_min)*0.2, y_max+(y_max-y_min)*0.2)
        ax.legend(fontsize=12, loc='best')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

    # 연속성 판정 안내
    if found_delta:
        st.success(f"함수는 x={a}에서 ε={epsilon}에 대해 연속입니다.")
    else:
        st.warning(f"함수는 x={a}에서 ε={epsilon}에 대해 연속이 아닐 수 있습니다.")
