# visual-analytics-system


# 교통정체예측시스템

## 모델
- convlstm_highway.py
## 결과
- check.py

## 사용 데이터

- 서울시 교통정보시스템 속도 데이터

![Untitled](https://user-images.githubusercontent.com/81469045/147448981-26daf304-fffe-43b6-b31a-e689bc577419.png)


- 고속도로 공공데이터 포털 VDS 데이터

![Untitled 1](https://user-images.githubusercontent.com/81469045/147448915-b0c7e501-c517-4c20-89bf-24a50c81ed8f.png)


## 데이터를 Heatmap으로 변환

![Untitled 2](https://user-images.githubusercontent.com/81469045/147449003-a5adc86f-e074-4676-b266-88067f3fb592.png)

- 주어진 데이터를 시각화 하여 Heatmap으로 만들었다.
- 속도가 낮은 부분은 검은색으로 표시된다.
- 그러므로 Jam의 형태를 파악할 수 있다.

## ConvLSTM

### 내부 구조

![Untitled 3](https://user-images.githubusercontent.com/81469045/147449021-cf92d258-36a4-44f9-b3e3-9268bddca62c.png)
![Untitled 4](https://user-images.githubusercontent.com/81469045/147449047-97d95525-78c4-4a01-9280-8936267f0c0b.png)


## 데이터 흐름

![Untitled 5](https://user-images.githubusercontent.com/81469045/147449059-ee9f2a14-60df-4f41-86e2-9af39db56fe1.png)


## 기능
<img width="487" alt="Untitled 6" src="https://user-images.githubusercontent.com/81469045/147449073-e22f2e1d-075a-4072-abff-091f9b45241e.png">

## 예측 결과
![Untitled 7](https://user-images.githubusercontent.com/81469045/147449087-0c3b517f-72f1-4a33-acd7-0c4b236ecbdb.png)
![Untitled 8](https://user-images.githubusercontent.com/81469045/147449090-181ef440-b90c-47d3-8b5b-ee57a3900ef0.png)
