from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.db import connection
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.db.models import Q

import razorpay
import qrcode
import io
from django.views.decorators.csrf import csrf_exempt

def base(r):
    return render(r,'base.html')

def adbase(r):
    return render(r,'adbase.html')

def chckcart(usr):
    re=cart.objects.filter(user_details__name=usr)
    length=len(re)
    return length

def index1(r):
    return render(r,'index1.html')
    
def index(r):
    return render(r,'index.html')

def adindex(r):
    return render(r,'adindex.html')

def aboutus(r):
    return render(r,'aboutus.html')

def frreg(r):
    if r.method=="POST":
        name=r.POST.get('name')
        address=r.POST.get('adrs')
        phonenumber=r.POST.get('phno')
        bankname=r.POST.get('bn')
        accountnumber=r.POST.get('acn')
        ifsccode=r.POST.get('ic')  
        username=r.POST.get('un')  
        password=r.POST.get('pwd')  
        email=r.POST.get('email')
        image=r.FILES.get('img') 
        flicense=r.FILES.get('fimg')       
        if farmer.objects.filter(username=username).exists():
                messages.info(r,f'Farmer {username} is already exist...')
                return redirect(frreg)
        elif farmer.objects.filter(email=email).exists():
            messages.info(r,f'Farmer with email - {email} is already exists...')
            return redirect(frreg)
        else:
                obj=farmer.objects.create(name=name,address=address,phonenumber=phonenumber,bankname=bankname,
                    accountnumber=accountnumber,ifsccode=ifsccode,username=username,password=password,email=email,image=image,flicense=flicense)
                obj.save()
    return render(r,'farmreg.html')

def usrreg(r):
    if r.method=="POST":
        name=r.POST.get('name')
        address=r.POST.get('adrs')
        phonenumber=r.POST.get('phno')
        bankname=r.POST.get('bn')
        accountnumber=r.POST.get('acn')
        ifsccode=r.POST.get('ic')  
        username=r.POST.get('un')  
        password=r.POST.get('pwd') 
        email=r.POST.get('email') 
        image=r.FILES.get('img')       
        if user.objects.filter(username=username).exists():
                messages.info(r,f'user {username} is already exist...')
                return redirect(usrreg)
        else:
                obj=user.objects.create(name=name,address=address,phonenumber=phonenumber,bankname=bankname,
                    accountnumber=accountnumber,ifsccode=ifsccode,username=username,password=password,email=email,image=image)
                obj.save()
    return render(r,'usrreg.html')

def contact(r):
    if 'user' in r.session:
        length=chckcart(r.session['user']['name'])
        usrdetail=user.objects.get(name=r.session['user']['name'])
        re=farmer.objects.filter(status=1)
        if r.method=='POST':
            message=r.POST.get('mesg')
            frname=r.POST.get('farmer')
            frobj=farmer.objects.get(username=frname)
            contact=cont.objects.create(usrdetail=usrdetail,message=message,frdetail=frobj)
            contact.save()
        return render(r,'contact-us.html',{'usrdetail':usrdetail,'st':re,'length':length})
    return render(r,'contact-us.html')

def adlog(r):
    if r.method=='POST':
        un=r.POST.get('n')
        pw=r.POST.get('no')
        print("HELLO",un,pw)
        if un=='admin':
            if pw=='1234':
                r.session['usr']=un
                print(r.session['usr'])
                
                return redirect(adindex)
            else:
                 messages.info(r,f'Wrong Password....')
                 return redirect(adlog)
        else:
            messages.info(r,f'Invalid Username...') 
    return render(r,'adlog.html')

def frview(r):
    re=farmer.objects.all()
    return render(r,'frview.html',{'st':re})

def usrview(r):
    re=user.objects.all()
    return render(r,'usrview.html',{'st':re})

def adlogout(r):
      if 'usr' in r.session:
            r.session.flush()
            return redirect(index1)

