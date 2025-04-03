# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 12:12:49 2025

@author: Admin
인터랙티브 시각화 : html 파일로 저장 => Web browser 로 실행
"""
import pandas as pd
mpg = pd.read_csv('./data/mpg.csv')

import plotly.express as px

# 산점도 : px.scatter(data_frame = , x = '', y = '', color = '')
px.scatter(data_frame = mpg,
           x = 'cty',  y = 'hwy',
           color = 'drv')

import matplotlib.pyplot as plt
# html로 저장
fig.write_html('scatter_plot.html')














