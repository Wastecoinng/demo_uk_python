import os
from django.shortcuts import render
from .models import WastecoinUser,WastecoinAgent,Coin,minedCoin,redeemCoin,notifications,Transaction,otp
from datetime import datetime,timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth import login,logout, authenticate
from CustomCode import string_generator,password_functions,validator,autentication
from django.db.models import Sum,Q
from django.core.mail import send_mail
# from CustomCode import string_generator,password_functions,validator,autentication


# Landing page
def index(request):
    if request.user.is_authenticated: 
        agent = WastecoinAgent.objects.filter(user=request.user)
        user = WastecoinUser.objects.filter(user=request.user)
        if agent:
            return HttpResponseRedirect(reverse("dashboard_agent"))
        if user:
            return HttpResponseRedirect(reverse("dashboard"))
    else:
        return render(request,"home.html") 

# signup view page
def register(request):
    return render(request,"register.html") 
# our teeam page
def ourteam(request):
    return render(request, "ourteam.html")

# FAQ page
def faq(request):
    return render(request, "faq.html")

# FAQ page
def privatepolicy(request):
    return render(request, "privatepolicy.html")

# signup for agent view page
def registeragent(request):
    return render(request,"registerAgent.html") 


# @api_view(["POST"])
# def user_verification(request):
#     email =str(request.session['email'])
#     # appuser = User.objects.get(username=email)
#     otp_entered = request.data.get("otp",None)
#     if otp_entered != None and otp_entered != "":
#         # user = authenticate(request,username=appuser.email, password =appuser.password )
#         user_data = otp.objects.get(user=email)
#         # if user:
#         return_data = {
#             "error": "0",
#             "message":"hu u are getting there."+str(user_data)
#         }

#         return render(request,"verification.html", return_data) 

# User verfication
@api_view(["POST"])
def user_verification(request):
    try:
        otp_entered = request.data.get("otp",None)
        if otp_entered != None and otp_entered != "":
            # user = authenticate(request,username=request.session['email'])
            user_data = otp.objects.get(user=request.session['email'])
            otpCode,date_added = str(user_data.otp_code),user_data.date_added
            date_now = datetime.now(timezone.utc)
            duration = float((date_now - date_added).total_seconds())
            timeLimit = 1800.0 #30 mins interval
            if otp_entered == otpCode and duration < timeLimit:
                #validate user
                user_data.validated = True
                user_data.save()
                return_data = {
                    "error": "0",
                    "message":"Congratulations! Your account has been Verified."
                }
                return render(request,"login.html", return_data) 
            elif otp_entered != otpCode and duration < timeLimit:
                return_data = {
                    "error": "1",
                    "message": "Incorrect OTP"
                }
            elif otp_entered == otpCode and duration > timeLimit:
                user_data.save()
                return_data = {
                    "error": "1",
                    "message": "OTP has expired"
                }
        else:
            return_data = {
                "error": "2",
                "message": "Invalid Parameters"+str(user_data.user)
            }
    except Exception as e:
        return_data = {
            "error": "3",
            "message": str(e)
        }
    return render(request,"verification.html", return_data) 

# resend code
def resend_code(request):
    email =request.session['email']
    initial = 1
    generator =string_generator.numeric(5)
    stringCode = str(initial) +''+str(generator)
    newCode = int(stringCode)

    updateOtp=otp.objects.filter(user=email).update(otp_code=newCode)
    if updateOtp:
        send_mail(
        'Please Activate your Account, Again!',
        'Your verification Code is '+ str(newCode),
        'info@wastecoin.co',
        [email],
        # fail_silently=False,
        )
        return_data = {
            "error": "0",
            "message":"New Verification code has been sent to "+ str(email),
        }
    else:
        return_data = {
        "error": "1",
        "message":"Sorry try again",
        }
    return render(request,"verification.html", return_data) 

# # User login
# @api_view(["POST"])
# def user_loginapi(request):
#     email_phone=request.POST["email_phone"]
#     password=request.POST["password"]
#     user = authenticate(request,username=email_phone, password=password)

#     # newly added
#     if user.is_superuser:
#         return HttpResponseRedirect(reverse("dashboard_admin"))
#     # newly added end
#     if  user is None:
#          return render(request,"login.html",{"message":"Sorry! User do not exist. Please Register. Thanks"})

#     user_validation = otp.objects.get(user=email_phone)
#     if  user is not None and user_validation.validated is False:
#          return render(request,"login.html",{"message":"Your Account is not validated! Please call 070-000-000-00 for immediate assistance"})

#     if user is not None and user_validation.validated is True:
#         login(request,user)
#         agent = WastecoinAgent.objects.filter(user=request.user)
#         user = WastecoinUser.objects.filter(user=request.user)
#         if agent:
#             return HttpResponseRedirect(reverse("dashboard_agent"))

#         if user:
#             return HttpResponseRedirect(reverse("dashboard"))
#     else:
#         return render(request,"login.html",{"message":"Invalid credentials"})

