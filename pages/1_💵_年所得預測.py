import streamlit as st
import joblib,csv

# 載入模型與標準化轉換模型
UCI_model = joblib.load('./MODEL/UCI_model.joblib')
scaler = joblib.load('./MODEL/UCI_scaler.joblib')

list_feature = []
with open('./MODEL/feature_names.csv', 'r') as csv_f:
    reader = csv.reader(csv_f, delimiter=',')
    for row in reader:
        list_feature.append(row)


list1 = [0 for _ in range(14)]
st.title('屬性資料預測年所得')
col1, col2 = st.columns(2)
with col1:
    list1[0] = st.slider(list_feature[0][0], value=37, min_value=17, max_value=90)              # Age
    list1[1] = list_feature[1].index(st.selectbox(list_feature[0][1], list_feature[1]))         # workclass
    list1[2] = st.slider(list_feature[0][2], value=17850, min_value=13000, max_value=1500000)   # fnlwgt
    list1[3] = list_feature[2].index(st.selectbox(list_feature[0][3], list_feature[2]))         # education
    list1[4] = st.slider(list_feature[0][4], value=10, min_value=1, max_value=16)               # education-num
    list1[5] = list_feature[3].index(st.selectbox(list_feature[0][5], list_feature[3]))         # marital-status
    list1[6] = list_feature[4].index(st.selectbox(list_feature[0][6], list_feature[4]))         # occupation
with col2:    
    list1[7] = list_feature[5].index(st.selectbox(list_feature[0][7], list_feature[5]))         # relationship
    list1[8] = list_feature[6].index(st.selectbox(list_feature[0][8], list_feature[6]))         # race
    list1[9] = 0 if st.radio(list_feature[0][9], options=('M', 'F'))=='M' else 1                # sex
    list1[10] = st.slider(list_feature[0][10], value=0, min_value=0, max_value=100000)          # capital-gain
    list1[11] = st.slider(list_feature[0][11], value=0, min_value=0, max_value=5000)            # capital-loss
    list1[12] = st.slider(list_feature[0][12], value=40, min_value=1, max_value=99)             # hours-per-week
    list1[13] = list_feature[8].index(st.selectbox(list_feature[0][13], list_feature[8]))       # native-country

labels = list_feature[9]                                                                        # labels
if st.button('預測'):
    X_new = [list1]
    X_new = scaler.transform(X_new)
    st.write(f'### 預測所得：',labels[UCI_model.predict(X_new)[0]])

