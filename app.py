import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# 앱 제목 및 설정
st.set_page_config(page_title="나라장터 입찰공고 요약", layout="wide")
st.title("🔍 최근 1주일 입찰공고 자동화 리스트")

# 사이드바 설정 (API 키 입력 등)
service_key = st.sidebar.text_input("61203561a5f6b1757e496997889aa776c9484657a36d4aaea2de18b25192393b", type="password")

if st.button("공고 불러오기"):
    if not service_key:
        st.error("61203561a5f6b1757e496997889aa776c9484657a36d4aaea2de18b25192393b")
    else:
        # 키워드 설정
        keywords = ['뉴미디어', '홍보', '온라인 홍보', '서포터즈', '서울창업허브', '농촌관광', '관광', '여행', '브랜딩']
        
        # 날짜 설정
        end_date = datetime.now().strftime('%Y%m%d%H%M')
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y%m%d0000')

        with st.spinner('데이터를 가져오는 중...'):
            url = "http://apis.data.go.kr/1230000/BidPublicInfoService05/getBidPblancListInfoServcPPSSrch01"
            params = {
                'serviceKey': service_key,
                'numOfRows': '1000',
                'inqryDiv': '1',
                'inqryBgnDt': start_date,
                'inqryEndDt': end_date,
                'type': 'json'
            }
            
            res = requests.get(url, params=params)
            data = res.json().get('response', {}).get('body', {}).get('items', [])
            
            # 데이터 필터링
            filtered = []
            for item in data:
                title = item.get('bidNtceNm', '')
                if any(k in title for k in keywords):
                    filtered.append({
                        "공고명": title,
                        "공고기관": item.get('ntceInsttNm'),
                        "공고일시": item.get('bidNtceDt'),
                        "링크": item.get('bidNtceDtlUrl')
                    })
            
            if filtered:
                df = pd.DataFrame(filtered)
                # 표 형태로 출력
                st.write(f"총 {len(df)}건의 공고가 발견되었습니다.")
                st.dataframe(df, use_container_width=True)
                
                # 엑셀 다운로드 버튼
                csv = df.to_csv(index=False).encode('utf-8-sig')
                st.download_button("결과 다운로드 (CSV)", csv, "bids.csv", "text/csv")
            else:
                st.warning("조건에 맞는 공고가 없습니다.")
