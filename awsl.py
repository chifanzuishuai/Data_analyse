import streamlit as st
import numpy as np
import pandas as pd
import pickle
import time


import seaborn as sns
import datetime

from pyecharts.charts import *
from pyecharts.globals import ThemeType
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
import streamlit.components.v1 as components
from streamlit_echarts import st_echarts

st.set_page_config(layout="wide")

# 全局变量

zhibiao_name = "当月个创奖比例"

df_database = pd.read_csv("./zhibiaokanban.csv")
df_database['Fact_date'] = pd.to_datetime(df_database['Fact_date'])  

# 侧边栏部分

st.sidebar.markdown('# 指标看板')

st.sidebar.markdown("**选择您要统计的数据时间区间:** 👇")

st.session_state.date_time=datetime.datetime.now() + datetime.timedelta(hours=-80000) 
Srart_date = st.sidebar.date_input('开始日期',st.session_state.date_time.date(),key='Srart_date')
End_date = st.sidebar.date_input('结束日期',st.session_state.date_time.now(),key='End_date')

Srart_date = pd.to_datetime(Srart_date)
End_date = pd.to_datetime(End_date)

unique_branch = ['分公司1','分公司2','分公司3','分公司4']
branch_selected = st.sidebar.selectbox('您想仅看某个分公司的数据吗?如果您有这个需要，请在下方选择“分公司”，并在新出现的字段中选择相应的分公司。', ['总公司','分公司'])
if branch_selected == '分公司':
    selected_branch = st.sidebar.selectbox("选择您关心的分公司", unique_branch)

## 数据筛选
if branch_selected == '总公司':
    filtered_df = df_database[(df_database['Fact_date'] >= Srart_date) & (df_database['Fact_date'] <= End_date)]
else:
    filtered_df = df_database[(df_database['Fact_date'] >= Srart_date) & (df_database['Fact_date'] <= End_date) & (df_database['Branch_code1'] == selected_branch)]


# 测试筛选条件用
# st.dataframe(filtered_df,use_container_width=True)




# 主体部分

row0_spacer1, row0_1, row0_spacer2 = st.columns((.2, 7.1, .2))
with row0_1:
    st.subheader('当月个创奖比例')

row1_spacer1, row1_1, row1_spacer2 = st.columns((.2, 7.1, .2))

with row1_1:
    st.markdown("统计月个人创业发展奖合计除以统计月个人出年度佣金合计。举例：评估2023年5月营业部A的当月个创奖比例，分子为：营业部A在2023年5月个人创业发展奖合计，分母为：营业部A在2023年5月个人创业初年度佣金金额合计；指标评估时间：2023年7月1日。")

row2_spacer1, row2_1, row2_spacer2 = st.columns((.2, 7.1, .2))
with row2_1:
    st.markdown("#####  当前选择数据:")


row3_spacer1, row3_1, row3_spacer2, row3_2, row3_spacer3, row3_3, row3_spacer4, row3_4, row3_spacer5   = st.columns((.2, 1.6, .2, 1.6, .2, 1.6, .2, 1.6, .2))
with row3_1:
    guanceshu = filtered_df['Fact_date'].count()
    str_guanceshu = "🏟️ "  +  str(guanceshu) + " " + " Observation"  
    st.markdown(str_guanceshu)  
with row3_2:
    zuida = filtered_df['Jxl'].max()
    str_zuida = "🏃‍♂️ " + str(zuida) + " " + "Maximum"
    st.markdown(str_zuida)
with row3_3:
    zuixiao = filtered_df['Jxl'].min()
    str_zuixiao = "🥅 " + str(zuixiao) + " " + "Minimum"
    st.markdown(str_zuixiao)
with row3_4:
    mean = filtered_df['Jxl'].mean().round(2)
    str_mean = "👟 " + str(mean) + " " + "Mean"
    st.markdown(str_mean)


