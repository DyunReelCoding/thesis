import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
from mlxtend.plotting import plot_confusion_matrix
import joblib

# Load the ransomware dataset
df1 = pd.read_csv('./datasets/ransomware.csv')

# Drop unnecessary columns
df1 = df1.drop(columns=['FileName', 'md5Hash'])

# Convert categorical columns to codes
columns = ["Machine", "DebugSize", "NumberOfSections", "SizeOfStackReserve", "MajorOSVersion", "BitcoinAddresses"]
for col in columns:
    df1[col] = df1[col].astype('category').cat.codes

# Remove duplicate rows
df1 = df1.drop_duplicates(keep='last')

# Save the cleaned dataset to a new CSV file
df1.to_csv("./datasets/df_clear.csv", index=False)

# Load the cleaned dataset
df1 = pd.read_csv("./datasets/df_clear.csv")

# Split the data into features and target
X = df1.iloc[:, :-1].values  # Features (all columns except the last)
y = df1.iloc[:, -1].values    # Target (the last column)

# Split data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Create and fit the Random Forest Classifier
rf = RandomForestClassifier(n_estimators=100, random_state=0)
rf.fit(X_train, y_train)

# Save the trained model to a file
joblib.dump(rf, './trained_model/random_forest_model.pkl')

# Predict the classes of the testing set
y_pred = rf.predict(X_test)

# Print the accuracy of the model
accuracy = rf.score(X_test, y_test)
print(f"Accuracy: {accuracy * 100:.2f}%")

# Calculate cross-validation scores
scores = cross_val_score(rf, X, y, cv=5)
print("Cross-Validation Scores:", scores)
print("Mean Score:", scores.mean())

# Print confusion matrix and classification report
print("Confusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
print(cm)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Plot confusion matrix
fig, ax = plot_confusion_matrix(conf_mat=cm, figsize=(6, 6), cmap=plt.cm.Greens)
plt.xlabel('Predictions', fontsize=18)
plt.ylabel('Actuals', fontsize=18)
plt.title('Confusion Matrix', fontsize=18)
plt.show()
