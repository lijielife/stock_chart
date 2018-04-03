import pandas as pd

import plotly.offline as offline
import plotly.graph_objs as go


def get_stock_list():
    stock_list = {
            "KODEX 200"                : "069500",
            "KINDEX 중국본토 CSI300"   : "168580",
            "TIGER 미국다우존스30"     : "245340",
            "TIGER 유로스탁스50"       : "195930",
            "TIGER 일본TOPIX"          : "195920",
            "TIGER 미국S&P500선물"     : "143850",
            "KINDEX 인도네시아MSCI"    : "256440",
            "TIGER 라틴35"             : "105010", 
            }
    return stock_list


''' 

            "KODEX 선진국MSCI World"   : "251350",
            "KINDEX 베트남VN30"        : "245710",
            "KINDEX S&P아시아TOP50"    : "277540",
            "TIGER 미국나스닥100"      : "133690",
            "TIGER 인도니프티50레버리지" : "236350",
            "TIGER 대만TAIEX선물"      : "253990",
            "TIGER 미국나스닥바이오"   : "203780",
            "KINDEX 필리핀MSCI"        : "261920",



            "KODEX 은행"               : "091170",
            "KODEX 증권"               : "102970",
            "TIGER 200 헬스케어"       : "227540", 
            "TIGER 코스피중형주"       : "277650",
            "TIGER 화장품"             : "228790",
            "KODEX 경기소비재"         : "266390",
            "KODEX 에너지화학"         : "117460",
            "TIGER 200에너지화학레버리지" : "243890",
            "KODEX 반도체"             : "091160",
            "TIGER 200 생활소비재"     : "227560",
            "TIGER 200 IT"             : "139260",
            "TIGER 200IT레버리지"      : "243880",
            "KODEX 모멘텀Plus"         : "244620",
            "KODEX IT소프트웨어"       : "266360",
            "KODEX 퀄리티Plus"         : "244660",
            "TIGER 배당성장"           : "211560",
            "KODEX 운송"               : "140710",
            "ARIRANG 고배당주"         : "161510",
            "TIGER 베타플러스"         : "170350",
            "KINDEX 스마트밸류"        : "272230",
            "KODEX 건설"               : "117700",
            "TIGER 여행레저"           : "228800",
            "TIGER 가격조정"           : "217790",
            "TIGER 모멘텀"             : "147970",
            "KODEX 바이오"             : "244580",
            "KOSEF 저PBR가중"          : "260270",
            "KBSTAR 수출주"            : "140570", 

            "TIGER 중국소비테마"       : "150460",
            "KODEX 자동차"             : "091180",
            "TIGER 200 중공업"         : "139230",
            "KODEX 기계장비"           : "102960",
            "KODEX 철강"               : "117680",
            "TIGER 경기방어"           : "139280",
            "KODEX 보험"               : "140700",
            "KINDEX 한류"              : "226380",
'''

''' 
'''




def get_stock_price(stock_list, stock_name):
    print("name: " + stock_name)
    print("code: " + stock_list[stock_name])

    url = "http://finance.naver.com/item/sise_day.nhn?code=" + stock_list[stock_name]
    print("url: " + url)

    # 일자 데이터를 담을 df라는 DataFrame 정의
    df = pd.DataFrame()

    # 1 page가 10일 분량의 데이터를 가지고 있다.
    # 1페이지에서 91페이지의 데이터만 가져오기
    for page in range(1, 150):
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
    ## df.head(1000)

    global max_price_kodex200
    
    # TODO 
    # Maximum, Minimum, Current value의 Ratio를 구하고 화면으로 출력한다.
    #  > Maximum value가 minimum value의 몇 배인지.
    #  > Current value가 Maximum value와 Minimum value의 몇 % 수준인지.
    if stock_list[stock_name] == "069500":
        max_price_kodex200 = df['close'].max()
        print("** KODEX 200 최고값: %s" % max_price_kodex200)
    else:
        this_max = df['close'].max()
        print("%s 최고값: %s" % (stock_list[stock_name], this_max))
        ratio = max_price_kodex200 / this_max
        df['close'] = df['close'] * ratio

    return df



def make_chart(chart_data, stock_name, price_df):
    print("make_chart")

    trace = go.Scatter(x=price_df.date, y=price_df.close, name=stock_name)
    chart_data.append(trace)
    
    return chart_data




my_stock_list = get_stock_list()

chart_data = []
for stock_name in my_stock_list.keys():
    price_df = get_stock_price(my_stock_list, stock_name)
    chart_data = make_chart(chart_data, stock_name, price_df)


layout = dict(
    title='{}의 종가(close) Time Series'.format(stock_name),
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
                dict(count=12,
                     label='12m',
                     step='month',
                     stepmode='backward'), 
                dict(count=24,
                     label='24m',
                     step='month',
                     stepmode='backward'), 
                dict(count=36,
                     label='36m',
                     step='month',
                     stepmode='backward'), 
                dict(step='all')
                ])
            ),
        rangeslider=dict(),
        type='date'
        )
    )
    
fig = go.Figure(data=chart_data, layout=layout)
offline.plot(fig)
