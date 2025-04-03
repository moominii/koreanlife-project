# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 07:37:42 2025

@author: Admin
종교 / 지역
"""

### 패키지 설치 및 로드
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

# 맑은 고딕 폰트 설정
plt.rcParams.update({'font.family' : 'Malgun Gothic'})

# 데이터 불러오기
raw_welfare = pd.read_spss('./data/Koweps_hpwc14_2019_beta2.sav')

# 복사본
welfare = raw_welfare.copy()

# 성별, 태어난 연도, 혼인 상태, 종교, 월급, 직업 코드, 지역 코드
# 변수명 변경
welfare = welfare.rename(columns = {'h14_g3'     : 'sex',            #  성별
                                    'h14_g4'     : 'birth',          #  태어난 연도
                                    'h14_g10'    : 'marriage_type',  #  혼인 상태
                                    'h14_g11'    : 'religion',       #  종교 
                                    'p1402_8aq1' : 'income',         #  월급 
                                    'h14_eco9'   : 'code_job',       #  직업 코드
                                    'h14_reg7'   : 'code_region'})   #  지역 코드 

# 성별 항목 이름 부여
welfare['sex'] = np.where(welfare['sex'] == 1, 'male', 'female')

# 나이 파생변수 
welfare = welfare.assign(age = 2019 - welfare['birth'] + 1)


# 연령대 변수 
welfare = welfare.assign(ageg = np.where(welfare['age'] <  30, 'young',
                                np.where(welfare['age'] <= 59, 'middle', 
                                         'old')))

# 전처리하기
list_job = pd.read_excel('./data/Koweps_Codebook_2019.xlsx',
                         sheet_name = '직종코드')

# welfare에 list_job 결합
welfare = welfare.merge(list_job, how = 'left', on = 'code_job')


"""
종교 유무에 따른 이혼율 - 종교가 있으면 이혼을 덜 할까?
"""
### 종교 변수 검토 및 전처리
welfare['religion'].dtypes  # 변수 타입 출력 dtype('float64')

welfare['religion'].value_counts()  # 빈도 구하기
'''
religion
2.0    7815
1.0    6603
Name: count, dtype: int64
'''
# 종교 유무 이름 부여
welfare['religion'] = np.where(welfare['religion'] == 1, 'yes', 'no')

welfare['religion'].value_counts()
'''
religion
no     7815
yes    6603
Name: count, dtype: int64
'''
sns.countplot(data = welfare, x = 'religion')
plt.show()

##  혼인 상태 변수 검토 및 전처리
welfare['marriage_type'].dtypes  # 변수 타입 출력  dtype('float64')

welfare['marriage_type'].value_counts()  # 빈도 구하기
'''
marriage_type
1.0    7190   유배우 <=
5.0    2357   미혼
0.0    2121   비해당
2.0    1954   사별
3.0     689   이혼  <=
4.0      78   별거
6.0      29   기타
Name: count, dtype: int64
'''
# 이혼 여부 변수
welfare['marriage'] = np.where(welfare['marriage_type'] == 1, 'marriage',
                      np.where(welfare['marriage_type'] == 3,  'divorce',
                               'etc'))
'''
0             etc
1             etc
2         divorce
3        marriage
4        marriage
  
14413    marriage
14414         etc
14415         etc
14416         etc
14417         etc
Name: marriage, Length: 14418, dtype: object
'''
## 이혼 여부별 빈도
# marriage별 분리
# marriage별 빈도 구하기
n_divorce = welfare.groupby('marriage', as_index = False) \
                   .agg(n = ('marriage', 'count'))
'''
   marriage     n
0   divorce   689
1       etc  6539
2  marriage  7190
'''
sns.barplot(data = n_divorce, x = 'marriage', y = 'n')
plt.show()

## 종교 유무에 따른 이혼율 분석
# 종교 유무에 따른 이혼율표 
# etc 제외
# religion별 분리
# marriage 추출
# 비율 구하기
rel_div = welfare.query('marriage != "etc"') \
                 .groupby('religion', as_index = False)['marriage'] \
                 .value_counts(normalize=True) # 빈도를 이용하여 비율 구하기
'''
  religion  marriage  proportion
0       no  marriage    0.905045
1       no   divorce    0.094955
2      yes  marriage    0.920469
3      yes   divorce    0.079531
'''
# divorce 추출
# 백분율로 바꾸기
# 반올림
rel_div = rel_div.query('marriage == "divorce"') \
                 .assign(proportion = rel_div['proportion'] * 100) \
                 .round(1)
'''
  religion marriage  proportion
1       no  divorce         9.5
3      yes  divorce         8.0
'''
sns.barplot(data = rel_div, x = 'religion', y = 'proportion')
plt.show()
'''
종교 있는 사람의 이혼율이 낮다...
'''
"""
연령대 및 종교 유무에 따른 이혼율 분석
"""
## 연령대별 이혼율표 
# etc 제외
# ageg별 분리
# marriage 추출
# 비율 구하기
age_div = welfare.query('marriage != "etc"') \
                 .groupby('ageg', as_index = False)['marriage'] \
                 .value_counts(normalize = True)
'''
     ageg  marriage  proportion
0  middle  marriage    0.910302
1  middle   divorce    0.089698
2     old  marriage    0.914220
3     old   divorce    0.085780
4   young  marriage    0.950000
5   young   divorce    0.050000
''' 
# 연령대별 이혼율 시각화
# 초년층 제외, 이혼 추출
# 백분율로 바꾸기
# 반올림
age_div = age_div.query('ageg != "young" & marriage == "divorce"') \
                 .assign(proportion = age_div['proportion'] * 100) \
                 .round(1)

sns.barplot(data = age_div, x = 'ageg', y = 'proportion')
plt.show()

## 연령대 및 종교 유무에 따른 이혼율표
# etc 제외, 초년층 제외
# marriage 추출
# 비율 구하기
age_rel_div = welfare.query('marriage != "etc" & ageg != "young"') \
                     .groupby(['ageg', 'religion'], as_index = False) \
                      ['marriage'] \
                     .value_counts(normalize = True)
'''
     ageg religion  marriage  proportion
0  middle       no  marriage    0.904953
1  middle       no   divorce    0.095047
2  middle      yes  marriage    0.917520
3  middle      yes   divorce    0.082480
4     old       no  marriage    0.904382
5     old       no   divorce    0.095618
6     old      yes  marriage    0.922222
7     old      yes   divorce    0.077778
'''
## 시각화
# divorce 추출
# 백분율로 바꾸기
# 반올림
age_rel_div = age_rel_div.query('marriage == "divorce"') \
                        .assign(proportion = age_rel_div['proportion'] * 100) \
                        .round(1)
'''
     ageg religion marriage  proportion
1  middle       no  divorce         9.5
3  middle      yes  divorce         8.2
5     old       no  divorce         9.6
7     old      yes  divorce         7.8
'''
sns.barplot(data = age_rel_div, 
            x = 'ageg', y = 'proportion', 
            hue = 'religion')
plt.show()



           
"""
지역별 연령대 비율 - 어느 지역에 노년층이 많을까?
"""
## 지역 변수 검토 및 전처리
welfare['code_region'].dtypes  # 변수 타입 출력  dtype('float64')

welfare['code_region'].value_counts()
'''
code_region
2.0    3246
7.0    2466
3.0    2448
1.0    2002
4.0    1728
5.0    1391
6.0    1137
Name: count, dtype: int64
'''

# 지역명 변수 추가
'''
1. 서울          2. 수도권(인천/경기)    3. 부산/경남/울산   4.대구/경북   
5. 대전/충남   6. 강원/충북               7.광주/전남/전북/제주도
'''
list_region = pd.DataFrame({'code_region' : [1, 2, 3, 4, 5, 6, 7],
                            'region'      : ['서울',
                                             '수도권(인천/경기)',
                                             '부산/경남/울산',
                                             '대구/경북',
                                             '대전/충남',
                                             '강원/충북',
                                             '광주/전남/전북/제주도']})
'''
   code_region        region
0            1            서울
1            2    수도권(인천/경기)
2            3      부산/경남/울산
3            4         대구/경북
4            5         대전/충남
5            6         강원/충북
6            7  광주/전남/전북/제주도
'''
# 지역명 변수 추가
welfare = welfare.merge(list_region, how = 'left', on = 'code_region')
welfare[['code_region', 'region']].head()
'''
   code_region region
0          1.0     서울
1          1.0     서울
2          1.0     서울
3          1.0     서울
4          1.0     서울
'''

## 지역별 연령대 비율
# 지역별 연령대 비율표
# region별 분리
# ageg 추출
# 비율 구하기
region_ageg = welfare.groupby('region', as_index = False)['ageg'] \
                     .value_counts(normalize = True)
'''
          region    ageg  proportion
0          강원/충북     old    0.459103
1          강원/충북  middle    0.308707
2          강원/충북   young    0.232190
3   광주/전남/전북/제주도     old    0.449311
4   광주/전남/전북/제주도  middle    0.317924
'''
region_ageg = region_ageg.assign(proportion = region_ageg['proportion'] * 100) \
                         .round(1)
'''
          region            ageg    proportion
0          강원/충북        old        45.9
1          강원/충북        middle        30.9
2          강원/충북         young        23.2
3   광주/전남/전북/제주도     old        44.9
4   광주/전남/전북/제주도   middle        31.8
'''
sns.barplot(data = region_ageg, 
            y = 'region', x = 'proportion', 
            hue = 'ageg')
plt.show()




# 시각화 (막대, 누적)
'''
          ageg
          region            old    middle young
0          강원/충북        45.9    30.99  23.2

3   광주/전남/전북/제주도     old        44.9
4   광주/전남/전북/제주도   middle        31.8
'''
"""
피벗 : 행과 열을 회전하여 표의 구성을 변경하는 작업.
       누적그래프 형태로 시각화할 때 사용...
1. 지역, 연령대, 비율 <= 추출
    region_ageg [['region', 'ageg', 'proportion']]
    
2. DataFrame.pivot() 
2-1. 지역을 기준으로 : index=지역
2-2. 연령대별로 컬럼을 구성 : columns = 연령대
2-3. 각 항목의 값을 비율로 채우기 : values=비율 
"""
pivot_df = region_ageg[['region', 'ageg', 'proportion']] \
                        .pivot(index='region',
                               columns = 'ageg',
                               values  = 'proportion')
'''
ageg                  middle   old  young
region                           
강원/충북               30.9  45.9   23.2
광주/전남/전북/제주도    31.8  44.9   23.3
대구/경북               29.6  50.4   20.0
대전/충남               33.6  41.3   25.0
부산/경남/울산           33.4  43.8   22.9
서울                    38.5  37.6   23.9
수도권(인천/경기)        38.8  32.5   28.7
'''
pivot_df.plot.barh(stacked = True)
plt.show()

reorder_df = pivot_df.sort_values('old')[['young', 'middle', 'old']]
'''
ageg                 young  middle   old
region                           
수도권(인천/경기)     28.7    38.8  32.5
'''
reorder_df.plot.barh(stacked = True)
plt.show()









