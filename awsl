import streamlit as st
import pandas as pd
import numpy as np

df_database = pd.read_csv("./zhibiaokanban.csv")

st.set_page_config(layout="wide")

row0_spacer1, row0_1, row0_spacer2 = st.columns((.1, 3.2, .1))
with row0_1:
    st.subheader('指标看板 - 当月个创奖比例')


row1_spacer1, row1_1, row1_spacer2 = st.columns((.1, 3.2, .1))

with row1_1:
    st.markdown("统计月个人创业发展奖合计除以统计月个人出年度佣金合计。举例：评估2023年5月营业部A的当月个创奖比例，分子为：营业部A在2023年5月个人创业发展奖合计，分母为：营业部A在2023年5月个人创业初年度佣金金额合计；指标评估时间：2023年7月1日。")


# 创建一个函数来生成带有边框的metric卡片  
def custom_metric(label, value, border_color='black', border_width='1px'):  
    # 使用HTML和CSS创建一个带有边框的div元素  
    html_template = f"""  
    <div style="border: {border_width} solid {border_color}; padding: 10px; margin: 5px;">  
        <p style="font-weight: bold; margin-bottom: 5px;">{label}:</p>  
        <p style="font-size: 25px;">{value}</p>  
    </div>  
    """  
    return html_template

# 创建
row2_spacer1, row2_1, row2_spacer2 ,row2_2 ,row2_spacer3,row2_3,row2_spacer4,row2_4,row2_spacer4 = st.columns((.25, 2, .1, 2, .1, 2, .1, 2, .45))

# 在第一个列中显示带有边框的metric  
with row2_1:  
    sales_value = df_database['Jxl'].count()  
    metric_html = custom_metric('总观测数', sales_value, border_color='blue', border_width='2px')  
    st.markdown(metric_html, unsafe_allow_html=True)  
  
# 在第二个列中显示带有边框的metric  
with row2_2:  
    profit_value = df_database['Jxl'].max()  
    metric_html = custom_metric('最大值', profit_value, border_color='green', border_width='2px')  
    st.markdown(metric_html, unsafe_allow_html=True)  
  
# 在第三列中显示带有边框的metric  
with row2_3:  
    customers_value = df_database['Jxl'].min()  
    metric_html = custom_metric('最小值', customers_value, border_color='red', border_width='2px')  
    st.markdown(metric_html, unsafe_allow_html=True)

# 在第四列中显示带有边框的metric  
with row2_4:  
    customers_value = df_database['Jxl'].mean().round(2)  
    metric_html = custom_metric('均值', customers_value, border_color='orange', border_width='2px')  
    st.markdown(metric_html, unsafe_allow_html=True)

# 空白行
st.markdown('')

row3_spacer1, row3_1, row0_spacer3 = st.columns((.1, 3.2, .1))
with row3_1:
    st.markdown('##### 表格区域')


# 假设我们有三个筛选条件，分别对应三列数据的可能值  
column1_choices = df_database['Branch_code1'].unique()  
column2_choices_initial = df_database['Branch_code2'].unique()  
column3_choices_initial = df_database['Branch_code3'].unique() 

# 初始化筛选条件变量  
selected_column1 = None  
selected_column2 = None  
selected_column3 = None 


# 在第一列中放置第一个筛选条件  
col0, col1, col2, col3, col4 = st.columns((.3, 3, 3, 3 ,.4))
selected_column1 = col1.selectbox('分公司', column1_choices)  
      
# 根据第一个筛选条件的结果，更新第二个筛选条件的选项  
if selected_column1 is not None:  
    df_filtered_by_column1 = df_database[df_database['Branch_code1'] == selected_column1]  
    column2_choices_filtered = df_filtered_by_column1['Branch_code2'].unique()  
          
    # 在第二列中放置第二个筛选条件  
    selected_column2 = col2.selectbox('四级机构', column2_choices_filtered)  
          
    # 根据前两个筛选条件的结果，更新第三个筛选条件的选项  
    if selected_column2 is not None:  
        df_filtered_by_both = df_filtered_by_column1[df_filtered_by_column1['Branch_code2'] == selected_column2]  
        column3_choices_filtered = df_filtered_by_both['Branch_code3'].unique()  
              
        # 在第三列中放置第三个筛选条件  
        selected_column3 = col3.selectbox('业务部', column3_choices_filtered) 

# 根据筛选条件筛选数据  
if selected_column1 is not None and selected_column2 is not None and selected_column3 is not None:  
    filtered_df = df_database[(df_database['Branch_code1'] == selected_column1) &  
                          (df_database['Branch_code2'] == selected_column2) &  
                          (df_database['Branch_code3'] == selected_column3)]  
elif selected_column1 is not None and selected_column2 is not None:  
    filtered_df = df_database[(df_database['Branch_code1'] == selected_column1) &  
                          (df_database['Branch_code2'] == selected_column2)]  
elif selected_column1 is not None:  
    filtered_df = df_database[df_database['Branch_code1'] == selected_column1]  
else:  
    filtered_df = df_database  # 如果没有选择任何筛选条件，则显示所有数据 

# 显示筛选后的数据表格
row4_spacer1, row4_1, row0_spacer4 = st.columns((.1, 3.2, .13))
with row4_1:
    st.dataframe(filtered_df,use_container_width=True)


# 空白行
st.markdown('')

row5_spacer1, row5_1, row0_spacer5 = st.columns((.1, 3.2, .1))
with row5_1:
    st.markdown('##### 图表区域')
