import pandas as pd

item_name = "KODEX 200"
url = "http://finance.naver.com/item/sise_day.nhn?code=069500"


# 일자 데이터를 담을 df라는 DataFrame 정의
df = pd.DataFrame()

# 1페이지에서 91페이지의 데이터만 가져오기
for page in range(1, 91):
    pg_url = '{url}&page={page}'.format(url=url, page=page)
    df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)

# df.dropna()를 이용해 결측값 있는 행 제거
df = df.dropna()

# 상위 1000개 데이터 확인하기
df.head(1000)

# 한글로 된 컬럼명을 영어로 바꿔줌
df = df.rename(columns= {'날짜': 'date', '종가': 'close', '전일비': 'diff', 
                         '시가': 'open', '고가': 'high', '저가': 'low', '거래량': 'volume'})

# 데이터의 타입을 int형으로 바꿔줌
df[['close', 'diff', 'open', 'high', 'low', 'volume']] \
    = df[['close', 'diff', 'open', 'high', 'low', 'volume']].astype(int)

# 컬럼명 'date'의 타입을 date로 바꿔줌
df['date'] = pd.to_datetime(df['date'])

# 일자(date)를 기준으로 오름차순 정렬
df = df.sort_values(by=['date'], ascending=True)

# 상위 1000개 데이터 확인
df.head(1000)





url = "http://finance.naver.com/item/sise_day.nhn?code=228790"


# 일자 데이터를 담을 df라는 DataFrame 정의
df_2 = pd.DataFrame()

# 1페이지에서 91페이지의 데이터만 가져오기
for page in range(1, 91):
    pg_url = '{url}&page={page}'.format(url=url, page=page)
    df_2 = df_2.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)

# df.dropna()를 이용해 결측값 있는 행 제거
df_2 = df_2.dropna()

# 상위 1000개 데이터 확인하기
df_2.head(1000)

# 한글로 된 컬럼명을 영어로 바꿔줌
df_2 = df_2.rename(columns= {'날짜': 'date', '종가': 'close', '전일비': 'diff', 
                         '시가': 'open', '고가': 'high', '저가': 'low', '거래량': 'volume'})

# 데이터의 타입을 int형으로 바꿔줌
df_2[['close', 'diff', 'open', 'high', 'low', 'volume']] \
    = df_2[['close', 'diff', 'open', 'high', 'low', 'volume']].astype(int)

# 컬럼명 'date'의 타입을 date로 바꿔줌
df_2['date'] = pd.to_datetime(df_2['date'])

# 일자(date)를 기준으로 오름차순 정렬
df_2 = df_2.sort_values(by=['date'], ascending=True)

# 상위 1000개 데이터 확인
df_2.head(1000)










max_kodex200 = df['close'].max()
max_2        = df_2['close'].max()
ratio = max_kodex200 / max_2
df['close'] = df['close'] / ratio









# 필요한 모듈 import 하기
import plotly.offline as offline
import plotly.graph_objs as go


trace = go.Scatter( x=df.date, y=df.close, name=item_name)
trace_2 = go.Scatter( x=df_2.date, y=df_2.close, name="화장품")
data = [trace, trace_2]

layout = dict(
    title='{}의 종가(close) Time Series'.format(item_name),
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label='1m',
                     step='month',
                     stepmode='backward'),
                dict(count=3,
                     label='3m',
                     step='month',
                     stepmode='backward'),
                dict(count=6,
                     label='6m',
                     step='month',
                     stepmode='backward'),
                dict(step='all')
                ])
            ),
        rangeslider=dict(),
        type='date'
        )
    )
fig = go.Figure(data=data, layout=layout)
offline.plot(fig)
