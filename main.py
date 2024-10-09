# Project packages
import api
import login

if login.LoginWindow().login_success:
    api.APIWindow()
