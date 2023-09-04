# streamlit run HW03_web_Solution

# 若出現錯誤：TypeError: Descriptors cannot not be created directly. 可執行下列指令：
# Set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# streamlit user guide
# https://docs.streamlit.io/en/stable/api.html#display-interactive-widgets

import streamlit as st
# from sympy.solvers import solve
# from sympy import symbols
# from sympy.core import sympify
import numpy as np
import matplotlib.pyplot as plt

def gradient_descent(f_func,df,x_init,lr,run_iter,stop_limit):
    try:

        draw_function(f_func,df,x,x_hist,df_hist)
    except:
        print('Inappropriate parameter')

def draw_function(f_func,df_func,final_x,x_hist,df_hist):
# def draw_function(f_func):    
    Xmin = -10
    Xmax = 10
    x = np.linspace(Xmin, Xmax, 1000)
    y = [f_func(i) for i in x]
    y_hist = [f_func(i) for i in x_hist]
    fig, ax = plt.subplots()
    # plt.figure(figsize=(12,6),constrained_layout=True)
    ax = plt.subplot(121)
    ax.plot(x,y, color='green',label='f(x)')
    ax.scatter(x_hist,y_hist, color='blue',label="gradient",s=5)
    ax.scatter(final_x,f_func(final_x), color='red',s=20)
    ax.set_title(get_function_source(f_func),{'fontsize':10,'color':'k'})
    ax.set_xlabel('x',{'fontsize':10,'color':'k'})
    ax.set_ylabel('f(x)',{'fontsize':10,'color':'k'})

    ax.plot([final_x-2,final_x+2],[f_func(final_x)-(df_func(final_x)),f_func(final_x)+(df_func(final_x))], color='purple')
    ax.grid(True)
    ax.legend()
    ax = plt.subplot(122)
    x1 = [i for i in range(len(df_hist))]
    ax.scatter(x1,df_hist, color='red',label='slope',s=5)
    ax.set_xlabel('time',{'fontsize':10,'color':'k'})
    ax.set_ylabel("slope",{'fontsize':10,'color':'k'})
    ax.legend()
    ax.grid(True)
    # print(f"Final x = {final_x: .2f}, final f(x) = {f_func(final_x): .2f}, slope = {df_func(final_x): .2e}")
    st.pyplot(fig)



f1 = lambda x: 5*x**2 + 3*x + 6
df1 = lambda x: 10*x + 3

Xmin = -10
Xmax = 10
x = np.linspace(Xmin, Xmax, 1000)
y1 = [f1(i) for i in x]
dy1 = [df1(i) for i in x]
col1, col2 = st.columns(2) 
with col1:
    st.markdown('# 函數與導數')
    fig, ax = plt.subplots()
    ax.plot(x,y1, color='green',label='$f(x)$')
    ax.plot(x,dy1, color='blue',label="$f'(x)$")
    ax.set_title('$ f(x) = 5x^2 + 3x + 6$',{'fontsize':10,'color':'red'})
    ax.set_xlabel('x',{'fontsize':10,'color':'k'})
    ax.set_ylabel('f(x)',{'fontsize':10,'color':'k'})
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

   
with col2:
    lr = st.slider('學習率(e-3)', value=5, min_value=1, max_value=100) /(1e3)
    init_v = st.slider('初始值', value=0, min_value=-8, max_value=8)
    epoch = st.slider('迭代次數', value=2000, min_value=100, max_value=5000)
    stop_limit = st.slider('中止斜率條件(e-4)', value=0, min_value=-100, max_value=100) / (1e4)
    

x_hist = []
df_hist = []
x = init_v
df_last = df1(x)
for i in range(epoch):
    df_value = df1(x)
    x_hist.append(x)
    df_hist.append(df_value)

    if abs(df_value) > abs(df_last):
        df_value = -df_value
    x = x - (lr*df_value)
    df_last = df_value
    final_x = x
    if abs(df_value) < stop_limit:
        break
Xmin = -10
Xmax = 10
x = np.linspace(Xmin, Xmax, 1000)
y = [f1(i) for i in x]
y_hist = [f1(i) for i in x_hist]
fig, ax = plt.subplots()
# plt.figure(figsize=(12,6),constrained_layout=True)
ax = plt.subplot(121)
ax.plot(x,y, color='green',label='f(x)')
ax.scatter(x_hist,y_hist, color='blue',label="gradient",s=5)
ax.scatter(final_x,f1(final_x), color='red',s=20)
ax.set_title('$ f(x) = 5x^2 + 3x + 6$',{'fontsize':10,'color':'red'})
ax.set_xlabel('x',{'fontsize':10,'color':'k'})
ax.set_ylabel('f(x)',{'fontsize':10,'color':'k'})

ax.plot([final_x-2,final_x+2],[f1(final_x)-(df1(final_x)),f1(final_x)+(f1(final_x))], color='purple')
ax.grid(True)
ax.legend()
ax = plt.subplot(122)
x1 = [i for i in range(len(df_hist))]
ax.scatter(x1,df_hist, color='red',label='slope',s=5)
ax.set_xlabel('iter',{'fontsize':10,'color':'k'})
ax.set_ylabel("slope",{'fontsize':10,'color':'k'})
ax.legend()
ax.grid(True)
# print(f"Final x = {final_x: .2f}, final f(x) = {f_func(final_x): .2f}, slope = {df_func(final_x): .2e}")
st.pyplot(fig)


