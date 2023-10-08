# SMSContactsManager
[connected applications](https://github.com/randeath/SMSSENDER)  

It allows the computer to store the phone number and message content to be sent to the server.

Additionally, it creates an API using request and helps to read messages from the internal server.

In case of the server, when the send button is pressed, the contents are saved in the DB, the 8000 port is closed, and the apiserver.py file is re-executed.

Based on this, we can create api through application link, and we need to separately run api server.py to check the internal port separately.

I created the DB based on mysql and used MariaDB.