def farmlog(r):
    if r.method=='POST':
            un=r.POST.get('un')
            pw=r.POST.get('pwd')
            if farmer.objects.filter(username=un).exists():
                fmr=farmer.objects.get(username=un)
                if fmr.status==0:
                    messages.info(r,'not approved...')
                    return redirect(farmlog)
                elif fmr.status==1:

                    if fmr.password==pw:
                            r.session['farmer']={'name':fmr.name,'address':fmr.address,'phonenumber':fmr.phonenumber,'bankname':fmr.bankname,'accountnumber':fmr.accountnumber,'ifsccode':fmr.ifsccode,'username':fmr.username,'password':fmr.password,'email':fmr.email}
                            if 'farmer' in r.session:
                                    print("farmer",r.session['farmer']['name'],r.session['farmer']['address'])
                                    messages.info(r,'Login Successfully...')
                            return redirect(frindex)
                    else:
                            messages.info(r,'Wrong Password...')
                            return redirect(farmlog)
                else:
                    messages.info(r,'rejected...')
                    return redirect(farmlog)

            else:
                messages.info(r,'Invalid Username...')
    return render(r,'farmlog.html')

def forgotfarm(r):
    if r.method == 'POST':
        email = r.POST.get('email')
        try:
            farm = farmer.objects.get(email=email)
        except:
            messages.info(r,"Email id not registered")
            return redirect(forgotfarm)
        token = get_random_string(length=4)
        print(token)
        PasswordResetFarm.objects.create(farm=farm, token=token)

        reset_link = f'http://127.0.0.1:8000/resetfarm/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}','settings.EMAIL_HOST_USER', [email],fail_silently=False)
        except:
            messages.info(r,"Network connection failed")
            return redirect(forgotfarm)

    return render(r, 'forgotfarm.html')

def reset_passwordfarm(request, token):
    print(token)
    password_reset = PasswordResetFarm.objects.get(token=token)
    usr = farmer.objects.get(id=password_reset.farm.id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            farm.password = new_password
            farm.save()
            
            return redirect(farmlog)
    return render(request, 'reset_passwordfarm.html',{'token':token})

def frlogout(r):
      if 'farmer' in r.session:
            r.session.flush()
            return redirect(index1)
    
def usrlog(r):
    if r.method=='POST':
        un=r.POST.get('un')
        pw=r.POST.get('pwd')
        if user.objects.filter(username=un).exists():
                usr=user.objects.get(username=un)
                if usr.password==pw:
                    r.session['user']={'name':usr.name,'address':usr.address,'phonenumber':usr.phonenumber,
                                    'bankname':usr.bankname,'accountnumber':usr.accountnumber,'ifsccode':usr.ifsccode,'username':usr.username,'password':usr.password,'email':usr.email}
                    if 'user' in r.session:
                        # messages.info(r,'Login Successfully...')
                        return redirect(usrindex)
                else:
                    messages.info(r,'Wrong Password...')
                    return redirect(usrlog)
        else:
            messages.info(r,'Invalid Username...')
    return render(r,'usrlog.html')

def forgotusr(r):
    if r.method == 'POST':
        email = r.POST.get('email')
        try:
            usr = user.objects.get(email=email)
        except:
            messages.info(r,"Email id not registered")
            return redirect(forgotusr)
        token = get_random_string(length=4)
        print(token)
        PasswordResetUsr.objects.create(usr=usr, token=token)

        reset_link = f'http://127.0.0.1:8000/resetuser/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}','settings.EMAIL_HOST_USER', [email],fail_silently=False)
        except:
            messages.info(r,"Network connection failed")
            return redirect(forgotusr)

    return render(r, 'forgotusr.html')

