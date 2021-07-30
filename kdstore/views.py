from django.db.models.fields import related
from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import context
from .models import Product, Checkout, Contact, ProductComment, ProductRating, Offer, Order
from Paytm import Checksum
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from math import ceil
import datetime

MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'



def index(request):
    allprods =[]
    offers = []
    offerList = []
    offer = Offer.objects.all()
    offerLen = len(offer)
    for i in offer:
        offerList.append((i))
    offers.append([offerList, range(1, offerLen)])
    mobiles = Product.objects.filter(category='Mobiles')[0:4]
    electronics = Product.objects.filter(category='Electronics')[0:4]
    appliances = Product.objects.filter(category='Appliances')[0:4]
    fashions = Product.objects.filter(category='Fashion')[0:4]
    allprods.append((mobiles))
    allprods.append((electronics))
    allprods.append((appliances))
    allprods.append((fashions))

    productsInfo = []
    product =[]
    for products in allprods:
        for item in products:
            rating = ProductRating.objects.filter(product=item)
            totalRate = 0
            rates = 0
            total = 0
            for i in rating:
                totalRate += 1
                rates = rates + i.rate
                total = rates / totalRate   
            productsInfo.append([item, total, totalRate])
    mobile = productsInfo[0:4]
    electronic = productsInfo[4:8]
    appliance = productsInfo[8:12]
    fashion = productsInfo[12:16]
    product.append((mobile))
    product.append((electronic))
    product.append((appliance))
    product.append((fashion))
    context = {'product': product, 'offers': offers}
    return render(request, 'kdstore/index.html', context)

def loginPage(request):
    return render(request, 'kdstore/loginPage.html')

def userLogin(request):
    if request.method == 'POST':
        myusername = request.POST['loginusername']
        mypassword = request.POST['loginpassword']

        user = authenticate(username= myusername, password=mypassword)

        if user is not None:
            login(request, user)
            messages.info(request, 'You are successfully logged in')
            return redirect('/')
        
        else:
            messages.info(request, 'Invalid credential')
            return redirect('loginPage')

    else:
        return HttpResponse('404-PAGE NOT FOUND')

def signUpPage(request):
    return render(request, 'kdstore/signUpPage.html')

