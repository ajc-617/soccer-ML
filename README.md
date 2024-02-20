# soccer-ML
Here are the steps to run my soccer classification model training and testing:
1. make sure you've pip installed torch, sklearn, pandas, numpy, and matplotlib
2. cd src
3. Type "python3 main.py" to start model training
4. In the console, you will see k-fold cross-validation in action for finding the ideal hyperparameters: For each combination of hyperparameters, you will see the current learning rate (or step size), the current regularization parameter, and the current batch size used for training, along with the validation accuracy produced by that hyperparameter combination.
5. Once all combinations of hyperparameters have been checked to determine which one yielded the best average validation accuracy, you will see the learning rate/regularizaiton parameter/batch size combination that yielded the highest validation accuracy, along with that highest validation accuracy and finally the testing accuracy on the testing set (it should be around 55-57%)
