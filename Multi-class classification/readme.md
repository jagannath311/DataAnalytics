# Multi class classification of penguin species:
Created a multi-class classifier upon existing binary classifier from sklearn to classify the penguin species.

Input: The dataset contains penguin attributes like Clutch completion, Culmen length, species etc. <br/>
link: Train data : https://drive.google.com/file/d/1Y71mPtZGsOrg8YeJW0yjF6aKGqcaagM_/view?usp=share_link <br/>
      Test data : https://drive.google.com/file/d/1DNOx3wOoyB2Foeehfb_ubNfrT_RXU7Ji/view?usp=share_link

Output: Species to which penguin belongs.

Files description:
classifier.py - It will take paths of the data and performs the classification using knn, decision tree, random forest and provides the results in the files predicted_knn, predicted_dtc, predicted_rf. <br/>
extras.ipynb : It contains all the code related to feauture engineering, error metrics calculation etc.


commands to run: <br/>
``` py classifier.py pathoftraindata pathoftestdata ```