def signUp(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstName = request.POST['fname']
        lastName = request.POST['lname']
        email = request.POST['email']
        password1 = request.POST['pass1']
        password2 = request.POST['pass2']

        if password1!=password2:
            messages.info(request, 'Password1 and Password2 are different')
            return redirect('signUpPage')

        elif User.objects.filter(username=username).exists():
            messages.info(request, 'This username already exist')
            return redirect('signUpPage')

        else:
            users = User.objects.create_user(username=username, password=password1, email=email, first_name=firstName, last_name=lastName)
            users.save()
            messages.info(request, 'Your KDstore account is successfully created')
            return redirect('/')
    else:
        return HttpResponse('404-page NOT FOUND')

def userLogout(request):
    logout(request)
    messages.info(request, "successfully loggedout")
    return redirect('/')

def userProfile(request):
    user = request.user
    userOrder = Checkout.objects.filter(user=user)
    orderNo = len(userOrder)
    context = {'userOrder': userOrder, 'orderNo': orderNo}
    return render(request, 'kdstore/userProfile.html', context)  

@login_required(login_url='loginPage')
def editProfilePage(request):
    user = request.user
    return render(request, 'kdstore/editProfilePage.html')


def products(request):
    products = []
    fcategory = Product.objects.values('category', 'id')
    fcats = {item['category'] for item in fcategory}
    for items in fcats:
        product = []
        prod = Product.objects.filter(category=items)
        n = len(prod)
        slides = n // 4 + ceil((n / 4) - (n // 4))
        for item in prod:
            rating = ProductRating.objects.filter(product=item)
            totalRate = 0
            rates = 0
            total = 0
            for i in rating:
                totalRate += 1
                rates = rates + i.rate
                total = rates / totalRate
            product.append([item, total, totalRate])
        products.append([product, range(1, slides), slides])
    params = {'products':products}
    return render(request, 'kdstore/products.html', params) 

def categoryProduct(request, category):
    categoryProduct = Product.objects.filter(category=category)
    n =len(categoryProduct)
    slides = n//4 + ceil((n/4)-(n//4))
    product = []
    products = []
    category = ""
    for item in categoryProduct:
        rating = ProductRating.objects.filter(product=item)
        category == item.category
        totalRate = 0
        rates = 0
        total = 0
        for i in rating:
            totalRate += 1
            rates = rates + i.rate
            total = rates / totalRate
        product.append([item, total, totalRate])
    products.append([product, range(1, slides), slides])

    return render(request, f'kdstore/productcat.html/{category}', {'products': products})


def editProfile(request):
    if request.method=="POST":
        user = request.user
        username = request.POST['username']
        firstName = request.POST['fname']
        lastName = request.POST['lname']
        email = request.POST['email']
        
        if User.objects.filter(username=username).exists():
            messages.info(request, 'This username already exist...')
            return redirect('editProfilePage')
        else:
            user.email = email
            user.username = username
            user.first_name = firstName
            user.last_name = lastName
            user.save()
            return redirect('userProfile')

def about(request):
    return render(request, "kdstore/about.html")

@login_required(login_url='loginPage')
def contactUs(request):
    if request.method == "POST":
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            subject = request.POST.get('subject', '')
            message = request.POST.get('message', '')
            contact = Contact(name=name, email=email, phone=phone, subject=subject, message=message)
            contact.save()
            messages.info(request, 'Your message is succesfully send...')
            return render(request, 'kdstore/contactUs.html')
    else:
        return render(request, 'kdstore/contactUs.html')


def productInfo(request, myid):
    prodInfo = Product.objects.filter(id=myid).first()
    comments = ProductComment.objects.filter(product=prodInfo, parent=None)
    replies = ProductComment.objects.filter(product=prodInfo).exclude(parent=None)
    rating = ProductRating.objects.filter(product=prodInfo)
    totalRate = 0
    rates = 0
    total = 0
    for i in rating:
        totalRate += 1
        rates = rates + i.rate
        total = rates / totalRate
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)   
    context = {'prodInfo':prodInfo, 'comments':comments, 'replyDict':replyDict, 'total':total, 'totalRate':totalRate}  
    return render(request, 'kdstore/prodInfo.html/', context)


