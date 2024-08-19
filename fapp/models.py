from django.db import models

# Create your models here.
class farmer(models.Model):
    name=models.CharField(max_length=15)
    address=models.CharField(max_length=50)
    phonenumber=models.IntegerField()
    bankname=models.CharField(max_length=30)
    accountnumber=models.IntegerField()
    ifsccode=models.CharField(max_length=15)
    username=models.CharField(max_length=15)
    email=models.EmailField(default='farmer@gmail.com')
    password=models.CharField(max_length=20)
    image=models.ImageField()
    flicense=models.ImageField()
    status=models.IntegerField(default=0)
    
    def __str__(s):
        return f'{s.name}'

class PasswordResetFarm(models.Model):
    farm=models.ForeignKey(farmer,on_delete=models.CASCADE,blank=True)
    token=models.CharField(max_length=100,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)

class addproduct(models.Model):
    frname=models.ForeignKey(farmer,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    description=models.CharField(max_length=1000)
    price=models.IntegerField()
    image=models.ImageField()
    stock=models.IntegerField(default=0)

    
    def __str__(s):
        return f'{s.name}'
    
class user(models.Model):
    name=models.CharField(max_length=15)
    address=models.CharField(max_length=100)
    phonenumber=models.IntegerField()
    bankname=models.CharField(max_length=30)
    accountnumber=models.IntegerField()
    ifsccode=models.CharField(max_length=15)
    username=models.CharField(max_length=15)
    email=models.EmailField(default='users@gmail.com')
    password=models.CharField(max_length=20)
    image=models.ImageField()
    
    def __str__(s):
        return f'{s.name}'

class feedback(models.Model):
    udetail=models.ForeignKey(user,on_delete=models.CASCADE)
    fdetail=models.ForeignKey(farmer,on_delete=models.CASCADE,default=1)
    comment=models.CharField(max_length=1000)

    def __str__(s):
        return f'{s.udetail.name}'

class PasswordResetUsr(models.Model):
    usr=models.ForeignKey(user,on_delete=models.CASCADE,blank=True)
    token=models.CharField(max_length=100,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)

class cart(models.Model):
    user_details=models.ForeignKey(user,on_delete=models.CASCADE)
    cartitm=models.ForeignKey(addproduct,on_delete=models.CASCADE,related_name='cart')
    count=models.IntegerField(default=0)
    # price=models.IntegerField()
    date=models.DateTimeField(auto_now=True)
    tprice=models.IntegerField(default=0)

    def __str__(s):
        return f'{s.cartitm.name}'

class buy(models.Model):
    userdetails=models.ForeignKey(user,on_delete=models.CASCADE)
    buyitm=models.ForeignKey(addproduct,on_delete=models.CASCADE,related_name='buy')
    qty=models.IntegerField(default=0)
    datee=models.DateTimeField(auto_now=True)
    totprice=models.IntegerField(default=0)


    def __str__(s):
        return f'{s.buyitm.name}'

class cont(models.Model):
    usrdetail=models.ForeignKey(user,on_delete=models.CASCADE)
    frdetail=models.ForeignKey(farmer,on_delete=models.CASCADE,default=1)
    message=models.CharField(max_length=1000)

    def __str__(s):
        return f'{s.usrdetail.name}'

class rply(models.Model):
    comment=models.CharField(max_length=1000)
    name=models.CharField(max_length=15)
    email=models.EmailField(default='users@gmail.com')

    def __str__(s):
        return f'{s.name}'

from django.db import models

class Payment(models.Model):
    usrdetail=models.ForeignKey(user,on_delete=models.CASCADE)
    product=models.ForeignKey(addproduct,on_delete=models.PROTECT)
    order_id = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='created')
    created_at = models.DateTimeField(auto_now_add=True)
    location=models.CharField(max_length=50)
    pincode=models.IntegerField(default=0)
    delistatus=(('pending','Pending'),('delivered','Delivered'))
    deliverystatus=models.CharField(max_length=20,choices=delistatus, default='pending')

    def __str__(self):
        return self.order_id

class cartpayment(models.Model):
    cartuser=models.ForeignKey(user,on_delete=models.CASCADE)
    pdctdetails=models.CharField(max_length=400, blank=True, null=True)
    priceitm=models.CharField(max_length=400, blank=True, null=True)
    qty=models.CharField(max_length=400, blank=True, null=True)
    qtyprice=models.CharField(max_length=400, blank=True, null=True)
    farmer=models.CharField(max_length=400, blank=True, null=True)
    fremail=models.CharField(max_length=400, blank=True, null=True)
    totalprice=models.IntegerField(default=0) 
    order_id = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    location=models.CharField(max_length=50)
    pincode=models.IntegerField(default=0)


    def __str__(self):
        return self.order_id

class frorder(models.Model):
    fruname=models.CharField(max_length=400)
    fuser=models.CharField(max_length=400)
    proprice=models.IntegerField(default=0) 
    pitm=models.CharField(max_length=400)
    pcount=models.IntegerField(default=0) 
    ptotal=models.IntegerField(default=0)
    delistatus=(('pending','Pending'),('delivered','Delivered'))
    deliverystatus=models.CharField(max_length=20,choices=delistatus, default='pending') 

    def __str__(self):
        return self.fruname