# User login
@api_view(["POST"])
def user_loginapi(request):
    email_phone=request.POST["email_phone"]
    password=request.POST["password"]
    user = authenticate(request,username=email_phone, password=password)

    if  user is None:
         return render(request,"login.html",{"message":"Sorry! User do not exist. Please Register. Thanks"})

    # newly added
    if user.is_superuser:
        return HttpResponseRedirect(reverse("dashboard_admin"))
    # newly added end

    user_validation = otp.objects.get(user=user)
    if  user is not None and user_validation.validated is False:
         return render(request,"verification.html",{"message":"Your Account is not validated! Please call 070-000-000-00 for immediate assistance"})

    

    if user is not None and user_validation.validated is True:
        login(request,user)
        agent = WastecoinAgent.objects.filter(user=request.user)
        user = WastecoinUser.objects.filter(user=request.user)
        if agent:
            return HttpResponseRedirect(reverse("dashboard_agent"))

        if user:
            return HttpResponseRedirect(reverse("dashboard"))
    else:
        return render(request,"login.html",{"message":"Invalid credentials"})
        
# user registration api
@api_view(["POST"])
def user_registrationapi(request):
    try:
        firstName = request.data.get('firstname',None)
        lastName = request.data.get('lastname',None)
        # phoneNumber = request.data.get('phonenumber',None)
        email = request.data.get('email',None)
        # gender = request.data.get('gender',None)
        password = request.data.get('password',None)
        confirmPassword = request.data.get('confirmPassword',None)
        # address = request.data.get('address',None)
        # lga = request.data.get('lga',None)
        state = request.data.get('state',None)
        country = request.data.get('country',None)
        reg_field = [firstName,lastName,email,password,confirmPassword,state,country]
        if not None in reg_field and not "" in reg_field:
            if User.objects.filter(email =email).exists():
                return_data = {
                    "error": "1",
                    "message": "User Exists"
                }
            if password != confirmPassword:
                return_data = {
                    "error": "1",
                    "message": "Password is not the same"
                }
            else:
                request.session['email'] =email
                user=User.objects.create_user(email, email,password)
                user.first_name=firstName
                user.last_name=lastName
                user.save()
                #Generate OTP
                initial = 5
                generator =string_generator.numeric(5)
                stringCode = str(initial) +''+str(generator)
                Otpcode = int(stringCode)
                code = Otpcode
                #Save OTP
                user_OTP =otp(user=user,otp_code=code)
                # user_OTP =otp(user=email,otp_code=code, validated=True)
                user_OTP.save()
                m = WastecoinUser(user=user, firstname=firstName, lastname=lastName, email=email, user_state=state, user_country=country) 
                m.save()
                n = notifications(sender="Admin", header="Welcome to WasteCoin, "+ str(user.first_name)+"!", message="Thank you for joining WasteCoin, "+ str(user.first_name)+"! Let's get the mining started already!", receiver=user) 
                n.save()
                send_mail(
                    str(user.first_name)+'! Please Activate your Account',
                    'Your verification Code is '+ str(code),
                    'wastecoinng@gmail.com',
                    [email],
                    fail_silently=False,
                )
                # verification.messages.create(
                #     from_=twilio_number, 
                #     to="+234"+phoneNumber,
                #     body='You verification code is: '+ code                
                #     )
                return_data = {
                    "error": "0",
                    "message":"The registration was successful.",
                    }
                return render(request,"verification.html", return_data) 
        else:
            return_data = {
                "error":"2",
                "message": "Invalid Parameter"
            }
    except Exception as e:
        return_data = {
            "error": "3",
            "message": str(e)
        }
    return render(request,"login.html", return_data) 

# agent registration api
@api_view(["POST"])
def agent_registrationapi(request):
    try:
        firstName = request.data.get('firstname',None)
        lastName = request.data.get('lastname',None)
        phoneNumber = request.data.get('phonenumber',None)
        email = request.data.get('email',None)
        gender = request.data.get('gender',None)
        password = request.data.get('password',None)
        confirmPassword = request.data.get('confirmPassword',None)
        address = request.data.get('address',None)
        lga = request.data.get('lga',None)
        state = request.data.get('state',None)
        country = request.data.get('country',None)
        agentid = request.data.get('agentid',None)
        reg_field = [firstName,lastName,phoneNumber,email,password,confirmPassword,address,lga,state,country, agentid]
        if not None in reg_field and not "" in reg_field:
            if User.objects.filter(username=agentid).exists():
                return_data = {
                    "error": "1",
                    "message": "Agent Exists"
                }
            if password != confirmPassword:
                return_data = {
                    "error": "1",
                    "message": "Password is not the same"
                }
            else:
                user=User.objects.create_user(agentid, email,password)
                user.first_name=firstName
                user.last_name=lastName
                user.save()
                m = WastecoinAgent(user=user, firstname=firstName, lastname=lastName, email=email,user_phone=phoneNumber, user_gender=gender, user_address=address, user_state=state, user_lga=lga, user_country=country) 
                m.save()
                n = notifications(sender="Admin", header="Welcome to WasteCoin, Agent "+ str(user.first_name)+"!", message="Thank you for joining WasteCoin, "+ str(user.first_name)+"! Let's get the mining started already!", receiver=user) 
                n.save()
                #Generate OTP
                code = string_generator.numeric(6)
                #Save OTP
                user_OTP =otp(user=agentid,user_phone=phoneNumber,otp_code=code, validated=True)
                user_OTP.save()
                return_data = {
                    "error": "0",
                    "message":"The registration was successful",
                    }
        else:
            return_data = {
                "error":"2",
                "message": "Invalid Parameter"
            }
    except Exception as e:
        return_data = {
            "error": "3",
            "message": str(e)
        }
    return render(request,"login.html", return_data)