def reset_passworduser(request, token):
    print(token)
    password_reset = PasswordResetUsr.objects.get(token=token)
    usr = user.objects.get(id=password_reset.usr.id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            usr.password = new_password
            usr.save()
            
            return redirect(usrlog)
    return render(request, 'reset_passworduser.html',{'token':token})

def usrlogout(r):
      if 'user' in r.session:
            r.session.flush()
            return redirect(index1)

def gallery(r):
    return render(r,'gallery.html')

def account(r):
    if 'user' in r.session:
        length=chckcart(r.session['user']['name'])
    return render(r,'account.html',{'length':length})

def checkout(r):
    if 'user' in r.session:
        length=chckcart(r.session['user']['name'])
        uc=user.objects.get(name=r.session['user']['name'])
        re=cart.objects.filter(user_details__name=r.session['user']['name'])
        total=[]
        for i in re:
            total.append(i.tprice)
        tot=sum(total)
        # print(r.session['user']['name'])
        return render(r,'checkout.html',{'up':re,'uc':uc,'tot':tot,'length':length})
    else:
        return redirect(checkout)
    # return render(r,'checkout.html')

def frbase(r):
    return render(r,'frbase.html')

def frindex(r):
    return render(r,'frindex.html')

def usrbase(r):
    return render(r,'usrbase.html')

def usrindex(r):
    if 'user' in r.session:
        length=chckcart(r.session['user']['name'])
    return render(r,'usrindex.html',{'length':length})

def adpro(r):
      if r.method=="POST":
            name=r.POST.get('name')
            description=r.POST.get('des')
            price=r.POST.get('price')
            image=r.FILES.get('img')
            stock=r.POST.get('stock')
            frname=farmer.objects.get(username=r.session['farmer']['username'])
            obj=addproduct.objects.create(name=name,description=description,price=price,image=image,frname=frname,stock=stock)
            obj.save()
            # return redirect(display)
      return render(r,'adpro.html')

def mngpro(r):
    display=farmer.objects.get(username=r.session['farmer']['username'])
    re=addproduct.objects.filter(frname=display)
    return render(r,'mngpro.html',{'st':re})

def edit(r,id):
    if 'farmer' in r.session:
        data=addproduct.objects.get(pk=id)
        m=mform(instance=data)
        if r.method=='POST':
            m=mform(r.POST,r.FILES,instance=data)
            print("hello")
            if m.is_valid():
                m.save()
                print("saved")
                return redirect(mngpro)                
        return render(r,'edit.html',{'data':m})
    return redirect(farmlog)

def delete(r,id):
    if 'farmer' in r.session:
        data=addproduct.objects.get(pk=id)
        data.delete()
        messages.success(r,'Deleted Successfully...')
        return redirect(mngpro)
    else:
        return redirect(farmlog)

def usrdisplay(r):
    length=chckcart(r.session['user']['name'])
    itms=[]
    re=addproduct.objects.all()
    citm=cart.objects.filter(user_details__username=r.session['user']['username'])
    for pro in re:
        for it in citm:
            if pro.name==it.cartitm.name:
                print("pro",pro.name,"CItm",it.cartitm.name)
                itms.append(pro.name)
    return render(r,'usrdisplay.html',{'st':re,'citm':citm,'itms':itms,'length':length})

def usrdisplay2(r,id):
    itms=[]
    length=chckcart(r.session['user']['name'])
    re=addproduct.objects.get(pk=id)
    citm=cart.objects.filter(user_details__username=r.session['user']['username'])
    print("ITEM",re)
    for it in citm:
        itms.append(it.cartitm.name)
        print('citm..',citm,itms)
    return render(r,'usrdisplay2.html',{'i':re,'citm':citm,'itms':itms,'length':length})

def addtocart(r,id):
    if 'user' in r.session:
        user_details=user.objects.get(name=r.session['user']['name'])
        itm=addproduct.objects.get(pk=id)
        if cart.objects.filter(cartitm=itm,user_details=user_details).exists():
            citm=cart.objects.get(user_details=user_details,cartitm=itm)
            citm.tprice=citm.tprice+itm.price
            citm.count=citm.count+1
            citm.save()
            return redirect(usrdisplay)
        else:
            citm=cart.objects.create(user_details=user_details,cartitm=itm)
            print(citm)
            citm.tprice=citm.tprice+itm.price
            citm.count=citm.count+1
            itm.save()
            citm.save()
            return redirect(usrdisplay)
    else:
        return redirect(usrlog)

def mycart(r):
    if 'user' in r.session:
        length=chckcart(r.session['user']['name'])
        if length==0:
            messages.info(r,'Empty Cart...')
            return redirect(empty)
        else:
            pp=addproduct.objects.all()
            re=cart.objects.filter(user_details__name=r.session['user']['name'])
            total=[]
            for i in re:
                total.append(i.tprice)
            print(re)
            tot=sum(total)
            print(r.session['user']['name'])
            return render(r,'mycart.html',{'st':re,'tot':tot,'length':length})
    else:
        return redirect(usrindex)

def empty(r):
    return render(r,'empty.html')

def minuscart(r,id):
    if 'user' in r.session:
        c=cart.objects.get(pk=id)
        if c.count>1:
            c.count = c.count - 1
            c.tprice=c.cartitm.price*c.count
            c.save()
        else:
            c.delete()
    return redirect(mycart)

def pluscart(r,id):
    if 'user' in r.session:
        c=cart.objects.get(pk=id)
        c.count = c.count + 1
        c.tprice=c.cartitm.price*c.count
        c.save()
    return redirect(mycart)

def delete_c(r,id):
    datas=cart.objects.get(pk=id)
    print(datas)
    datas.delete()
    return redirect(mycart)


def search(r):
    if r.method=='POST':
        s=r.POST.get('srch')
        re=addproduct.objects.filter(name=s)
        re=addproduct.objects.filter(name__icontains=s)
        #   re=product.objects.filter(Q(code=s) | Q(price=s))
        print(len(re))
    return render(r,'usrdisplay.html',{'st':re})   

def approve(r,id):
    if 'usr'in r.session:
        farmer.objects.filter(id=id).update(status=1)
        messages.success(r,'Approved Successfully...')
        return redirect(frview)
    else:
        return redirect(adindex)

def cancel(r,id):
    if 'usr' in r.session:
        farmer.objects.filter(id=id).update(status=2)
        # data=farmer.objects.get(id=id)
        # data.delete()
        messages.success(r,'Deleted Successfully...')
        return redirect(frview)
    else:
        return redirect(adindex)

def msg(r):
    if 'user' in r.session:
        length=chckcart(r.session['user']['name'])
        udetail=user.objects.get(name=r.session['user']['name'])
        re=farmer.objects.filter(status=1)
        if r.method=='POST':
            comment=r.POST['cmt']
            fname=r.POST['farmer']
            fobj=farmer.objects.get(username=fname)
            data=feedback.objects.create(comment=comment,udetail=udetail,fdetail=fobj)
            data.save()
        return render(r,'msg.html',{'udetail':udetail,'st':re,'length':length})
    return redirect(usrindex)

def fmsg(r):
    display=farmer.objects.get(username=r.session['farmer']['username'])
    data=feedback.objects.filter(fdetail=display)
    return render(r,'fmsg.html',{'data':data})

def admsg(r):
    re=feedback.objects.all()
    return render(r,'admsg.html',{'st':re})

def adcon(r):
    re=cont.objects.all()
    return render(r,'adcon.html',{'st':re})

def buynow(r,id):
    if 'user' in r.session:
        userdetails=user.objects.get(name=r.session['user']['name'])
        pp=addproduct.objects.get(pk=id)
        #re=buy.objects.filter(userdetails__name=r.session['user']['name'])
        bitm=buy.objects.create(userdetails=userdetails,buyitm=pp)
        bitm.totprice=bitm.totprice+pp.price
        bitm.qty=bitm.qty+1
        pp.save()
        bitm.save()
        return redirect(mybuy,bitm.id)
    else:
        return redirect(usrdisplay)
       
def mybuy(r,id):
    if 'user' in r.session:
        length=chckcart(r.session['user']['name'])
        uu=user.objects.get(name=r.session['user']['name'])
        re=buy.objects.filter(userdetails__name=r.session['user']['name'])
        pp=buy.objects.get(pk=id)
        total=[]
        # for i in re:
        #     total.append(i.totprice)
        # print(re)
        # tot=sum(total)
        print(r.session['user']['name'])
        return render(r,'buynow.html',{'i':pp,'uu':uu,'length':length})
    else:
        return redirect(usrindex)

def plusbuy(r,id):
    if 'user' in r.session:
        p=buy.objects.get(pk=id)
        p.qty = p.qty+ 1
        p.totprice=p.buyitm.price*p.qty
        p.save()
    return redirect(mybuy,p.id)

def minusbuy(r,id):
    if 'user' in r.session:
        p=buy.objects.get(pk=id)
        if p.qty>1:
            p.qty = p.qty- 1
            p.totprice=p.buyitm.price*p.qty
            p.save()
        else:
            p.delete()
    return redirect(mybuy,p.id)

def rlyusr(r,id):
    obj=cont.objects.get(pk=id)
    if r.method=='POST':
        comment=r.POST['cmt']
        name=r.POST['name']
        email=r.POST['email']
        replay=rply.objects.create(name=name,email=email,comment=comment)
        replay.save()
        try:
            send_mail('Replay to user',f'{comment}','settings.EMAIL_HOST_USER',[email],fail_silently=False)
        except Exception as E:
            print("Error",E)
            # return render(r,'rlyusr.html',{'alert':alert})
    return render(r,'rlyusr.html',{'obj':obj})

def adshare(r,id):
    obj=cont.objects.get(pk=id)
    if r.method=='POST':
        fmail=r.POST['fmail']
        comment=r.POST['cmt']
        name=r.POST['name']
        email=r.POST['email']
        phonenumber=r.POST['num']
        # replay=rply.objects.create(name=name,email=email,comment=comment)
        # replay.save()
        try:
            send_mail('Message forward to farmer..',f'{comment}','settings.EMAIL_HOST_USER',[fmail],fail_silently=False)
        except Exception as E:
            print("Error",E)
            # return render(r,'rlyusr.html',{'alert':alert})
    return render(r,'adshare.html',{'obj':obj})

def prodisp(r):
    re=addproduct.objects.all()
    return render(r,'prodisp.html',{'st':re})

def edt(r,id):
    if 'user' in r.session:
        length=chckcart(r.session['user']['name'])
        data=user.objects.get(pk=id)
        m=myform(instance=data)
        if r.method=='POST':
            m=myform(r.POST,r.FILES,instance=data)
            if m.is_valid():
                m.save()
                print("saved",m)
                return redirect(myacc)  
        return render(r,'edt.html',{'data':m,'length':length})
    return redirect(account)

def myacc(r):
    if 'user' in r.session:
        length=chckcart(r.session['user']['name'])
        uu=user.objects.get(name=r.session['user']['name'])
        return render(r,'myacc.html',{'uu':uu,'length':length})

def order(r):
    length=chckcart(r.session['user']['name'])
    re=user.objects.get(username=r.session['user']['username'])
    data=Payment.objects.filter(usrdetail=re)
    data1=cartpayment.objects.filter(cartuser=re)
    return render(r,'order.html',{'pay':data,'ca':data1,'length':length})

def adpay(r):
    spay=Payment.objects.all()
    mpay=cartpayment.objects.all()
    return render(r,'adpay.html',{'spay':spay,'mpay':mpay})

def fpay(r):
    display=farmer.objects.get(username=r.session['farmer']['username'])
    data1=Payment.objects.filter(product__frname__username=r.session['farmer']['username'])
    data2=frorder.objects.filter(fruname=display)
    return render(r,'fpay.html',{'data1':data1,'data2':data2})

def delivery(r,id):
    if 'farmer'in r.session:
        order=Payment.objects.get(id=id)
        if r.method=='POST':
            status=r.POST.get('status')
            order.deliverystatus=status
            print("HELLO-1",order.deliverystatus)
            order.save()
            print("HELLO-2",order.deliverystatus)
            print('orderrrrr',order)
        return redirect(fpay)
    return render(r,'fpay.html',{'order':order})

def deliveries(r,id):
    if 'farmer'in r.session:
        order=frorder.objects.get(id=id)
        
        if r.method=='POST':
            status=r.POST.get('status')
            
            order.deliverystatus=status
            print("HELLO-1",order.deliverystatus)
            order.save()
            crtpay=cartpayment.objects.filter(fremail=r.session['farmer']['email'],pdctdetails=order.pitm).first()
            crtpay.status=order.deliverystatus
            crtpay.save()
            print(crtpay,crtpay.status)
            print("HELLO-2",order.deliverystatus)
            print('orderrrrr',order)
        return redirect(fpay)
    return render(r,'fpay.html',{'order':order})

client = razorpay.Client(auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))

