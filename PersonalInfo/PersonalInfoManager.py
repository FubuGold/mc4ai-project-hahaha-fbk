import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

class UpClassPredict:
    __UpClassPredictModel = LogisticRegression()
    score = 0

    def __init__(self, data) -> None:
        self.__TrainUpClassPredict(data)

    def __TrainUpClassPredict(self, Data) -> None:
        X = np.append(Data.iloc[:,4:14].isnull()
                      .to_numpy()
                      .sum(axis=1)
                      .reshape(-1,1),
                      Data['GPA'].fillna(0).to_numpy().reshape(-1,1), axis = 1)
        y = Data['REG-MC4AI'].apply(lambda x: 1 if x == 'Y' else 0)
        X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.3)
        self.__UpClassPredictModel.fit(X_train,y_train)

        self.score = self.__UpClassPredictModel.score(X_test,y_test)

    def PredictUpClass(self, pData):
        if pData['GPA'] == float('nan'): pData['GPA'] = 0
        pData = np.array([pData.iloc[4:14].isnull().sum(),pData['GPA']]).reshape(1,-1)
        # print(type(pData))
        return self.__UpClassPredictModel.predict(pData)[0]
    
class FinalScorePredict:
    __FinalPredictModel = LinearRegression()
    score = 0

    def __init__(self, data) -> None:
        self.__TrainFinalPredict(data)

    def __TrainFinalPredict(self, Data) -> None:
        X = np.append(Data.iloc[:, 4:13]
                            .drop(labels = 'S6', axis = 1)
                            .fillna(0)
                            .apply(np.sum, axis = 1)
                            .to_numpy()
                            .reshape(-1,1),
                        Data['S6'].fillna(0).to_numpy().reshape(-1,1), axis = 1)
        y = Data['S10'].fillna(0)
        X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.3)
        self.__FinalPredictModel.fit(X_train,y_train)

        self.score = self.__FinalPredictModel.score(X_test,y_test)
        

    def PredictFinal(self, pData):
        pData = np.append(pData.iloc[4:13]
                         .drop(labels = 'S6')
                         .fillna(0)
                         .sum()
                         .reshape(-1,1),
                      pData.loc['S6'].reshape(-1,1), axis = 1)
        return self.__FinalPredictModel.predict(pData).round(1)[0]
    
class GPAPredict:
    __GPAPredictModel = LinearRegression()
    score = 0

    def __init__(self,Data) -> None:
        self.__TrainGPAPredict(Data)
    
    def __TrainGPAPredict(self, Data) -> None:
        X = Data[['S6','S10','BONUS']].fillna(0).to_numpy()
        y = Data['GPA'].fillna(0)
        X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.3)
        self.__GPAPredictModel.fit(X_train,y_train)
        
        self.score = self.__GPAPredictModel.score(X_test,y_test)

    def PredictGPA(self, pData):
        pData = pData[['S6','S10','BONUS']].fillna(0).to_numpy().reshape(1,-1)
        return self.__GPAPredictModel.predict(pData).round(1)[0]
    

class ComparePredictReal:

    FinalModel = None
    GPAModel = None
    UpClassModel = None

    def __init__(self, Data) -> None:
        self.FinalModel = FinalScorePredict(Data)
        self.UpClassModel = UpClassPredict(Data)
        self.GPAModel = GPAPredict(Data)

    def TransfromScore(self,score) -> str:
        return str(round(score,2)) + '%'

    def CompareTable(self,pData) -> pd.DataFrame():
        score = [self.FinalModel.score, self.GPAModel.score, self.UpClassModel.score]
        score = [self.TransfromScore(x*100) for x in score]
        Table = pd.DataFrame({
            'Tên':['Điểm cuối kỳ','GPA','Đăng ký MC4AI'],
            'AI':[self.FinalModel.PredictFinal(pData), self.GPAModel.PredictGPA(pData), self.UpClassModel.PredictUpClass(pData)],
            'Thực tế': pData[['S10','GPA','REG-MC4AI']],
            'Độ chính xác': score
        })
        if Table.iloc[2,1] == 1: Table.iloc[2,1] = 'Y'
        else: Table.iloc[2,1] = ''
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

# if __name__ == '__main__':
#     test()

