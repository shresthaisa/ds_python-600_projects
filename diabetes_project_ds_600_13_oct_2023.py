# -*- coding: utf-8 -*-
"""Diabetes_project_DS-600_13_oct_2023.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11SAGIVfYc0bV1YUH53gP6KFnby-3Q8JM

# predict onset of diabetes based on diagnostic measures.
* use ML algorithm to classify diabetes.Plot and display necessary metrics.use EDA for feature selection.
* do necessary feature engineering and modeling and evaluation with explanation
"""

import pandas as pd
df=pd.read_csv('/content/diabetes.csv')
df.sample(1)

"""# Data profiling and inspection



"""

df.dtypes # shows the datatypes of each feature
# features like pregnancies,glucose,bloodpressure has integer where as BMI and DiabetesPedigreeFunction has float value

df.info() # gives you information about datatype and presence of any null values in the dataset

df.shape #( num of rows and columns)
# the dataframe has 768 rows and 9 columns

df.columns # list of cloumns of the dataframe

df.describe() # descriptive statistics of features

df.isna().sum()
#shows the sum of any null values in any rows, here none of the rows has null values

df.isna().sum()/len(df) * 100
 # none of the column has missing data
 # there is zero vlaue in some columns

#none of the column has missing data
 # there is zero vlaue in some columns
df.isnull()

print(df.isnull().sum())

import numpy as np
a=df[['Insulin','Glucose','BloodPressure','SkinThickness','BMI']]
b=a.replace(0,np.NaN)
b
# replacing the features with zero with NaN

# univarate data analysis

df.hist(figsize=(20,20))
# hist plot of each features
#around 250 patients with 0 or 1 pregnancy
#100-125 patients with glucose level >200

df['Outcome'].plot(kind='hist',bins=30)
# 500 0 = no diabetes and aprox 300 1= yes diabetes

df['Pregnancies'].value_counts() # gives you count of values in the pregnancy column
# 1 women only has 17 pregnancies and 135 women has 1 pregnancy
# pregnancies has value zero

df['Insulin'].value_counts()# insulin has 374 rows with zero value  which is not missing value

df['SkinThickness'].value_counts()  # has 227 zero values

df['Pregnancies'].plot(kind='hist',bins=50)

"""# EDA :Explanatory Data analysis
HERE outcome has value 0 and 1. this is what we want to predict with features like BMI,Glucose,insulin,etc.are features upon which the outcome of diabetes
depends.
data type is binary: 0 means an individual has no diabetes and 1 means one has diabetes.
"""

# anaylse target or dependent variable

df['Outcome'].value_counts()
# outcome is a target

# the outcome contains two values 0 and 1 and has 500 zeros which means 500 patient has no diabetes  and 268 are non diabetic ones.

#to check if the values are imbalance? visualize in piechart
import matplotlib.pyplot as plt
outcome_freq = df['Outcome'].value_counts()
plt.pie(outcome_freq.values, labels=outcome_freq.index, autopct='%.2f')
plt.show()

# here the piechart shows that the data is imbalanced. therefore we use f1 score evaluation metrics.

# lets see if Pregnancies and outcome i.e. probability of having diabetes has any relation

import seaborn as sns
figsize=(5,10)
sns.countplot(x='Pregnancies', hue = 'Outcome', data = df)

# above figure shows that more people with zero pregnancy had no diabetes whereas few num with zero pregnancy had diabetes
# similar trend is obtained in women with 6 pregnacy too, more women with 6 pregnancy had no diabetes but less num had diabetes
#bt less women with 7 pregnancy had no diabetes whereas more women had a diabetes
 #more than 60 and less than 80 people with 0 pregnancy had diabetes where as more than 100 with 1 pregnancy had no diabetes at all
 #seems like there is relation betn num of pregnancies and onset of diabetes

df.corr()
# correlation between features in an uncleaned dataframe

sns.heatmap(df.corr(),annot=True) # checking corelation on data before cleaning NaN VALUES
#each feature has perfect correlation with oneself thats why there is 1 in diagnoal
#glucose has highest correlation with outcome of diabetes
# age and pregnancies has high correlation

sns.pairplot(data=df,hue='Outcome')

import matplotlib.pyplot as plt
plt.figure(figsize=(15,5))
df.boxplot()

df['Insulin'].describe()
# outlier in insulin ,75% data is 127, max value is 846

df['Age'].describe()

df['BMI'].describe()

df['BloodPressure'].describe()

# identifying dependent and independent variable

X = df.iloc[:, :-1]
y = df.Outcome
X

y

df_copy=df.copy(deep=True)
df_copy[['Pregnancies','Insulin','Glucose','BloodPressure','SkinThickness','DiabetesPedigreeFunction','BMI']]=df_copy[['Pregnancies','Insulin','Glucose','BloodPressure','SkinThickness','DiabetesPedigreeFunction','BMI']].replace(0,np.NaN)
df_copy

df_copy.describe()

# lets check if there is any missing data and visualize it

# replacing NaN values with mean in all the columns

df_copy['Pregnancies'].fillna(df_copy['Pregnancies'].mean(),inplace=True)
df_copy['Glucose'].fillna(df_copy['Glucose'].mean(),inplace=True)
df_copy['BloodPressure'].fillna(df_copy['BloodPressure'].median(),inplace=True)
df_copy['SkinThickness'].fillna(df_copy['SkinThickness'].median(),inplace=True)
df_copy['Insulin'].fillna(df_copy['Insulin'].mean(),inplace=True)
df_copy['BMI'].fillna(df_copy['BMI'].mean(),inplace=True)

sns.heatmap(df_copy.corr(),annot=True) # correlation between the features after filling up NaN values with mean and meadian of individual features
# outcome of diabetes is correlated with blood glucose level and pregnancies  where as it is not in good correlation with skin thickness

X1 = df_copy.iloc[:, :-1]
y1 = df_copy.Outcome
# identification of target and feature

# training data set

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X1, y1, test_size=0.2, random_state=42)

from sklearn.linear_model import LogisticRegression
model= LogisticRegression(max_iter=5000)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score

cm = confusion_matrix(y_true=y_test, y_pred=y_pred)
cm

accuracy = accuracy_score(y_test, y_pred)
accuracy

from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score
recall_score(y_true=y_test, y_pred=y_pred)

from sklearn.metrics import f1_score
f1_score(y_true=y_test, y_pred=y_pred)

from sklearn.metrics import ConfusionMatrixDisplay
ConfusionMatrixDisplay.from_estimator(model, X_test, y_test, cmap='Blues')

from sklearn.metrics import classification_report
report = classification_report(y_true = y_test, y_pred=y_pred)
print(report)