# verification view page
def loginpage(request):
    return render(request,"login.html") 

# reset password view page
def resetpassword(request):
    return render(request,"resetpassword.html") 

# dashboard view page
def dashboard(request):
    unreadMessages = notifications.objects.filter(receiver=request.user, beenRead ="No").order_by('-date_added').count()
    userState = WastecoinUser.objects.get(user=request.user).user_state
    totalCoins = Coin.objects.filter(state=userState).order_by('-date_added')[0]
    # totalCoins = Coin.objects.filter().order_by('-date_added')[0]
    minedCoins = minedCoin.objects.aggregate(Sum('minedCoin'))
    miner_list = WastecoinUser.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(miner_list, 4)
    try:
        miners = paginator.page(page)
    except PageNotAnInteger:
        miners = paginator.page(1)
    except EmptyPage:
        miners = paginator.page(paginator.num_pages)
    return_data = {
        "user":request.user,
        "unreadMsg": unreadMessages,
        "allocatedWasteCoins": totalCoins,
        "minedCoins": minedCoins,
        "userman": WastecoinUser.objects.filter(user=request.user),
        "miner": miners,
        }
    return render(request,"dashboard_home.html", return_data) 


# dashboard view page
def dashboard_agent(request):
    unreadMessages = notifications.objects.filter(receiver=request.user, beenRead ="No").order_by('-date_added').count()
    agentState = WastecoinAgent.objects.get(user=request.user).user_state
    totalCoins = Coin.objects.filter(state=agentState).order_by('-date_added')[0]
    # totalCoins = Coin.objects.filter().order_by('-date_added')[0]
    minedCoins = minedCoin.objects.aggregate(Sum('minedCoin'))
    miner_list = WastecoinUser.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(miner_list, 4)
    try:
        miners = paginator.page(page)
    except PageNotAnInteger:
        miners = paginator.page(1)
    except EmptyPage:
        miners = paginator.page(paginator.num_pages)
    return_data = {
        "user":request.user,
        "unreadMsg": unreadMessages,
        "allocatedWasteCoins": totalCoins,
        "minedCoins": minedCoins,
        "miner": miners,
        "userman": WastecoinAgent.objects.filter(user=request.user),
        }
    return render(request,"dashboard_home_agent.html", return_data) 

# newly added ended
# profile agent view page
def profile_agent(request):
    unreadMessages = notifications.objects.filter(receiver=request.user, beenRead ="No").order_by('-date_added').count()
    return_data = {
        "unreadMsg": unreadMessages,
        "user":request.user,
        "userman": WastecoinAgent.objects.filter(user=request.user)
        }
    return render(request,"profile_agent.html", return_data) 

# profile view page
def profile(request):
    unreadMessages = notifications.objects.filter(receiver=request.user, beenRead ="No").order_by('-date_added').count()
    return_data = {
        "unreadMsg": unreadMessages,
        "user":request.user,
        "userman": WastecoinUser.objects.filter(user=request.user)
        }
    return render(request,"profile.html", return_data) 

# wallet view page
def wallet(request):
    unreadMessages = notifications.objects.filter(receiver=request.user, beenRead ="No").order_by('-date_added').count()
    totalCoins = Coin.objects.filter().order_by('-date_added')[0]
    minedCoins = minedCoin.objects.aggregate(Sum('minedCoin'))
    transaction_list = Transaction.objects.filter(Q(recipient=request.user) | Q(sender=request.user)).order_by('-date_added')
    page = request.GET.get('page', 1)
    paginator = Paginator(transaction_list, 5)
    try:
        transaction = paginator.page(page)
    except PageNotAnInteger:
        transaction = paginator.page(1)
    except EmptyPage:
        transaction = paginator.page(paginator.num_pages)
    return_data = {
        "user":request.user,
        "unreadMsg": unreadMessages,
        "allocatedWasteCoins": totalCoins,
        "minedCoins": minedCoins,
        "transaction": transaction,
        "userman": WastecoinUser.objects.filter(user=request.user)
        }
    return render(request,"wallet.html", return_data) 



# wallet agent view page
def wallet_agent(request):
    unreadMessages = notifications.objects.filter(receiver=request.user, beenRead ="No").order_by('-date_added').count()
    totalCoins = Coin.objects.filter().order_by('-date_added')[0]
    minedCoins = minedCoin.objects.aggregate(Sum('minedCoin'))
    transaction_list = Transaction.objects.filter(Q(recipient=request.user) | Q(sender=request.user)).order_by('-date_added')
    page = request.GET.get('page', 1)
    paginator = Paginator(transaction_list, 5)
    try:
        transaction = paginator.page(page)
    except PageNotAnInteger:
        transaction = paginator.page(1)
    except EmptyPage:
        transaction = paginator.page(paginator.num_pages)
    return_data = {
        "user":request.user,
        "unreadMsg": unreadMessages,
        "allocatedWasteCoins": totalCoins,
        "minedCoins": minedCoins,
        "transaction": transaction,
        "userman": WastecoinAgent.objects.filter(user=request.user)
        }
    return render(request,"wallet_agent.html", return_data) 