def productComment(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        productSno = request.POST.get('productSno')
        product = Product.objects.get(id=productSno)
        parentSno = request.POST.get('parentSno')
        if parentSno == "":
            comment = ProductComment(comment=comment, user=user, product=product)
            comment.save()
            messages.success(request, 'your comment has been posted successfully')
        else:
            parent = ProductComment.objects.get(sno=parentSno)
            comment=ProductComment(comment= comment, user=user, product=product , parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")

    return redirect(f'/product/{product.id}')

def moreComments(request, myid):
    prodInfo = Product.objects.filter(id=myid).first()
    comments = ProductComment.objects.filter(product=prodInfo, parent=None)
    return render(request, 'kdstore/moreComments.html/', {'prodInfo': prodInfo,'comments': comments})

def productRating(request):
    if request.method == "POST":
        user = request.user
        productId = request.POST.get('productId')
        rating = request.POST.get('rating')
        product = Product.objects.get(id=productId)
        tempRate = ProductRating.objects.filter(user=user, product = product)
        if tempRate.exists():
            tempRate.update(rate = rating)
            messages.info(request, 'your rating updated')
        else:
            productRating = ProductRating(user = user, product = product, rate = rating)
            productRating.save()
            messages.info(request, 'Thanks for rating')
            
        return redirect('/userProfile/')

def offers(request):
    allOffer = Offer.objects.all()
    offers = []
    for i in allOffer:
        offers.append((i))
    return render(request, 'kdstore/offers.html', {'offers':offers})

def search(request):
    query = request.GET.get('search')
    allSearch = []
    fcategory = Product.objects.values('category', 'id')
    fcats = {item['category'] for item in fcategory}
    for fcat in fcats:
        sprod = Product.objects.filter(category=fcat)
        products=[]
        for item in sprod:
            if searchMatch(query,item):
                rating = ProductRating.objects.filter(product = item)
                totalRate = 0
                rates = 0
                total = 0
                for i in rating:
                    totalRate += 1
                    rates = rates + i.rate
                    total = rates / totalRate
                products.append([item, total, totalRate])
        n = len(products)
        slides = n // 4 + ceil((n / 4) - (n // 4))
        allSearch.append([products, range(1, slides), n, slides])
    params = {'allSearch': allSearch}
    if len(products) == 0 or len(query)<4:
        messages.info(request, "please enter relevent item...")
    return render(request, 'kdstore/search.html', params)

def searchMatch(query, item):
    if str(query) in item.description.lower() or str(query) in item.product_name.lower() or str(query) in item.category.lower() or str(query) in item.subcategory.lower() or str(query) in item.brand.lower():
        return True
    elif str(query) in item.description.capitalize() or str(query) in item.product_name.capitalize() or str(query) in item.category.capitalize() or str(query) in item.subcategory.capitalize() or str(query) in item.brand.capitalize():
        return True
    elif str(query) in item.description.upper() or str(query) in item.product_name.upper() or str(query) in item.category.upper() or str(query) in item.subcategory.upper() or str(query) in item.brand.upper():
        return True
    else:
        return False

def cart(request):
    return render(request, 'kdstore/cart.html')

@login_required(login_url='loginPage')
def checkout(request):
    if request.method=='POST':
        return render(request, 'kdstore/checkout.html')
    else:
        return HttpResponse('NOT VALID PAGE')

@login_required(login_url='loginPage')
def order(request):
    if request.method == 'POST':
        user = request.user
        amount = request.POST['amount']
        orderItem = request.POST['orderItem']
        email = request.POST['email']
        address = request.POST['address']
        phoneNo = request.POST['phoneNo']
        state = request.POST['state']
        zip1 = request.POST['zip']
        a = datetime.datetime.now()
        b = str(a)
        # c = b[0:4]
        d = b[5:7]
        e = b[8:10]
        f = b[11:13]
        g = b[14:16]
        h = b[17:19]
        orderId = d+e+f+g+h

        order = Checkout(user=user, email=email, address=address, phone=phoneNo, zip_code=zip1, amount=amount, orderItem=orderItem, state=state, orderId= orderId)
        order.save()
        id = order.orderId
        param_dict = {
                    'MID': 'WorldP64425807474247',
                    'ORDER_ID': str(order.orderId),
                    'TXN_AMOUNT': str(amount),
                    'CUST_ID': email,
                    'INDUSTRY_TYPE_ID': 'Retail',
                    'WEBSITE': 'WEBSTAGING',
                    'CHANNEL_ID': 'WEB',
                    'CALLBACK_URL': 'http://127.0.0.1:8000/payment-request/',

                }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'kdstore/paytm.html', {'param_dict': param_dict})
    else:
        return HttpResponse('PAGE IS NOT VALID')

@csrf_exempt
def paymentRequest(request):
    response = request.POST
    response_info = {}
    for i in response.keys():
        response_info[i] = response[i]
        if i=='CHECKSUMHASH':
            checksum = response[i]

    checksumVerify = Checksum.verify_checksum(response_info, MERCHANT_KEY, checksum)
    if checksumVerify:
        orderid = response_info['ORDERID']
        if response_info['RESPCODE'] == '01':
            messages.info(request, 'Order Successfull')
            orderCreate = Checkout.objects.filter(orderId=orderid).first()
            order = Order(order=orderCreate)
            order.save()

        else:
            messages.error(request, 'Order Fail')

    return render(request, 'kdstore/paymentStatusInfo.html', {'response_info': response_info})