def create_payment(request):
    if 'user' in request.session:
        obj=user.objects.get(name=request.session['user']['name'])
        
        if request.method == 'POST':
            location=request.POST.get('location')
            pincode=request.POST.get('pincode')

            rpamount = int(request.POST['amount'])  # Razorpay amount in paisa
            pdctid=int(request.POST['pdctid'])
            print(pdctid)
            amount=rpamount*100
            print("AMOUNT",amount)
            # payment = Payment.objects.create(amount=rpamount,usrdetail=obj,location=location,pincode=pincode)
            razorpay_order = client.order.create(dict(amount=amount, currency='INR', payment_capture='1'))
            # payment.order_id = razorpay_order['id']
            request.session['payment']={'amount':rpamount,'location':location,'pincode':pincode,'order_id':razorpay_order['id'],'pdctid':pdctid}
            # payment.save()
            
            # Generate QR code for the payment link
            payment_url = f"https://api.razorpay.com/v1/checkout/embedded?order_id={razorpay_order['id']}&key_id=WIWYANkTTLg7iGbFgEbwj4BM"
            qr = qrcode.make(payment_url)
            buffer = io.BytesIO()
            qr.save(buffer, format="PNG")
            buffer.seek(0)
            qr_image = buffer.getvalue()

            context = {
                'qr_image': qr_image,
                'razorpay_order_id': razorpay_order['id'],
                'razorpay_key_id': 'WIWYANkTTLg7iGbFgEbwj4BM',
                'amount': amount,
                'currency': 'INR',
            }
            return render(request, 'payment.html', context)
    return render(request, 'create_payment.html')