row4_spacer1, row4_1, row4_spacer2 = st.columns((.2, 7.1, .2))
with row4_1:
    st.markdown("")
    see_data = st.expander('您可以点击这里查看原始数据 👉')
    with see_data:
        st.dataframe(data=filtered_df[['Year','Month','Branch_code1','Branch_code2','Branch_code3','Jxl','Jxl_fz','Jxl_fm']].reset_index(drop=True),use_container_width=True)
st.text('')


# 时序图部分
row5_spacer1, row5_1, row5_spacer2 = st.columns((.2, 7.1, .2))

filtered_df['year_month'] = filtered_df['Year'].astype(str) + "-" + filtered_df['Month'].astype(str)
data1 =  filtered_df.groupby('year_month')[['Jxl_fz', 'Jxl_fm']].sum().reset_index()           
data1['Jxl'] = round(data1['Jxl_fz']/data1['Jxl_fm'],2)

x_axis_data = data1['year_month'].tolist()  
y_axis_data = data1['Jxl'].tolist()  

if branch_selected == '总公司':
    title_text1 = branch_selected 
else:
    title_text1 = selected_branch

with row5_1:
    st.markdown("")
    option = {
       "title": {
         "left": 'center',
         "text": title_text1 + '-' +  zhibiao_name + "时序图"
         },
       "tooltip": {
          "trigger": 'axis'
         },
       "toolbox": {
        "show": "true",
        "right": '15',
        "feature": {
            "mark": {"show": "true"},
            "dataView": {"show": "true", "readOnly": "false"},
            "restore": {"show": "true"}
        }
         },
      "xAxis": {
        "type": 'category',
        "data": x_axis_data
         },
      "yAxis": {
        "type": 'value',
        "min": 0,  # y轴最小值  
        "max": 1  # y轴最大值  
         },
      "series": [
        {
          "data": y_axis_data,
          "type": 'line'
        }
        ],
      "dataZoom": [  # 数据区域缩放组件  
        {  
            "type": "slider",  # 滑块型数据区域缩放组件  
            "start": 50,  # 左边在 10% 的位置。  
            "end": 100  # 右边在 60% 的位置。  
        },  
        {  
            "type": "inside",  # 内置型数据区域缩放组件  
            "start": 50,  
            "end": 100  
        }  
    ]  
    };
    st_echarts(options=option,height='380px',width='100%' , key="时序图")


row6_spacer1, row6_1, row6_spacer2 = st.columns((.2, 7.1, .2))
with row6_1:
    st.subheader('Analysis per Team')

row7_spacer1, row7_1, row7_spacer2, row7_2, row7_spacer3, row7_3, row7_spacer4, row7_4, row7_spacer5   = st.columns((.2, 1.6, .2, 1.6, .2, 1.6, .2, 1.6, .2))
with row7_1:
    sijijigou = filtered_df['Branch_code2'].nunique()
    str_sijijigou = "🏟️ "  +  str(sijijigou) + " " + " Nniform"  
    st.markdown(str_sijijigou)  
with row7_2:
    yewubu = filtered_df['Branch_code3'].nunique()
    str_yewubu = "🏃‍♂️ " + str(yewubu) + " " + "Department"
    st.markdown(str_yewubu)
with row7_3:
    zuixiao = filtered_df['Jxl'].min()
    str_zuixiao = "🥅 " + str(zuixiao) + " " + "Minimum"
    st.markdown(str_zuixiao)
with row7_4:
    mean = filtered_df['Jxl'].mean().round(2)
    str_mean = "👟 " + str(mean) + " " + "Mean"
    st.markdown(str_mean)


row8_spacer1, row8_1, row8_spacer2, row8_2, row8_spacer3  = st.columns((.2, 2.5, .3, 4.2, .1))
unique_level = ['四级机构','业务部']
type1 = ['全部','个例']
with row8_1:
    st.markdown("")
    st.markdown('分析四级机构维度或业务部维度指标的数据分布机构维度或业务部维度指标的数据分布')    
    per_level_selected = st.selectbox ("您想要分析的维度是什么?", unique_level, key = 'Branch_code2')
    per_type_selected = st.selectbox ("您想要分析具体的样本，请在下方选择'个例'?", type1, key = '分析类别')
    if per_type_selected == '个例':
        comparison_branchcode = st.checkbox("是否需要对比两个样本？")


