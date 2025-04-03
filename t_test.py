# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 08:06:17 2025

@author: Admin
t_test.py

통계 분석 기법을 이용한 가설 검정
mpg.csv
"""
### compact 자동차와 suv 자동차의 도시 연비 <= t 검정
import pandas as pd
mpg = pd.read_csv('./data/mpg.csv')

## 기술 통계 분석
# compact, suv 추출
# category별 분리
# 빈도 구하기
# cty 평균 구하기
mpg.query('category in ["compact", "suv"]') \
    .groupby('category', as_index = False)  \
    .agg(n = ('category', 'count'),
         mean = ('cty', 'mean'))
'''
  category   n      mean
0  compact  47  20.12766
1      suv  62  13.50000
'''
## t 검정
# mpg에서 category가 'compact' => cty
# mpg에서 category가 'suv'     => cty
compact = mpg.query('category == "compact"')['cty']
suv = mpg.query('category == "suv"')['cty']

# t-test : stats.ttest_ind(compact, suv, equal_var = True)
# equal_var = True : 집단(변수)간의 분산 같다
from scipy import stats

stats.ttest_ind(compact, suv, equal_var = True)
'''
TtestResult(statistic=11.917282584324107, 
            pvalue=2.3909550904711282e-21, 
            df=107.0)

pvalue : 유의확률
e-21   : 2.3909550904711282에 0이 21개가 있는 값
       : 0.0000000000022

일반적으로 유의확률 5% 판단 기준
pvalue 0.05 미만 , 집단(변수)간 차이가 통계적으로 유의하다 
compact와 suv간 평균 도시연비 차이가 통계적으로 유의하다
'''
### 일반 휘발유와 고급 휘발유의 도시 연비 <= t 검정
## 기술 통계 분석
# r, p 추출하기
# fl별 분리
# 빈도 구하기
# cty 평균 구하기
mpg.query('fl in ["r", "p"]') \
    .groupby('fl', as_index = False) \
    .agg(n    = ('category', 'count'),
         mean = ('cty', 'mean'))
'''
  fl    n       mean
0  p   52  17.365385
1  r  168  16.738095
'''
regular = mpg.query('fl == "r"')['cty']
premium = mpg.query('fl == "p"')['cty']

stats.ttest_ind(regular, premium, equal_var = True)
'''
TtestResult(statistic=-1.066182514588919, 
            pvalue=0.28752051088667036, 
            df=218.0)
pvalue=0.28752051088667036 => 28%
=> 실제로는 차이가 없는데
   우연에 의해 이런 정도의 차이가 관찰될 확률이 28.75% 라는 의미!
   
   일반 휘발유와 고급 휘발유를 사용하는 도시 연비차이가 
   통계적으로 유의하지 않다
   
   고급 휘발유 도시 연비 평균이 0.6정도 높지만
   이런 정도의 차이는 우연히 발생했을 가능성이 크다
'''

"""
상관분석 - 두 변수의 관계 분석하기

상관분석을 통해 도출된 상관계수 값으로 판단 가능(관련성 여부)

상관계수 : 0~1 사이의 값
          1에 가까울수록 관련성이 크다
          양수이면 정비례
          음수면 반비레
"""
## 실업자 수(unemploy)와 개인 소비 지출(pce)의 상관관계 : economics.csv
economics = pd.read_csv('./data/economics.csv')

# 상관계수 : corr()
economics[['unemploy', 'pce']].corr()
'''
상관행렬
          unemploy       pce
unemploy  1.000000  0.614518
pce       0.614518  1.000000
'''

# 유의확률 구하기 : stats.pearsonr(   ,   )
stats.pearsonr(economics['unemploy'], economics['pce'])
'''
PearsonRResult(statistic=0.6145176141932082, <= 상관계수
               pvalue=6.773527303289964e-61) <= 유의확률
'''

### 상관행렬 히트맵 : mtcars.csv
mtcars = pd.read_csv('./data/mtcars.csv')
mtcars.head()
'''
    mpg  cyl   disp   hp  drat     wt   qsec  vs  am  gear  carb
0  21.0    6  160.0  110  3.90  2.620  16.46   0   1     4     4
1  21.0    6  160.0  110  3.90  2.875  17.02   0   1     4     4
2  22.8    4  108.0   93  3.85  2.320  18.61   1   1     4     1
3  21.4    6  258.0  110  3.08  3.215  19.44   1   0     3     1
4  18.7    8  360.0  175  3.15  3.440  17.02   0   0     3     2
'''
# 상관행렬 만들기
car_cor = mtcars.corr() 

# 소수점 둘째 자리까지 반올림
car_cor = round(car_cor, 2)

import matplotlib.pyplot as plt
import seaborn as sns

# 해상도 설정 , 가로 세로 크기 설정
plt.rcParams.update({'figure.dpi' : '120',  
                     'figure.figsize': [7.5, 5.5]}) 

# 히트맵: sns.heatmap(상관행열, 상관계수 표시, 컬러맵)
# 상관계수 표시 : annot = True
# 컬러맵 : cmap = 'RdBu'
sns.heatmap(car_cor, annot = True, cmap = 'RdBu')
# Rd <= Red(음수) / Bu <=Blue(양수)
plt.show()

##  대각 행렬 제거 
# mask 만들기
import numpy as np
mask = np.zeros_like(car_cor)

# 오른쪽 위 대각 행렬을 1로 바꾸기
mask[np.triu_indices_from(mask)] = 1

# 히트맵에 mask 적용 : heatmap(mask = mask)
sns.heatmap(data = car_cor,
            annot = True,
            cmap = 'RdBu',
            mask = mask) 
plt.show()

## 빈 행과 열 제거하기
# mask 첫 번째 행, 마지막 열 제거
# 상관행렬 첫 번째 행, 마지막 열 제거
mask_new = mask[1:, :-1] 
cor_new = car_cor.iloc[1:, :-1]

sns.heatmap(data = cor_new,
            annot = True,
            cmap = 'RdBu', 
            mask = mask_new)
plt.show()