# notification view page
def notification(request):
    updateReadMessage=notifications.objects.filter(receiver=request.user).update(beenRead= "Yes")
    notification_list = notifications.objects.filter(receiver=request.user)
    page = request.GET.get('page', 1)
    paginator = Paginator(notification_list, 5)
    try:
        notificationss = paginator.page(page)
    except PageNotAnInteger:
        notificationss = paginator.page(1)
    except EmptyPage:
        notificationss = paginator.page(paginator.num_pages)
    agent = WastecoinAgent.objects.filter(user=request.user)
    user = WastecoinUser.objects.filter(user=request.user)
    return_data = {
        "user":request.user,
        "error": "0",
        "notification": notificationss,
        "userman": WastecoinUser.objects.filter(user=request.user)
        }
    if agent:
        return render(request,"notification_agent.html", return_data) 
    return render(request,"notification.html", return_data) 

# contact us api
@api_view(["POST"])
def contactusapi(request):
    fullName = request.data.get('fullName',None)
    phoneNumber = request.data.get('phonenumber',None)
    email = request.data.get('email',None)
    message = request.data.get('message',None)
    contact_field = [fullName,email,message]
    try:
        if not None in contact_field and not "" in contact_field:
            n = notifications(sender=fullName, header="Contact us Message from "+ str(email)+" -"+ str(phoneNumber), message=message, receiver="Admin") 
            n.save()
            return_data = {
                "error": "0",
                "message": 'Message well recieved! We will get back to you shortly.'
                }
        else:
            return_data = {
                "error":"2",
                "message": "Sorry! You did not fill some fields. Try again"
            }
    except Exception as e:
        return_data = {
            "error": "3",
            "message": str(e)
        }
    return render(request,"home.html", return_data)

# subscribe api
@api_view(["POST"])
def subscribeapi(request):
    sub_email = request.data.get('sub_email',None)
    sub_field = [sub_email]
    try:
        if not None in sub_field and not "" in sub_field:
            n = notifications(sender="Subscription", header="A new Subscriber with "+ str(sub_email), message=sub_email, receiver="Admin") 
            n.save()
            return_data = {
                "error": "0",
                "message": 'Thank you for Subscribing! You will be recieving our newsletters henceforth.'
                }
        else:
            return_data = {
                "error":"2",
                "message": "Sorry! You did not enter your email. Try again"
            }
    except Exception as e:
        return_data = {
            "error": "3",
            "message": str(e)
        }
    return render(request,"home.html", return_data)
subscribeapi
# Signout
def signout(request):
    logout(request)
    return render(request,"home.html") 



# update biodata
@api_view(["POST"])
def update_biodata(request):
    try:

        firstName = request.data.get('firstname',None)
        lastName = request.data.get('lastname',None)
        state = request.data.get('state',None)
        phoneNumber = request.data.get('phonenumber',None)
        address = request.data.get('address',None)
        update_field = [firstName,lastName,state,address]
        if not None in update_field and not "" in update_field:
            if WastecoinUser.objects.filter(user =request.user).exists():
                user=User.objects.get(username= phoneNumber)
                User.objects.filter(username= user).update(first_name=firstName, last_name=lastName)
                WastecoinUser.objects.filter(user=user).update(firstname=firstName, lastname=lastName, user_address=address, user_state=state)
                return_data = {
                    "error": "0",
                    "message":"The Biodata Update was successful",
                    "userman": WastecoinUser.objects.filter(user=request.user)
                    }
            else:
                return_data = {
                    "error": "1",
                    "message": "You are not permitted to change anything.",
                    "userman": WastecoinUser.objects.filter(user=request.user)
                }
                    
        else:
            return_data = {
                "error":"2",
                "message": "Invalid Parameter",
                "userman": WastecoinUser.objects.filter(user=request.user)
            }
    except Exception as e:
        return_data = {
            "error": "3",
            "message": str(e),
            "userman": WastecoinUser.objects.filter(user=request.user)
        }
    return render(request,"profile.html", return_data) 

# update agent biodata
@api_view(["POST"])
def update_agent_biodata(request):
    try:

        firstName = request.data.get('firstname',None)
        lastName = request.data.get('lastname',None)
        state = request.data.get('state',None)
        agentid = request.data.get('agentid',None)
        address = request.data.get('address',None)
        update_field = [firstName,lastName,state,address]
        if not None in update_field and not "" in update_field:
            if WastecoinAgent.objects.filter(user =request.user).exists():
                user=User.objects.get(username= agentid)
                User.objects.filter(username= user).update(first_name=firstName, last_name=lastName)
                WastecoinAgent.objects.filter(user=user).update(firstname=firstName, lastname=lastName, user_address=address, user_state=state)
                return_data = {
                    "error": "0",
                    "message":"The Biodata Update was successful",
                    "userman": WastecoinAgent.objects.filter(user=request.user)
                    }
            else:
                return_data = {
                    "error": "1",
                    "message": "You are not permitted to change anything.",
                    "userman": WastecoinAgent.objects.filter(user=request.user)
                }
                    
        else:
            return_data = {
                "error":"2",
                "message": "Invalid Parameter",
                "userman": WastecoinAgent.objects.filter(user=request.user)
            }
    except Exception as e:
        return_data = {
            "error": "3",
            "message": str(e),
            "userman": WastecoinAgent.objects.filter(user=request.user)
        }
    return render(request,"profile_agent.html", return_data)