# def success(request):
#     if 'user' in request.session:
#         obj=user.objects.get(name=request.session['user']['name'])
#         pp=addproduct.objects.get(pk=request.session['payment']['pdctid'])
#         payment,created=Payment.objects.get_or_create(order_id=request.session['payment']['order_id'],amount=request.session['payment']['amount'],location=request.session['payment']['location'],pincode=request.session['payment']['pincode'],usrdetail=obj,product=pp)
#         payment.save()
#         pay=Payment.objects.filter(order_id=request.session['payment']['order_id'])
#     return render(request,'success.html',{'pay':pay})
def success(request):
    if 'user' in request.session:
        obj=user.objects.get(name=request.session['user']['name'])
        print('user',obj)
        pp=addproduct.objects.get(pk=request.session['payment']['pdctid'])
        payment,created = Payment.objects.get_or_create(order_id=request.session['payment']['order_id'] ,amount=request.session['payment']['amount'],location=request.session['payment']['location'],pincode=request.session['payment']['pincode'],usrdetail=obj,product=pp)
        payment.save()
        pay=Payment.objects.filter(order_id=request.session['payment']['order_id'])
        itm=buy.objects.filter(userdetails=obj).first()
        pro=addproduct.objects.get(id=itm.buyitm.id)
        print(itm)
        print("Stock",itm.buyitm.stock,pro.stock)
        print("Quantity",itm.qty)
        pro.stock=pro.stock-itm.qty
        print("Stock after decriment",pro.stock)
        pro.save()
        order=buy.objects.filter(userdetails__username=request.session['user']['username'])
        for i in order:
            print(i.delete())
    return render(request,'success.html',{'pay':pay})
