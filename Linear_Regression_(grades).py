import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from twilio.rest import Client

googleSheetsID = '1RNnWiuirzG5lle7zqUHjkgPQGux37sdbB8HROjfDiKg'
workSheetName = 'Grades'

URL = 'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheets={1}'.format(
    googleSheetsID,
    workSheetName
    )

df = pd.read_csv(URL) ##this comes with extra vals
df2 = df.set_index('Quarter') ## this gets rid of extra vals

print(df2)  ##Datatable of vals in the CSV file

X = df.iloc[:, 0].values.reshape(-1, 1)  # values converts it into a numpy array
Y = df.iloc[:, 1].values.reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column
linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(X, Y)  # perform linear regression
linear_regressor = LinearRegression().fit(X, Y)
Y_pred = linear_regressor.predict(X)  # make predictions


r_sq = linear_regressor.score(X, Y) ##The r^2 value, which tells how related values are to eachother, higher better
print('coefficent of determination:', r_sq)


print('intercept: ', linear_regressor.intercept_) ##found the intercept and the slope
print('Slope: ', linear_regressor.coef_)


Y_pred = linear_regressor.predict(X) ##gives predicted values of the results
print('Predicted respose: ', Y_pred, sep='\n')


if Y_pred[1]/88 >1:  ## Y_pred (list of pred values)
    print('cool')
else:
    print('no')


##when comparing predicted/actual, this will let us grab the predicted
curr_quar = int(input("What quarter are we on: "))-1 ##we need the minus one because the first quarter garde would technically come from the zero index, or index -1
pred_val=(Y_pred[curr_quar])
print(f'predicted val: {pred_val}')


##Get the actual grade from the csv
act_val = df.iat[curr_quar ,1]
#print(act_val)
 ##the (zero, zero) is 1, top left number,   Zero is the first quater, and y should always be 1
print(f'Actual Grade: {act_val}')


## Find the percent difference between the actual grade and te real grade
per_diff = ((pred_val-act_val)/pred_val)*100
double_percent_val = '%.f'% per_diff
print(f'Percent difderence: {double_percent_val}%')


##Send automated emails
## link: https://www.twilio.com/docs/sms/send-messages
def send_mail():
    account_sid = 'AC6e07de95d0e549506bda40cb4bc79a9f'  ## need to find a way to hide the account sid and auth token
    auth_token = '62dcb7b591af323179b1dca2dbef5b06'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f'Hey this student may need some help, the percent difference betweent the grades was {double_percent_val}% ',
        from_='+18509044362',
        to='+18455468642'
    )
    print(message.sid)


if per_diff>10:
    send_mail()  ##this function will text my phone number when ran
else:
    print('All good')


plt.scatter(X, Y)  ##cant use any type of print or return statements after this since the graph is created and stays until the graph is exited
plt.plot(X, Y_pred, color='green')
plt.show()


plt.figure(figsize=(15,10))
plt.tight_layout()