# update account
@api_view(["POST"])
def update_account(request):
    try:

        accountname = request.data.get('accountname',None)
        accountnumber = request.data.get('accountnumber',None)
        bank = request.data.get('bank',None)
        phoneNumber = request.data.get('phonenumber',None)
        update_field = [accountname,accountnumber,bank,phoneNumber]
        if not None in update_field and not "" in update_field:
            if WastecoinUser.objects.filter(user =request.user).exists():
                user=User.objects.get(username= phoneNumber)
                WastecoinUser.objects.filter(user=user).update(accountname=accountname, accountnumber=accountnumber, bank=bank)
                return_data = {
                    "error": "0",
                    "message":"The Account Update was successful",
                    "userman": WastecoinUser.objects.filter(user=request.user)
                    }
            else:
                return_data = {
                    "error": "1",
                    "message": "You are not permitted to change anything.",
                    "userman": WastecoinUser.objects.filter(user=request.user)
                }
                    
        else:
            return_data = {
                "error":"2",
                "message": "Invalid Parameter",
                "userman": WastecoinUser.objects.filter(user=request.user)
            }
    except Exception as e:
        return_data = {
            "error": "3",
            "message": str(e),
            "userman": WastecoinUser.objects.filter(user=request.user)
        }
    return render(request,"profile.html", return_data) 

# update agent account
@api_view(["POST"])
def update_agent_account(request):
    try:

        accountname = request.data.get('accountname',None)
        accountnumber = request.data.get('accountnumber',None)
        bank = request.data.get('bank',None)
        agentid = request.data.get('agentid',None)
        update_field = [accountname,accountnumber,bank]
        if not None in update_field and not "" in update_field:
            if WastecoinAgent.objects.filter(user =request.user).exists():
                user=User.objects.get(username= agentid)
                WastecoinAgent.objects.filter(user=user).update(accountname=accountname, accountnumber=accountnumber, bank=bank)
                return_data = {
                    "error": "0",
                    "message":"The Account Update was successful",
                    "userman": WastecoinAgent.objects.filter(user=request.user)
                    }
            else:
                return_data = {
                    "error": "1",
                    "message": "You are not permitted to change anything.",
                    "userman": WastecoinAgent.objects.filter(user=request.user)
                }
                    
        else:
            return_data = {
                "error":"2",
                "message": "Invalid Parameter",
                "userman": WastecoinAgent.objects.filter(user=request.user)
            }
    except Exception as e:
        return_data = {
            "error": "3",
            "message": str(e),
            "userman": WastecoinAgent.objects.filter(user=request.user)
        }
    return render(request,"profile_agent.html", return_data) 