@csrf_exempt
# def payment_callback(request):
#     if request.method == 'POST':
#         payment_id = request.POST.get('razorpay_payment_id')
#         order_id = request.POST.get('razorpay_order_id')
#         signature = request.POST.get('razorpay_signature')

#         payment = Payment.objects.get(order_id=order_id)
#         params_dict = {
#             'razorpay_order_id': order_id,
#             'razorpay_payment_id': payment_id,
#             'razorpay_signature': signature
#         }
#         try:
#             client.utility.verify_payment_signature(params_dict)
#             payment.status = 'successful'
#             payment.payment_id = payment_id
#             payment.save()
#             return render(request, 'payments/success.html')
#         except:
#             payment.status = 'failed'
#             payment.save()
#             return render(request, 'payments/failure.html')
#     return redirect('/')

def cart_payment(request):
    if 'user' in request.session:
        obj=user.objects.get(name=request.session['user']['name'])
        print('user',obj)
        if request.method == 'POST':
            location=request.POST.get('location')
            pincode=request.POST.get('pincode')
            rpamount = int(request.POST['amount'])  # Razorpay amount in paisa
            # if len(request.session['product'])>0:
            #     pdct=request.session['product']
            #     request.session.pop('product')
        
            amount=rpamount*100
            print("AMOUNT",amount)
            # payment = Payment.objects.create(amount=rpamount,usrdetail=obj,location=location,pincode=pincode)
            razorpay_order = client.order.create(dict(amount=amount, currency='INR', payment_capture='1'))
            # payment.order_id = razorpay_order['id']
            request.session['cartpay']={'amount':rpamount,'location':location,'pincode':pincode,'order_id':razorpay_order['id']}

            # payment.save()
            
            # Generate QR code for the payment link
            payment_url = f"https://api.razorpay.com/v1/checkout/embedded?order_id={razorpay_order['id']}&key_id=WIWYANkTTLg7iGbFgEbwj4BM"
            qr = qrcode.make(payment_url)
            buffer = io.BytesIO()
            qr.save(buffer, format="PNG")
            buffer.seek(0)
            qr_image = buffer.getvalue()

            context = {
                'qr_image': qr_image,
                'razorpay_order_id': razorpay_order['id'],
                'razorpay_key_id': 'WIWYANkTTLg7iGbFgEbwj4BM',
                'amount': amount,
                'currency': 'INR',
            }
            return render(request, 'cpayment.html', context)
    return render(request, 'cpay.html')

