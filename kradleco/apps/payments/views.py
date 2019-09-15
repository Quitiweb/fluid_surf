import stripe
import requests

from django.conf import settings
from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.views import View
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

from .models import Seller

stripe.api_key = settings.STRIPE_SECRET_KEY


class HomePageView(TemplateView):
    template_name = 'payments/stripe.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        context['stripe'] = True
        return context


def charge_iban(request):
    source = stripe.Source.create(
        type='sepa_debit',
        sepa_debit={'iban': 'DE89370400440532013000'},
        currency='eur',
        owner={
            'name': 'Jenny Rosen',
        },
    )
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=10000,
            currency='eur',
            description='IBAN SEPA Charge',
            source=source
        )
        return render(request, 'payments/charge-iban.html')


def charge(request):
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=50000,
            currency='eur',
            description='A Django charge',
            source=request.POST['stripeToken']
        )
        return render(request, 'payments/charge.html')


def charge_account(request):
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=10000,
            currency='eur',
            description='Payment from views.charge_account',
            source="tok_visa",
            application_fee_amount='300',
            stripe_account='acct_1EX8cPFibtUO8iPR'
        )
        return render(request, 'payments/charge-account.html')


def transfer(request):
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=10000,
            currency='eur',
            description='Test 1',
            source='tok_visa',
            transfer_group='ORDER_19'
        )
        transfer = stripe.Transfer.create(
            amount=1940,
            currency='eur',
            description='Kradleco Transfer Test 1',
            destination='acct_1EX8cPFibtUO8iPR',  # El ID de la cuenta quiti@quitiweb.com
            transfer_group='ORDER_19'
        )
        transfer = stripe.Transfer.create(
            amount=7760,
            currency='eur',
            description='Kradleco Transfer Test 1',
            destination='acct_1EXbhEA49TuR4jcA',  # El ID de la cuenta info@quitiweb.com
            transfer_group='ORDER_19'
        )
        return render(request, 'payments/transfer.html')


class CallBack(View):

    def get(self, request):
        code = request.GET.get('code')
        if code:
            data = {
                'client_secret': settings.STRIPE_SECRET_KEY,
                'grant_type': 'authorization_code',
                'client_id': settings.STRIPE_CONNECT_CLIENT_ID,
                'code': code
            }
            url = 'https://connect.stripe.com/oauth/token'
            resp = requests.post(url, params=data)

            # add stripe info to the seller
            stripe_user_id = resp.json()['stripe_user_id']
            stripe_access_token = resp.json()['access_token']
            seller = Seller.objects.filter(user_id=self.request.user.id).first()
            seller.stripe_access_token = stripe_access_token
            seller.stripe_user_id = stripe_user_id
            seller.save()

        url = reverse('landing')
        response = redirect(url)

        return response


class Authorize(View):

    def get(self, request):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        url = 'https://connect.stripe.com/oauth/authorize'
        params = {
            'response_type': 'code',
            'scope': 'read_write',
            'client_id': settings.STRIPE_CONNECT_CLIENT_ID,
            'redirect_uri': 'http://localhost:8000/payments/callback'
        }

        url = '{url}?{urllib.parse.urlencode(params)}'

        return redirect(url)
