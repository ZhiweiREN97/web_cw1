To use this client, the users should install the “requests” and “prettytable” library that is supposed to be pip-installed. I will explain all the possible commands.
“register”: after you enter “register”, the client will let you enter username, password and email. If your user name is possible to use, the register process will be success.
“login”: after you enter “login”, the system will let you enter username and password to login.
“logout”: you can enter “logout” to log out your account.
“list”: this command will list all module instances.
“view”: this command will list the average score of all professors.
“average [professor_id] [module_code]”: after enter “average” and the professor id as well as module code, the server will return the average rating of a certain professor in a certain module.
“rate [professor_id] [module_code] [year] [semester] [rating]”, after you typed such commands, you can rate the teaching of one professor in a certain module instance. You need to log in to use this API. 
“exit”: enter exit to exit the client application.