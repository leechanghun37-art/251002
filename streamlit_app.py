import streamlit as st

st.title("🎈 My new app")


import numpy as np
import matplotlib.pyplot as plt

st.title("코시 연속성 ε-δ 시각 계산기 (개선판)")
st.write("함수, 점, ε 값을 쉽게 선택하고 δ 및 연속성 시각화를 확인하세요.")

# 대표 함수 선택 또는 직접 입력
func_options = {
    "x^2": "x**2",
    "sin(x)": "np.sin(x)",
    "exp(x)": "np.exp(x)",
    "1/x (x≠0)": "1/x if x!=0 else np.nan",
    "직접 입력": None
}
func_name = st.selectbox("함수 선택", list(func_options.keys()))
if func_options[func_name] is None:
    func_str = st.text_input("함수 f(x) 직접 입력 (예: x**3 + 2*x)", value="x**2")
else:
    func_str = func_options[func_name]

# 점 a 슬라이더 (범위 자동 조정)
a = st.slider("연속성 판정 점 a", min_value=-10.0, max_value=10.0, value=1.0, step=0.1)
# epsilon 슬라이더
epsilon = st.slider("ε 값 (양수)", min_value=0.001, max_value=2.0, value=0.1, step=0.001)

def f(x):
    try:
        return eval(func_str, {"x": x, "np": np, "__builtins__": {}})
    except Exception:
        return np.nan

if st.button("δ 및 연속성 시각화"):
    # δ 계산: 양방향, 수치적 오차 보정
    delta_candidates = np.linspace(0.00001, 2, 10000)
    found_delta = None
    fa = f(a)
    for delta in delta_candidates:
        x_left = np.linspace(a-delta, a, 50)
        x_right = np.linspace(a, a+delta, 50)
        x_vals = np.concatenate([x_left, x_right])
        fx_vals = f(x_vals)
        # nan, inf 값 제외
        valid = np.isfinite(fx_vals)
        if np.all(valid) and np.all(np.abs(fx_vals[valid] - fa) < epsilon):
            found_delta = delta
            break
    # 시각화
    fig, ax = plt.subplots(figsize=(7,4))
    x_plot = np.linspace(a-2, a+2, 400)
    y_plot = f(x_plot)
    ax.plot(x_plot, y_plot, label=f"f(x)")
    ax.axvline(a, color='r', linestyle='--', label='a')
    ax.axhline(fa, color='g', linestyle='--', label='f(a)')
    ax.fill_between(x_plot, fa-epsilon, fa+epsilon, color='yellow', alpha=0.3, label='ε 범위')
    if found_delta:
        ax.axvspan(a-found_delta, a+found_delta, color='cyan', alpha=0.2, label='δ 범위')
        st.success(f"적당한 δ 값: {found_delta:.6f}")
        st.info(f"모든 x∈({a-found_delta:.3f}, {a+found_delta:.3f})에서 |f(x)-f(a)|<{epsilon} 입니다.")
    else:
        st.error("해당 ε에 대해 δ를 찾을 수 없습니다. 함수 또는 입력값을 확인하세요.")
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.legend()
    st.pyplot(fig)

    # 연속성 판정 안내
    if found_delta:
        st.success(f"함수는 x={a}에서 ε={epsilon}에 대해 연속입니다.")
    else:
        st.warning(f"함수는 x={a}에서 ε={epsilon}에 대해 연속이 아닐 수 있습니다.")
