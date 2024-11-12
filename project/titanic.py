import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


train_data = pd.read_csv("/workspaces/spbu-python-course/project/train.csv")
test_data = pd.read_csv("/workspaces/spbu-python-course/project/test.csv")

titanic_data = pd.concat([train_data, test_data], ignore_index=True)

titanic_data["Survived"] = titanic_data["Survived"].astype("category")
titanic_data["Pclass"] = titanic_data["Pclass"].astype("category")
titanic_data["Sex"] = titanic_data["Sex"].astype("category")

titanic_data.info()

# Основная статистика
statistics = titanic_data.describe(include="all")

# Количество пассажиров в каждом классе
passenger_counts = titanic_data["Pclass"].value_counts()
most_passengers_class = passenger_counts.idxmax()

# Группировка по классам и полу
age_group = titanic_data.groupby(["Pclass", "Sex"], observed=True)["Age"].mean()

# Найдем самую юную и самую старую комбинацию
youngest = age_group.idxmin()
oldest = age_group.idxmax()
age_difference = age_group.max() - age_group.min()

# Отбор выживших пассажиров с фамилией на "K"
survivors_k = titanic_data[titanic_data["Survived"] == 1]
survivors_k = survivors_k[survivors_k["Name"].str.contains(" K")]

# Сортировка по стоимости билета
sorted_survivors = survivors_k.sort_values(by="Fare", ascending=False)
highest_fare = sorted_survivors.iloc[0]
lowest_fare = sorted_survivors.iloc[-1]

# Максимальное количество родных с выжившим пассажиром
max_relatives = survivors_k["SibSp"].max() + survivors_k["Parch"].max()

# Средняя стоимость билета с и без указания каюты
fare_with_cabin = titanic_data[titanic_data["Cabin"].notna()]["Fare"].mean()
fare_without_cabin = titanic_data[titanic_data["Cabin"].isna()]["Fare"].mean()
fare_difference = fare_with_cabin / fare_without_cabin

# 1. Scatter plot
sns.scatterplot(data=titanic_data, x="Age", y="Fare", hue="Survived")
plt.title("Scatter plot of Age vs Fare")
plt.show()

# 2. Linear plot
sns.lineplot(data=titanic_data, x="Age", y="Fare", hue="Pclass", estimator="mean")
plt.title("Average Fare by Age and Class")
plt.show()

# 3. Histogram
sns.histplot(data=titanic_data, x="Age", bins=30, kde=True)
plt.title("Age Distribution")
plt.show()

# 4. Bar chart
sns.countplot(data=titanic_data, x="Pclass")
plt.title("Number of Passengers by Class")
plt.show()

# 5. Horizontal bar chart
sns.countplot(data=titanic_data, y="Sex")
plt.title("Number of Passengers by Gender")
plt.show()

# 6. Pie chart
fig = px.pie(titanic_data, names="Survived", title="Survival Distribution")
fig.show()

# 7. Box chart
sns.boxplot(data=titanic_data, x="Pclass", y="Fare")
plt.title("Fare Distribution by Class")
plt.show()

# 8. Sunburst chart
fig = px.sunburst(titanic_data, path=["Pclass", "Sex", "Survived"], values="Fare")
fig.show()

# 9. 3D plot
fig = px.scatter_3d(titanic_data, x="Age", y="Fare", z="Pclass", color="Survived")
fig.show()

# 10. Pair plot
sns.pairplot(titanic_data, hue="Survived")
plt.show()
