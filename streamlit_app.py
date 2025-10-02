import streamlit as st

st.title("🎈 My new app")

import numpy as np
import matplotlib.pyplot as plt

st.title("코시의 연속 정의: ε-δ 계산기")

st.write("연속함수 $f(x)$, 점 $a$, 그리고 $\epsilon$ 값을 입력하면, $|x-a|<\delta$일 때 $|f(x)-f(a)|<\epsilon$을 만족하는 최소 $\delta$ 값을 계산합니다.")

# 함수 입력
func_str = st.text_input("함수 f(x) 입력 (예: x**2, np.sin(x), np.exp(x))", value="x**2")
a = st.number_input("점 a 입력", value=1.0)
epsilon = st.number_input("ε 값 입력 (양수)", min_value=0.0001, value=0.1, format="%f")

def f(x):
    try:
        return eval(func_str, {"x": x, "np": np, "__builtins__": {}})
    except Exception:
        return np.nan

if st.button("δ 계산하기"):
    # delta를 수치적으로 근사
    delta_candidates = np.linspace(0.00001, 2, 10000)
    found_delta = None
    for delta in delta_candidates:
        x_vals = np.linspace(a-delta, a+delta, 100)
        fx_vals = f(x_vals)
        if np.all(np.abs(fx_vals - f(a)) < epsilon):
            found_delta = delta
            break
    if found_delta:
        st.success(f"적당한 δ 값: {found_delta:.6f}")
        # 시각화
        fig, ax = plt.subplots()
        x_plot = np.linspace(a-2*found_delta, a+2*found_delta, 400)
        y_plot = f(x_plot)
        ax.plot(x_plot, y_plot, label=f"f(x) = {func_str}")
        ax.axvline(a, color='r', linestyle='--', label='a')
        ax.fill_between(x_plot, f(a)-epsilon, f(a)+epsilon, color='yellow', alpha=0.3, label='ε 범위')
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.legend()
        st.pyplot(fig)
    else:
        st.error("해당 ε에 대해 δ를 찾을 수 없습니다. 함수 또는 입력값을 확인하세요.")