# 箱线图
data2 =  filtered_df.groupby(['year_month','Branch_code2'])[['Jxl_fz', 'Jxl_fm']].sum().reset_index()           
data2['Jxl'] = round(data2['Jxl_fz']/data2['Jxl_fm'],2)
data3 =  filtered_df.groupby(['year_month','Branch_code3'])[['Jxl_fz', 'Jxl_fm']].sum().reset_index()           
data3['Jxl'] = round(data3['Jxl_fz']/data3['Jxl_fm'],2)
if per_level_selected == '四级机构':
    boxplot_data = data2['Jxl'].tolist() 
else:
    boxplot_data = data3['Jxl'].tolist() 

boxplot_text = per_level_selected + "维度箱线图"

with row8_2:
    option = {
    "title": [
     {
       "text": boxplot_text,
       "left": 'center',
       "textStyle": {   
            "fontFamily": 'Arial',
            "fontSize": 15   
        }  
    },
    {
      "text": 'upper: Q3 + 1.5 * IQR  lower: Q1 - 1.5 * IQR',
      "borderWidth": 1,
      "textStyle": {
        "fontSize": 10
      },
      "left": '10%',
      "top": '92%'
    }
     ],
    "dataset": [
    {
      "source": [
                boxplot_data
            ]
    },
    {
      "transform": {
        "type": 'boxplot',
        "config": {
          "itemNameFormatter": ''
        }
      }
    },
    {
      "fromDatasetIndex": 1,
      "fromTransformResult": 1
    }
    ],
    "tooltip": {
      "trigger": 'item',
      "axisPointer": {
        "type": 'shadow'
    }
    },
    "grid": {
     "left": '10%',
     "right": '10%',
     "bottom": '15%',
     "top": '10%'
    },
    "yAxis": {
      "type": 'category',
     "boundaryGap": 'true',
     "nameGap": 30,
     "splitArea": {
       "show": 'false'
    },
    "splitLine": {
      "show": 'false'
    }
    },
    "xAxis": {
      "type": 'value',
      "name": '',
      "splitArea": {
      "show": 'true'
    }
     },
    "series": [
    {
      "name": 'boxplot',
      "type": 'boxplot',
      "datasetIndex": 1
    },
    {
      "name": 'outlier',
      "type": 'scatter',
      "encode": { "x": 1, "y": 0 },
      "datasetIndex": 2
    }
    ]
    };
    st_echarts(options=option,height='290px',width='100%' , key="boxplot")