# send coin (Agent)
@api_view(["POST"])
def send_coins(request):
    try:
        totalCoins = Coin.objects.filter().order_by('-date_added')[0]
        # amount = request.data.get('amount',None)
        weight = request.data.get('weight',None)
        recipient = request.data.get('recipient',None)
        agentid = request.data.get('agentid',None)
        amount = float(weight)*15
        update_field = [amount,recipient]
        if not None in update_field and not "" in update_field:
            if User.objects.filter(username =request.user).exists():
                payee=User.objects.get(username= recipient)
                user=User.objects.get(username= agentid)
                payeeFirstName =WastecoinUser.objects.get(user=payee).firstname
                payeeLastName =WastecoinUser.objects.get(user=payee).lastname
                AgentWastecoinBalance = float(WastecoinAgent.objects.get(user=user).currentAgentWastecoinBalance)
                UserWastecoinBalance =float(WastecoinUser.objects.get(user=payee).currentUserWastecoinBalance)
                AgentState = WastecoinAgent.objects.get(user=user).user_state
                UserState = WastecoinUser.objects.get(user=payee).user_state
                if AgentWastecoinBalance < float(amount):
                    return_data = {
                    "error": "4",
                     "transaction": Transaction.objects.filter(sender=request.user).order_by('-date_added'),
                     "allocatedWasteCoins": totalCoins,
                    "message":"Sorry! You have exceeded your Current WasteCoin Balance",
                    "userman": WastecoinAgent.objects.filter(user=request.user)
                    }
                if AgentWastecoinBalance == 0:
                    return_data = {
                    "error": "4",
                     "transaction": Transaction.objects.filter(sender=request.user).order_by('-date_added'),
                     "allocatedWasteCoins": totalCoins,
                    "message":"Sorry! You have Zero Wastecoins in your wallet.",
                    "userman": WastecoinAgent.objects.filter(user=request.user)
                    }
                if AgentState != UserState:
                    return_data = {
                    "error": "4",
                     "transaction": Transaction.objects.filter(sender=request.user).order_by('-date_added'),
                     "allocatedWasteCoins": totalCoins,
                     "AgentState": AgentState,
                     "UserState": UserState,
                    "message":"Sorry! You can't send Coins to the recipient!",
                    "userman": WastecoinAgent.objects.filter(user=request.user)
                    }
                else:
                    newAgentWastecoinBalance = AgentWastecoinBalance - float(amount)
                    WastecoinAgent.objects.filter(user=user).update(currentAgentWastecoinBalance=newAgentWastecoinBalance)
                    newUserWastecoinBalance = UserWastecoinBalance + float(amount)
                    WastecoinUser.objects.filter(user=payee).update(currentUserWastecoinBalance=newUserWastecoinBalance)
                    g = Transaction(recipient=recipient, sender=agentid, amount=amount) 
                    g.save()
                    m = minedCoin(miner=recipient, creditedBy=agentid, minedCoin=amount) 
                    m.save()
                    return_data = {
                        "error": "0",
                        "message":str(amount)+" Wastecoin was Successfully sent to "+str(payeeFirstName)+" "+str(payeeLastName),
                        "allocatedWasteCoins": totalCoins,
                         "transaction": Transaction.objects.filter(sender=request.user).order_by('-date_added'),
                        "userman": WastecoinAgent.objects.filter(user=request.user)
                        }
            else:
                return_data = {
                    "error": "1",
                    "message": "You are not authorized to make this transaction.",
                    "allocatedWasteCoins": totalCoins,
                     "transaction": Transaction.objects.filter(sender=request.user).order_by('-date_added'),
                    "userman": WastecoinAgent.objects.filter(user=request.user)
                }
                    
        else:
            return_data = {
                "error":"2",
                "message": "Invalid Parameter",
                "allocatedWasteCoins": totalCoins,
                 "transaction": Transaction.objects.filter(sender=request.user).order_by('-date_added'),
                "userman": WastecoinAgent.objects.filter(user=request.user)
            }
    except Exception as e:
        return_data = {
            "error": "3",
            "message": str(e),
            "allocatedWasteCoins": totalCoins,
             "transaction": Transaction.objects.filter(sender=request.user).order_by('-date_added'),
            "userman": WastecoinAgent.objects.filter(user=request.user)
        }
    return render(request,"wallet_agent.html", return_data)

# redeem coin (user)
@api_view(["POST"])
def redeem_coins(request):
    try:
        totalCoins = Coin.objects.filter().order_by('-date_added')[0]
        amount = request.data.get('amount',None)
        user_state = request.data.get('state',None)
        phonenumber = request.data.get('email',None)
        month = request.data.get('month',None)
        incentive = request.data.get('incentive',None)
        amountExchange = float(amount)*float(totalCoins.exchangeRate)
        update_field = [amount,incentive]
        if not None in update_field and not "" in update_field:
            if User.objects.filter(username =request.user).exists():
                user=User.objects.get(username= request.user)
                payeeFirstName =WastecoinUser.objects.get(user=user).firstname
                payeeLastName =WastecoinUser.objects.get(user=user).lastname
                backAllocatedCoins = float(Coin.objects.get(state=user_state, month=month).backAllocatedCoins)
                UserWastecoinBalance =float(WastecoinUser.objects.get(user=user).currentUserWastecoinBalance)
                if UserWastecoinBalance < float(amount):
                    return_data = {
                    "error": "4",
                     "transaction": Transaction.objects.filter(recipient=request.user).order_by('-date_added'),
                     "allocatedWasteCoins": totalCoins,
                    "message":"Sorry! You have exceeded your Current WasteCoin Balance.",
                    "userman": WastecoinUser.objects.filter(user=request.user)
                    }
                if UserWastecoinBalance == 0:
                    return_data = {
                    "error": "4",
                     "transaction": Transaction.objects.filter(recipient=request.user).order_by('-date_added'),
                     "allocatedWasteCoins": totalCoins,
                    "message":"Sorry! You have Zero Wastecoins. Start to mine already.",
                    "userman": WastecoinUser.objects.filter(user=request.user)
                    }
                else:
                    newUserWastecoinBalance = UserWastecoinBalance - float(amount)
                    newBackAllocatedCoins = backAllocatedCoins + float(amount)
                    Coin.objects.filter(state=user_state, month=month).update(backAllocatedCoins=newBackAllocatedCoins)
                    WastecoinUser.objects.filter(user=user).update(currentUserWastecoinBalance=newUserWastecoinBalance)
                    g = Transaction(recipient="Admin", sender=user, amount=amount) 
                    g.save()
                    m = redeemCoin(miner=user, redeemedCoin=amount, incentive=incentive) 
                    m.save()
                    return_data = {
                        "error": "0",
                        "message":"\u00a3"+str(amountExchange)+" has been approved for payment to "+str(payeeFirstName)+" "+str(payeeLastName),
                        "allocatedWasteCoins": totalCoins,
                         "transaction": Transaction.objects.filter(recipient=request.user).order_by('-date_added'),
                        "userman": WastecoinUser.objects.filter(user=request.user)
                        }
            else:
                return_data = {
                    "error": "1",
                    "message": "You are not authorized to make this transaction.",
                    "allocatedWasteCoins": totalCoins,
                     "transaction": Transaction.objects.filter(recipient=request.user).order_by('-date_added'),
                    "userman": WastecoinUser.objects.filter(user=request.user)
                }
                    
        else:
            return_data = {
                "error":"2",
                "message": "Invalid Parameter",
                "allocatedWasteCoins": totalCoins,
                 "transaction": Transaction.objects.filter(recipient=request.user).order_by('-date_added'),
                "userman": WastecoinUser.objects.filter(user=request.user)
            }
    except Exception as e:
        return_data = {
            "error": "3",
            "message": str(e),
            "allocatedWasteCoins": totalCoins,
             "transaction": Transaction.objects.filter(recipient=request.user).order_by('-date_added'),
            "userman": WastecoinUser.objects.filter(user=request.user)
        }
    return render(request,"wallet.html", return_data)


