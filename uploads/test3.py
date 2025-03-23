import pandas as pd                                                                                              
import matplotlib.pyplot as plt                                                                                  
import seaborn as sns                                                                                            
import os                                                                                                        
from sklearn.linear_model import LinearRegression                                                                
from sklearn.model_selection import train_test_split                                                             
from sklearn.metrics import mean_squared_error                                                                   
                                                                                                                
# 加载数据                                                                                                       
data_path = '/Users/esca/Desktop/Agent/data/anime-dataset-2023.csv'                                              
data = pd.read_csv(data_path)                                                                                    
                                                                                                                
# 保存输出目录                                                                                                   
output_dir = './outputs'                                                                                         
if not os.path.exists(output_dir):                                                                               
    os.makedirs(output_dir)                                                                                      
                                                                                                                
# 分析Score的影响因素                                                                                            
# 选择数值型特征进行分析                                                                                         
numeric_features = ['Popularity', 'Favorites', 'Members', 'Scored By']                                           
X = data[numeric_features]                                                                                       
y = data['Score']                                                                                                
                                                                                                                
# 检查缺失值                                                                                                     
print("数值型特征的缺失值统计:")                                                                                 
print(X.isnull().sum())                                                                                          
                                                                                                                
# 填充缺失值（如果有）                                                                                           
X = X.fillna(X.mean())                                                                                           
                                                                                                                
# 划分训练集和测试集                                                                                             
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)                        
                                                                                                                
# 训练线性回归模型                                                                                               
model = LinearRegression()                                                                                       
model.fit(X_train, y_train)                                                                                      
                                                                                                                
# 预测与评估                                                                                                     
y_pred = model.predict(X_test)                                                                                   
mse = mean_squared_error(y_test, y_pred)                                                                         
print(f"线性回归模型的均方误差 (MSE): {mse}")                                                                    
                                                                                                                
# 保存模型系数                                                                                                   
coefficients = pd.Series(model.coef_, index=numeric_features)                                                    
print("模型系数:")                                                                                               
print(coefficients)                                                                                              
                                                                                                                
# 绘制特征重要性图                                                                                               
plt.figure(figsize=(10, 6))                                                                                      
sns.barplot(x=coefficients.index, y=coefficients.values, palette='viridis')                                      
plt.title('特征对Score的影响')                                                                                   
plt.xlabel('特征')                                                                                               
plt.ylabel('系数')                                                                                               
plt.savefig(f'{output_dir}/feature_importance.png')                                                              
plt.close()                                                                                                      
                                                                                                                
print("已保存特征重要性图到 outputs/feature_importance.png")    