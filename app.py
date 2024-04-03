import streamlit as st

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd


def movie_crawling(movie_name):
    driver = webdriver.Chrome()
    driver.maximize_window()  # 브라우저 창 최대화

    url = f'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=영화{movie_name}관람평'
    driver.get(url)
    
    reply_quantity = 300

    rating = []
    comment = []
    date = []
    positive = []
    negative = []

    # 리뷰 박스 스크롤
    for _ in range(reply_quantity):    
        scroll = driver.find_element(By.XPATH, '//*[@id="main_pack"]/div[2]/div[2]/div/div/div[4]/div[4]')  # 스크롤할 요소 선택
        driver.execute_script("arguments[0].scrollBy(0, 2000)", scroll)                                     # 스크롤

    for i in range(1, reply_quantity + 1):
        rating.append(driver.find_elements(By.XPATH, f'//*[@id="main_pack"]/div[2]/div[2]/div/div/div[4]/div[4]/ul/li[{i}]/div[1]/div/div[2]')[0].text)
        comment.append(driver.find_elements(By.XPATH, f'//*[@id="main_pack"]/div[2]/div[2]/div/div/div[4]/div[4]/ul/li[{i}]/div[2]/div/span[2]')[0].text)
        date.append(driver.find_elements(By.XPATH, f'//*[@id="main_pack"]/div[2]/div[2]/div/div/div[4]/div[4]/ul/li[{i}]/dl/dd[2]')[0].text)
        positive.append(driver.find_elements(By.XPATH, f'//*[@id="main_pack"]/div[2]/div[2]/div/div/div[4]/div[4]/ul/li[{i}]/div[3]/button[1]/span')[0].text)
        negative.append(driver.find_elements(By.XPATH, f'//*[@id="main_pack"]/div[2]/div[2]/div/div/div[4]/div[4]/ul/li[{i}]/div[3]/button[2]/span')[0].text)

    # 웹 드라이버 종료
    driver.quit()
    
    df = pd.DataFrame({'rating': rating,
                       'comment': comment,
                       'date': date,
                       'positive': positive,
                       'negative': negative})
    
    # rating 전처리
    def star_split(rating):
        return rating.split()[-1]
    
    df['rating'] = df['rating'].apply(star_split)
    df = df[~df['comment'].str.contains('스포일러')]
    
    return df


def main():
    font_path = 'C:\Windows\Fonts\HMFMPYUN.ttf'

    st.title('영화 리뷰 워드클라우드')
    
    movie_name = st.text_input('영화명을 입력해주세요')
    
    if movie_name:
        st.write(f'[{movie_name}] 의 리뷰를 수집 중입니다.')
        df = movie_crawling(movie_name)
        # st.dataframe(df)

        # 데이터프레임에서 텍스트 추출
        text = ' '.join(df['comment'])

        # 워드클라우드 생성
        wordcloud = WordCloud(font_path=font_path,
                            background_color="white",
                            width=1000,
                            height=1000,
                            max_words=100,
                            max_font_size=300).generate(text)

        # 워드클라우드 표시
        st.image(wordcloud.to_array())

if __name__ == '__main__':
    main()