# transaction agent search 
  
@api_view(["POST"])
def transaction_agent_search(request):
    try:
        totalCoins = Coin.objects.filter().order_by('-date_added')[0]
        from_date = request.data.get('from',None)
        to_date = request.data.get('to',None)
        update_field = [from_date,to_date]
        if not None in update_field and not "" in update_field:
            if User.objects.filter(username =request.user).exists():
                return_data = {
                    "error": "0",
                    "transaction": Transaction.objects.filter(sender=request.user, date_added_normal__gte=from_date, date_added_normal__lte=to_date).order_by('-date_added'),
                    "allocatedWasteCoins": totalCoins,
                    "userman": WastecoinAgent.objects.filter(user=request.user)
                    }

            else:
                return_data = {
                    "error": "1",
                    "message": "You are not authorized to make this Search Query.",
                    "allocatedWasteCoins": totalCoins,
                    "transaction": Transaction.objects.filter(recipient=request.user).order_by('-date_added'),
                    "userman": WastecoinAgent.objects.filter(user=request.user)
                }
                    
        else:
            return_data = {
                "error":"2",
                "message": "Invalid Search Parameter",
                "allocatedWasteCoins": totalCoins,
                 "transaction": Transaction.objects.filter(recipient=request.user).order_by('-date_added'),
                "userman": WastecoinAgent.objects.filter(user=request.user)
            }
    except Exception as e:
        return_data = {
            "error": "3",
            "message": str(e),
            "allocatedWasteCoins": totalCoins,
             "transaction": Transaction.objects.filter(recipient=request.user).order_by('-date_added'),
            "userman": WastecoinAgent.objects.filter(user=request.user)
        }
    return render(request,"wallet_agent.html", return_data)

# trasactions earch user password
@api_view(["POST"])
def transaction_user_search(request):
    try:
        totalCoins = Coin.objects.filter().order_by('-date_added')[0]
        from_date = request.data.get('from',None)
        to_date = request.data.get('to',None)
        update_field = [from_date,to_date]
        if not None in update_field and not "" in update_field:
            if User.objects.filter(username =request.user).exists():
                return_data = {
                    "error": "0",
                    "transaction": Transaction.objects.filter(recipient=request.user, date_added_normal__gte=from_date, date_added_normal__lte=to_date).order_by('-date_added'),
                    "allocatedWasteCoins": totalCoins,
                    "userman": WastecoinUser.objects.filter(user=request.user)
                    }

            else:
                return_data = {
                    "error": "1",
                    "message": "You are not authorized to make this Search Query.",
                    "allocatedWasteCoins": totalCoins,
                    "transaction": Transaction.objects.filter(recipient=request.user).order_by('-date_added')[0:5],
                    "userman": WastecoinUser.objects.filter(user=request.user)
                }
                    
        else:
            return_data = {
                "error":"2",
                "message": "Invalid Search Parameter",
                "allocatedWasteCoins": totalCoins,
                 "transaction": Transaction.objects.filter(recipient=request.user).order_by('-date_added')[0:5],
                "userman": WastecoinUser.objects.filter(user=request.user)
            }
    except Exception as e:
        return_data = {
            "error": "3",
            "message": str(e),
            "allocatedWasteCoins": totalCoins,
             "transaction": Transaction.objects.filter(recipient=request.user).order_by('-date_added')[0:5],
            "userman": WastecoinUser.objects.filter(user=request.user)
        }
    return render(request,"wallet.html", return_data)



# @api_view(["POST"])
# def update_password(request):
#     try:
#         oldpassword = request.data.get('oldpassword',None)
#         newpassword = request.data.get('newpassword',None)
#         newpassword2 = request.data.get('newpassword2',None)
#         phoneNumber = request.data.get('phonenumber',None)
#         updatepass_field = [oldpassword,newpassword,newpassword2,phoneNumber]
#         if not None in updatepass_field and not "" in updatepass_field and newpassword == newpassword2:
#             if WastecoinUser.objects.filter(user =request.user).exists():
#                 user=User.objects.get(username= phoneNumber)
#                 User.objects.filter(username= user).update(password=newpassword)
#                 WastecoinUser.objects.filter(user=user).update(user_password=newpassword)
#                 return_data = {
#                     "error": "0",
#                     "message":"The Password Update was successful",
#                     "userman": WastecoinUser.objects.filter(user=request.user)
#                     }
#             else:
#                 return_data = {
#                     "error": "1",
#                     "message": "You are not permitted to change anything.",
#                     "userman": WastecoinUser.objects.filter(user=request.user)
#                 }
                    
