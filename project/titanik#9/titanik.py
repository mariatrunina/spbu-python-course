import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, accuracy_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_squared_error as rmse



data = pd.read_csv('/workspaces/spbu-python-course/project/titanik#9/titanic.csv') 
print(data.head())

# DataCleaning
print(data.isnull().sum())
data = data.dropna() 

# EDA. Гистограммы возраста пассажиров
plt.figure(figsize=(10, 6))
sns.histplot(data['Age'], bins=30, kde=True)
plt.title('Distribution of Ages')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.show()

# Соотношение выживаемости по полу
plt.figure(figsize=(8, 5))
sns.countplot(x='Survived', hue='Sex', data=data)
plt.title('Survivorship by Sex')
plt.xlabel('Survived')
plt.ylabel('Count')
plt.show()

# Преобразование категориальных признаков в числовые
data = pd.get_dummies(data, columns=['Sex', 'Embarked'], drop_first=True)  
data = data.drop(['Name', 'Ticket', 'Cabin'], axis=1)


# Разделение данных на обучающую и тестовую выборки
x = data.drop('Survived', axis=1) 
y = data['Survived']  
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Обучение модели
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(x_train, y_train)
y_pred = model.predict(x_test)

precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
accuracy = accuracy_score(y_test, y_pred)

print(f'Precision: {precision:.2f}, Recall: {recall:.2f}, Accuracy: {accuracy:.2f}')


x_reg = data.drop('Age', axis=1)  
y_reg = data['Age'] 

x_train_reg, x_test_reg, y_train_reg, y_test_reg = train_test_split(x_reg, y_reg, test_size=0.2, random_state=42)
reg_model = LinearRegression()
reg_model.fit(x_train_reg, y_train_reg)
y_pred_reg = reg_model.predict(x_test_reg)

rmse_value = rmse(y_test_reg, y_pred_reg)  # RMSE
print(f'Root Mean Squared Error: {rmse_value:.2f}')  # Вывод RMSE