# def csuccess(request):
#     if 'user' in request.session:
#         cobj=user.objects.get(name=request.session['user']['name'])
#         pay=0  #testing
#         # pdct=request.session['cartpay']['ctid']
#         details=''
#         product=''
#         priceitm=''
#         qty=''
#         qtyprice=''
#         farmer=''
#         fremail=''
#         tot=0
#         obj=cart.objects.filter(user_details__name=request.session['user']['name'])
#         for i in obj:
#             print("ID=",i)
#             # obj=cart.objects.get(id=i)
            
#             # st=f'''
#             # {i.cartitm.name:<18}{i.cartitm.price:<5}{i.count:<10}{i.tprice}\n
#             # {i.cartitm.frname.name:<20}{i.cartitm.frname.email}\n
#             # '''
#             #  details=details+st+'\n'
#             #  tot=tot+i.tprice
#             #  s='--'*20
#             #  details=details+s+'\n\tTOTAL - '+str(tot)+'\n'+s

#             st=i.cartitm.name
#             st1=str({i.cartitm.price})
#             st2=str({i.count})
#             st3=str({i.tprice})
#             st4=i.cartitm.frname.name
#             st5=i.cartitm.frname.email

#             product=product+st+'\n'
#             priceitm=priceitm+st1+'\n'
#             qty=qty+st2+'\n'
#             qtyprice=qtyprice+st3+'\n'
#             farmer=farmer+st4+'\n'
#             fremail=fremail+st5+'\n'
#             fpro=frorder.objects.create(fruname=i.cartitm.frname.name,fuser=i.user_details.name,proprice=i.cartitm.price,pitm=i.cartitm.name,pcount=i.count,ptotal=i.tprice)
#             fpro.save()
#             tot=tot+i.tprice
#             # s='--'*20
#         details=tot
#         print(details)
        