if per_type_selected == '个例':

    if comparison_branchcode:

        row9_spacer1, row9_1, row9_spacer2 = st.columns((.2, 7.1, .2))
        with row9_1:
             st.subheader('Analysis per Team')
    
        row10_spacer1, row10_1, row10_spacer2, row10_2, row10_3  = st.columns((.2, 2.3, .4, 2.3, 2.3))
        if branch_selected == '总公司':
            unique_branch_code2 = filtered_df['Branch_code2'].unique()
        else:
            unique_branch_code2 = filtered_df.loc[filtered_df['Branch_code1'] == selected_branch, 'Branch_code2'].unique() 
        with row10_1:
            Branch_code2_1 = st.selectbox("选择您想要对比分析的"+ per_level_selected + '1', unique_branch_code2,key="10-1")
        if per_level_selected == '业务部':
            with row10_2:
                unique_branch_code3 = filtered_df.loc[filtered_df['Branch_code2'] == Branch_code2_1, 'Branch_code3'].unique() 
                branch_code3_selected_1 = st.selectbox("",unique_branch_code3,key="10-2")
            Branch_select1 = branch_code3_selected_1
        else:
            Branch_select1 = Branch_code2_1
        

        row14_spacer1, row14_1, row14_spacer2, row14_2, row14_spacer3  = st.columns((.2, 2.3, .4, 2.3, 2.3))
        if branch_selected == '总公司':
            unique_branch_code2 = filtered_df['Branch_code2'].unique()
        else:
            unique_branch_code2 = filtered_df.loc[filtered_df['Branch_code1'] == selected_branch, 'Branch_code2'].unique() 
        with row14_1:
            Branch_code2_2 = st.selectbox("选择您想要对比分析的"+ per_level_selected + '2', unique_branch_code2,key="14-1")
        if per_level_selected == '业务部': 
            with row14_2:
                unique_branch_code3 = filtered_df.loc[filtered_df['Branch_code2'] == Branch_code2_2, 'Branch_code3'].unique() 
                branch_code3_selected_2 = st.selectbox("",unique_branch_code3,key="14-2")
            Branch_select2 = branch_code3_selected_2
        else:
            Branch_select2 = Branch_code2_2
            
        # 对比模块
        row11_spacer1, row11_1, row11_spacer2, row11_2, row11_emoji,row11_spacer3, row11_3 ,row11_spacer4 = st.columns((0.7, 2.3, 0.1,2.3, 0.3,0.3, 3, 0.3))
        with row11_2:
            styled_text_css = f"<span style='font-size: 17px; font-weight: bold;'>{Branch_select1}</span>"
            st.markdown("")
            st.markdown(styled_text_css, unsafe_allow_html=True)
        with row11_emoji:
            st.markdown("")
            st.markdown("🆚")
        with row11_3:
            styled_text_css = f"<span style='font-size: 17px; font-weight: bold;'>{Branch_select2}</span>"
            st.markdown("")
            st.markdown(styled_text_css, unsafe_allow_html=True)
     
        row12_spacer1, row12_1, row12_spacer2, row12_2,  row12_spacer3 ,row12_3,row12_spacer4 = st.columns((0.9, 2.5, 1, 2, 1.2, 2, 0.5))
        with row12_1:
            st.markdown("👟 Observation")
            st.markdown("🏃‍♂️ Maximum")
            st.markdown("🔁 Minimum")
            st.markdown("🤹‍♂️ Mean")
            st.markdown("🤕 The 25th percentile")
            st.markdown("🚫 Median")
            st.markdown("📐 The 75th percentile")
        
        if per_level_selected == '业务部':
            Branch_code3_1 = filtered_df[(filtered_df['Branch_code3'] == Branch_select1) ]
            Branch_code3_2 = filtered_df[(filtered_df['Branch_code3'] == Branch_select2) ]
        else:
            Branch_code3_1 = filtered_df[(filtered_df['Branch_code2'] == Branch_select1) ]
            Branch_code3_2 = filtered_df[(filtered_df['Branch_code2'] == Branch_select2) ]

        with row12_2:           
            guanceshu_1 = Branch_code3_1['Branch_code3'].count()
            st.markdown(str(guanceshu_1) )
            zuidaazhi_1 = Branch_code3_1['Jxl'].max()
            st.markdown(str(zuidaazhi_1) )
            zuixiaoazhi_1 = Branch_code3_1['Jxl'].min()
            st.markdown(str(zuixiaoazhi_1) )
            junzhi_1 = Branch_code3_1['Jxl'].mean().round(2)
            st.markdown(str(junzhi_1) )   
            fenweishu25_1 = Branch_code3_1['Jxl'].quantile(0.25).round(2)
            st.markdown(str(zuixiaoazhi_1) )      
            zhongweishu_1 = Branch_code3_1['Jxl'].median() 
            st.markdown(str(zhongweishu_1) )
            fenweishu75_1 = Branch_code3_1['Jxl'].quantile(0.75).round(2) 
            st.markdown(str(fenweishu75_1) )  
        
        with row12_3:           
            guanceshu_2 = Branch_code3_2['Branch_code3'].count()
            st.markdown(str(guanceshu_2) )
            zuidaazhi_2 = Branch_code3_2['Jxl'].max()
            st.markdown(str(zuidaazhi_2) )
            zuixiaoazhi_2 = Branch_code3_2['Jxl'].min()
            st.markdown(str(zuixiaoazhi_2) )
            junzhi_2 = Branch_code3_2['Jxl'].mean().round(2)
            st.markdown(str(junzhi_2) )   
            fenweishu25_2 = Branch_code3_2['Jxl'].quantile(0.25).round(2)
            st.markdown(str(zuixiaoazhi_2) )      
            zhongweishu_2 = Branch_code3_2['Jxl'].median() 
            st.markdown(str(zhongweishu_2) )
            fenweishu75_2 = Branch_code3_2['Jxl'].quantile(0.75).round(2) 
            st.markdown(str(fenweishu75_2) )  

    else:

        row9_spacer1, row9_1, row9_spacer2 = st.columns((.2, 7.1, .2))
        with row9_1:
             st.subheader('Analysis per Team')
    
        row10_spacer1, row10_1, row10_spacer2, row10_2, row10_spacer3  = st.columns((.2, 2.3, .4, 2.3, 2.3))
    
        if branch_selected == '总公司':
            unique_branch_code2 = filtered_df['Branch_code2'].unique()
        else:
            unique_branch_code2 = filtered_df.loc[filtered_df['Branch_code1'] == selected_branch, 'Branch_code2'].unique() 
        with row10_1:
            Branch_code2 = st.selectbox("选择您想要分析的"+ per_level_selected, unique_branch_code2,key="10-1")
    
        if per_level_selected == '业务部':
            with row10_2:
                unique_branch_code3 = filtered_df.loc[filtered_df['Branch_code2'] == Branch_code2, 'Branch_code3'].unique() 
                branch_code3_selected = st.selectbox("",unique_branch_code3,key="10-2")
        else:
            branch_code3_selected = Branch_code2
    
        
        row11_spacer1, row11_1, row11_2, row11_3, row11_4, row11_spacer2  = st.columns((0.5, 3, 4, 1, 2, 0.5))
        with row11_2:
            styled_text_css = f"<span style='font-size: 17px; font-weight: bold;'>{branch_code3_selected}</span>"
            st.markdown("")
            st.markdown(styled_text_css, unsafe_allow_html=True)
     
        row12_spacer1, row12_1, row12_spacer2, row12_2,  row12_spacer3  = st.columns((0.7, 2, 0.6, 4, 0.5))
        with row12_1:
            st.markdown("👟 Observation")
            st.markdown("🏃‍♂️ Maximum")
            st.markdown("🔁 Minimum")
            st.markdown("🤹‍♂️ Mean")
            st.markdown("🤕 The 25th percentile")
            st.markdown("🚫 Median")
            st.markdown("📐 The 75th percentile")


        if per_level_selected == '业务部':
            Branch_code3_1 = filtered_df[(filtered_df['Branch_code3'] == branch_code3_selected) ]
        else:
            Branch_code3_1 = filtered_df[(filtered_df['Branch_code2'] == branch_code3_selected) ]
    
        with row12_2:
            guanceshu_1 = Branch_code3_1['Branch_code3'].count()
            st.markdown(str(guanceshu_1) )
            zuidaazhi_1 = Branch_code3_1['Jxl'].max()
            st.markdown(str(zuidaazhi_1) )
            zuixiaoazhi_1 = Branch_code3_1['Jxl'].min()
            st.markdown(str(zuixiaoazhi_1) )
            junzhi_1 = Branch_code3_1['Jxl'].mean().round(2)
            st.markdown(str(junzhi_1) )   
            fenweishu25_1 = Branch_code3_1['Jxl'].quantile(0.25).round(2)
            st.markdown(str(zuixiaoazhi_1) )      
            zhongweishu_1 = Branch_code3_1['Jxl'].median() 
            st.markdown(str(zhongweishu_1) )
            fenweishu75_1 = Branch_code3_1['Jxl'].quantile(0.75).round(2) 
            st.markdown(str(fenweishu75_1) )   