#         else:
#             return_data = {
#                 "error":"2",
#                 "message": "Invalid Parameter",
#                 "userman": WastecoinUser.objects.filter(user=request.user)
#             }
#     except Exception as e:
#         return_data = {
#             "error": "3",
#             "message": str(e),
#             "userman": WastecoinUser.objects.filter(user=request.user)
#         }
#     return render(request,"profile.html", return_data) 
    

    # ADMIN APIS
# newly added
# dashboard view page
def dashboard_admin(request):
    unreadMessages = notifications.objects.filter(receiver=request.user, beenRead ="No").order_by('-date_added').count()
    totalCoins = Coin.objects.filter().order_by('-date_added')[0]
    minedCoins = minedCoin.objects.aggregate(Sum('minedCoin'))
    totalAgents = WastecoinAgent.objects.all().count()
    totalMiners = WastecoinUser.objects.all().count()
    redeemRequests = redeemCoin.objects.all().count()
    totalMessages = notifications.objects.all().count()
   
    return_data = {
        "user":request.user,
        "unreadMsg": unreadMessages,
        "allocatedWasteCoins": totalCoins,
        "minedCoins": minedCoins,
        "userman": User.objects.filter(username=request.user),
        "totalMiners": totalMiners, 
        "totalAgents": totalAgents, 
        "redeemRequests": redeemRequests, 
        "totalMessages": totalMessages,
        }
    return render(request,"dashboard_admin.html", return_data) 
    # dashboard query
@api_view(["POST"])
def dashboard_search_query(request):

    from_date = request.data.get('from',None)
    to_date = request.data.get('to',None)
    search_state = request.data.get('state',None)
    # transaction_list = Transaction.objects.filter(Q(recipient=request.user) | Q(sender=request.user)).order_by('-date_added')
    # minedCoins = minedCoin.objects.filter(state=search_state).aggregate(Sum('minedCoin'))
    # allocatedWasteCoins = Coin.objects.filter(state=search_state).order_by('-date_added')[0]
    totalCoins = Coin.objects.filter(state=search_state).aggregate(Sum('allocatedCoins'))
    # totalCoins = Coin.objects.filter(Q(state=search_state) | Q(date_added_normal__gte=from_date)| Q(date_added_normal__lte=to_date)).aggregate(Sum('allocatedCoins'))

    # unreadMessages = notifications.objects.filter(receiver=request.user, beenRead ="No").order_by('-date_added').count()
    totalAgents = WastecoinAgent.objects.all().count()
    totalMiners = WastecoinUser.objects.all().count()
    redeemRequests = redeemCoin.objects.all().count()
    totalMessages = notifications.objects.all().count()
    return_data = {
        # "user":request.user,
        # "unreadMsg": unreadMessages,
        # "allocatedWasteCoins": allocatedWasteCoins,
        # "minedCoins": minedCoins,
        # "userman": User.objects.filter(username=request.user),
        "totalMiners": totalMiners, 
        "totalCoins": totalCoins,
        "totalAgents": totalAgents, 
        "From": from_date,
        "To": to_date,
        "redeemRequests": redeemRequests, 
        "totalMessages": totalMessages,
        }
    return render(request,"dashboard_admin.html", return_data) 

    #     update_field = [from_date,to_date]
    #     if not None in update_field and not "" in update_field:
    #         if User.objects.filter(username =request.user).exists():
    #             return_data = {
    #                 "error": "0",
    #                 "transaction": Transaction.objects.filter(recipient=request.user, date_added_normal__gte=from_date, date_added_normal__lte=to_date).order_by('-date_added'),
    #                 "allocatedWasteCoins": totalCoins,
    #                 "userman": WastecoinUser.objects.filter(user=request.user)
    #                 }

    #         else:
    #             return_data = {
    #                 "error": "1",
    #                 "message": "You are not authorized to make this Search Query.",
    #                 "allocatedWasteCoins": totalCoins,
    #                 "transaction": Transaction.objects.filter(recipient=request.user).order_by('-date_added')[0:5],
    #                 "userman": WastecoinUser.objects.filter(user=request.user)
    #             }
                    
    #     else:
    #         return_data = {
    #             "error":"2",
    #             "message": "Invalid Search Parameter",
    #             "allocatedWasteCoins": totalCoins,
    #              "transaction": Transaction.objects.filter(recipient=request.user).order_by('-date_added')[0:5],
    #             "userman": WastecoinUser.objects.filter(user=request.user)
    #         }
    # except Exception as e:
    #     return_data = {
    #         "error": "3",
    #         "message": str(e),
    #         "allocatedWasteCoins": totalCoins,
    #          "transaction": Transaction.objects.filter(recipient=request.user).order_by('-date_added')[0:5],
    #         "userman": WastecoinUser.objects.filter(user=request.user)
    #     }
    # return render(request,"dashboard_admin", return_data)
