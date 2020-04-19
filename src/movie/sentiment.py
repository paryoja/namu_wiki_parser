import pandas as pd
import urllib.request
import matplotlib.pyplot as plt
import re
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

urllib.request.urlretrieve(
    "https://raw.githubusercontent.com/e9t/nsmc/master/ratings_train.txt",
    filename="ratings_train.txt",
)
urllib.request.urlretrieve(
    "https://raw.githubusercontent.com/e9t/nsmc/master/ratings_test.txt",
    filename="ratings_test.txt",
)
train_data = pd.read_table("ratings_train.txt")
test_data = pd.read_table("ratings_test.txt")
print("훈련용 리뷰 개수 :", len(train_data))  # 훈련용 리뷰 개수 출력
print(train_data[:5])  # 상위 5개 출력
print("테스트용 리뷰 개수 :", len(test_data))  # 테스트용 리뷰 개수 출력
print(train_data["document"].nunique(), train_data["label"].nunique())

train_data.drop_duplicates(
    subset=["document"], inplace=True
)  # document 열에서 중복인 내용이 있다면 중복 제거

print("총 샘플의 수 :", len(train_data))
print(train_data.groupby("label").size().reset_index(name="count"))
print(train_data.isnull().values.any())
print(train_data.isnull().sum())
print(train_data.loc[train_data.document.isnull()])
train_data = train_data.dropna(how="any")  # Null 값이 존재하는 행 제거
print(train_data.isnull().values.any())  # Null 값이 존재하는지 확인
