import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

class UpClassPredict:
    UpClassPredictModel = LogisticRegression()

    def __init__(self, data) -> None:
        self.TrainUpClassPredict(data)

    def TrainUpClassPredict(self, Data) -> None:
        X = Data['GPA'].to_numpy().reshape(-1,1)
        y = Data['REG-MC4AI'].apply(lambda x: 1 if x == 'Y' else 0)
        X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.3, random_state=10)
        self.UpClassPredictModel.fit(X_train,y_train)

    def PredictUpClass(self, pData):
        pData = pData.loc['GPA'].reshape(-1,1)
        return self.UpClassPredictModel.predict(pData)[0]
    
class FinalScorePredict:
    FinalPredictModel = LinearRegression()

    def __init__(self, data) -> None:
        self.TrainFinalPredict(data)

    def TrainFinalPredict(self, Data) -> None:
        X = np.append(Data.iloc[:, 4:13]
                            .drop(labels = 'S6', axis = 1 if isinstance(Data, pd.DataFrame) else 0)
                            .fillna(0)
                            .apply(np.sum, axis = 1)
                            .to_numpy()
                            .reshape(-1,1),
                        Data['S6'].fillna(0).to_numpy().reshape(-1,1), axis = 1)
        y = Data['S10'].fillna(0)
        X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.3, random_state=10)
        self.FinalPredictModel.fit(X_train,y_train)

    def PredictFinal(self, pData):
        pData = np.append(pData.iloc[4:13]
                         .drop(labels = 'S6')
                         .fillna(0)
                         .sum()
                         .reshape(-1,1),
                      pData.loc['S6'].reshape(-1,1), axis = 1)
        return self.FinalPredictModel.predict(pData).round(1)[0]
    
class GPAPredict:
    GPAPredictModel = LinearRegression()

    def __init__(self,Data) -> None:
        self.TrainGPAPredict(Data)
    
    def TrainGPAPredict(self, Data) -> None:
        X = Data[['S6','S10','BONUS']].fillna(0).to_numpy()
        y = Data['GPA'].fillna(0)
        X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.3, random_state=10)
        self.GPAPredictModel.fit(X=X_train,y=y_train)

    def PredictGPA(self, pData):
        pData = pData[['S6','S10','BONUS']].fillna(0).to_numpy().reshape(1,-1)
        return self.GPAPredictModel.predict(pData).round(1)[0]
    

class ComparePredictReal:

    FinalModel = None
    UpClassModel = None
    GPAModel = None
    pData = 0

    def __init__(self, Data, pData) -> None:
        self.pData = pData
        self.FinalModel = FinalScorePredict(Data)
        self.UpClassModel = UpClassPredict(Data)
        self.GPAModel = GPAPredict(Data)

    def CompareTable(self) -> pd.DataFrame():
        Table = pd.DataFrame({
            'Tên':['Điểm cuối kỳ','GPA','Đăng ký MC4AI'],
            'AI':[self.FinalModel.PredictFinal(self.pData), self.GPAModel.PredictGPA(self.pData), self.UpClassModel.PredictUpClass(self.pData)],
            'Thực tế': self.pData[['S10','GPA','REG-MC4AI']]
        })
        return Table.reset_index(drop=True)

    

# def test():
#     Data = pd.read_csv('py4ai-score.csv')
#     # model = FinalScorePredict(Data)
#     # print(model.PredictFinal(Data.iloc[86]))
#     print(Data.iloc[105])
#     model = ComparePredictReal(Data,Data.iloc[105])
#     print(model.CompareTable())
#     # model = GPAPredict(Data)
#     # print(model.PredictGPA(Data.iloc[86]))
#     pass

# if __name__ == '__main__':
#     test()

