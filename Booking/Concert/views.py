
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from Concert.forms import SignUpForm, ConcertForm, GoldTicketForm, SliverTicketForm, BronzeTicketForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Concert, GoldTicket, SliverTicket, BronzeTicket
import stripe
from django.core.mail import send_mail
stripe.api_key = "sk_test_51Mi5SeAxQsk8kssvom87yN3TqmqI9LLlTReUD3iKxMGn3WItkeaZTb5lqAVxVnOhFNErGUCV7ENpyz5FT1DWRzBy00pkk56HcU"

# Create your views here.
def home(request):
    concerts = Concert.objects.all()
    return render(request, 'base.html', {'concerts': concerts})

def concert_detail(request, id):
    concert = get_object_or_404(Concert, id=id)
    gold = get_object_or_404(GoldTicket, id=id)
    sliver = get_object_or_404(SliverTicket, id=id)
    bronze = get_object_or_404(BronzeTicket, id=id)
    """  else: return redirect('/') """

    return render(request, 'detail.html', {'concert': concert, 'gold': gold , 'sliver': sliver, 'bronze': bronze, "id":id,  })

def admin_home(request):
    concerts = Concert.objects.all()
    return render(request, 'adminMain.html', {'concerts': concerts})

    
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                if username == 'admin':
                    return redirect('/adminHome')   
                else : 
                    return redirect('/')
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name='login.html', context={"login_form":form})


def create_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            form.save()
            return redirect('/login')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect('/')

def create_ticket(request):
    if request.method == 'POST':
        form1 = GoldTicketForm(request.POST )
        form2 = SliverTicketForm(request.POST )
        form3 = BronzeTicketForm(request.POST)
        if form1.is_valid() and form2.is_valid() and form3.is_valid():
            form1.save()
            form2.save()
            form3.save()
            return redirect('/createConcert')
    else:
        form1 = GoldTicketForm()
        form2 = SliverTicketForm()
        form3 = BronzeTicketForm()
    return render(request, 'createTicket.html', {'form1': form1 ,'form2': form2, 'form3': form3})

def create_concert(request):
    if request.method == 'POST':
        form = ConcertForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/adminHome')
    else:
        form = ConcertForm()
    return render(request, 'createConcert.html', {'form': form })


def payment(request, id):
    if request.method == 'POST':
        # Get the ticket details submitted by the form
        gold_quantity = int(request.POST.get('g_quantity'))
        silver_quantity = int(request.POST.get('s_quantity'))
        bronze_quantity = int(request.POST.get('b_quantity'))

        # Get the total amount based on the ticket prices and quantities
        gold_price = gold_quantity * GoldTicket.objects.first().price
        silver_price = silver_quantity * SliverTicket.objects.first().price
        bronze_price = bronze_quantity * BronzeTicket.objects.first().price
        total_amount = gold_price + silver_price + bronze_price

        gold_ticket = GoldTicket.objects.first()
        silver_ticket = SliverTicket.objects.first()
        bronze_ticket = BronzeTicket.objects.first()
        if gold_ticket.numOfTicket >= gold_quantity and silver_ticket.numOfTicket >= silver_quantity and bronze_ticket.numOfTicket >= bronze_quantity:
            gold_ticket.numOfTicket -= gold_quantity
            silver_ticket.numOfTicket -= silver_quantity
            bronze_ticket.numOfTicket -= bronze_quantity
            gold_ticket.save()
            silver_ticket.save()
            bronze_ticket.save()

            # Redirect the user to a success page
            return redirect('/')
        else:
            # Render the payment page with an error message if the available ticket quantity is less than the purchased quantity for any ticket type
            return render(request, 'payment.html', {'error_message': 'Not enough tickets available'})
    else:
        gold_ticket = GoldTicket.objects.first()
        silver_ticket = SliverTicket.objects.first()
        bronze_ticket = BronzeTicket.objects.first()
        return render(request, 'payment.html', {'gold_ticket': gold_ticket, 'silver_ticket': silver_ticket, 'bronze_ticket': bronze_ticket, 'id':id})

""" def payment(request, id):
        # Get the ticket details submitted by the form
    gold_quantity = int(request.POST.get('gold_quantity', 0))
    silver_quantity = int(request.POST.get('silver_quantity', 0))
    bronze_quantity = int(request.POST.get('bronze_quantity', 0))

    # Get the total amount based on the ticket prices and quantities
    gold_price = gold_quantity * GoldTicket.objects.first().price
    silver_price = silver_quantity * SliverTicket.objects.first().price
    bronze_price = bronze_quantity * BronzeTicket.objects.first().price
    total_amount = gold_price + silver_price + bronze_price
    if gold_ticket.numOfTicket >= gold_quantity and silver_ticket.numOfTicket >= silver_quantity and bronze_ticket.numOfTicket >= bronze_quantity:
            # Subtract the purchased quantity from the available quantity for each ticket type and save the changes to the model instances
            gold_ticket.numOfTicket -= gold_quantity
            silver_ticket.numOfTicket -= silver_quantity
            bronze_ticket.numOfTicket -= bronze_quantity
            gold_ticket.save()
            silver_ticket.save()
            bronze_ticket.save()
    if request.method == 'POST':
        # Get the credit card details submitted by the form
        token = request.POST.get('stripeToken')
        amount = request.POST.get('amount')
        description = request.POST.get('description')

        # Create a Stripe charge
        try:
            payment = stripe.Charge.create(
                amount=amount,
                currency='usd',
                description=description,
                source=token,
            )
        except stripe.error.CardError as e:
            # The card has been declined
            pass

        # Redirect the user to a success page
        return redirect('/')
    else:
        return render(request, 'payment.html',{'gold': gold , 'sliver': sliver, 'bronze': bronze, "id":id,  })
"""