#         for i in obj:
#             print('user product',i.id)
#         # prod=[]
#         # for i in obj:
#         #     prod.append(i.id)
#         # print(prod)
#         cpayment,created = cartpayment.objects.get_or_create(order_id=request.session['cartpay']['order_id'] ,amount=request.session['cartpay']['amount'],location=request.session['cartpay']['location'],pincode=request.session['cartpay']['pincode'],pdctdetails=product,priceitm=i.cartitm.price,qty=i.count,qtyprice=i.tprice,farmer=farmer,fremail=fremail,totalprice=details,cartuser=cobj)
#         cpayment.save()
#         pay=cartpayment.objects.filter(order_id=request.session['cartpay']['order_id'] )
#         order=cart.objects.filter(user_details__username=request.session['user']['username'])
#         for i in order:
#             print(i.delete())  
#     return render(request,'csuccess.html',{'pay':pay,})

def csuccess(request):
    if 'user' in request.session:
        cobj=user.objects.get(name=request.session['user']['name'])
        pay=0  #testing
        details=''
        product=''
        priceitm=''
        qty=''
        qtyprice=''
        farmer=''
        fremail=''
        tot=0
        obj=cart.objects.filter(user_details__name=request.session['user']['name'])
        for i in obj:
            print("ID=",i)

            st=i.cartitm.name
            st1=str({i.cartitm.price})
            st2=str({i.count})
            st3=str({i.tprice})
            st4=i.cartitm.frname.name
            st5=i.cartitm.frname.email
            print("Farmer Name","Price","Item","Count","Total")
            print(st4,st1,st,st2,st3)

            product=product+st+'\n'
            priceitm=priceitm+st1+'\n'
            qty=qty+st2+'\n'
            qtyprice=qtyprice+st3+'\n'
            farmer=farmer+st4+'\n'
            fremail=fremail+st5+'\n'
            fpro=frorder.objects.create(fruname=i.cartitm.frname.name,fuser=i.user_details.name,proprice=i.cartitm.price,pitm=i.cartitm.name,pcount=i.count,ptotal=i.tprice)
            fpro.save()

            tot=tot+i.tprice
        details=tot
        print(details)
        
        for i in obj:
            print('user product',i.id)

            cpayment,created = cartpayment.objects.get_or_create(order_id=request.session['cartpay']['order_id'] ,amount=request.session['cartpay']['amount'],location=request.session['cartpay']['location'],pincode=request.session['cartpay']['pincode'],pdctdetails=i.cartitm.name,priceitm=i.cartitm.price,qty=i.count,qtyprice=i.tprice,farmer=i.cartitm.frname.name,fremail=i.cartitm.frname.email,totalprice=details,cartuser=cobj)
            cpayment.save()
        pay=cartpayment.objects.filter(order_id=request.session['cartpay']['order_id'] )       

        itm=cart.objects.filter(user_details=cobj)
        for i in itm:
            pro=addproduct.objects.get(id=i.cartitm.id)
            print(i)
            print("Stock",i.cartitm.stock,pro.stock)
            print("Quantity",i.count)
            pro.stock=pro.stock-i.count
            print("Stock after decriment",pro.stock)
            pro.save()

        order=cart.objects.filter(user_details__username=request.session['user']['username'])
        for i in order:
            print(i.delete())
    return render(request,'csuccess.html',{'pay':pay})