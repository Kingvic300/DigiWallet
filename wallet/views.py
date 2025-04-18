import uuid

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import requests

from wallet.models import Transaction
from wallet.serializer import FundSerializer


# Create your views here.
@api_view()
def welcome(request):
    return Response(f"Welcome to SafeWallet")


def greeting(request, name):
    return render(request,'hello.html',{'name':name})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def fund_wallet(request):
    data = FundSerializer(data = request.data)
    data.is_valid(raise_exception=True)
    amount = data.validated_data['amount']
    amount*=100
    email = request.user.email
    reference = f'ref_{uuid.uuid4().hex}'
    Transaction.objects.create(amount=amount, reference_number=reference, sender=request.user)
    url = 'https://api.paystack.co/transaction/initialize'
    secret = settings.PAYSTACK_SECRET_KEY
    headers = {
        'Authorization': f'Bearer {secret}',
    }
    data = {
        'amount': amount,
        'reference_number': reference,
        'email': email,
    }
    response_str = requests.post(url = url, json=data, headers=headers)
    response = response_str.json()
    if response['status']:
        return Response(data=response['data'],status=status.HTTP_200_OK)
    return Response(data={'message':'Unable to complete transaction'},status=status.HTTP_400_BAD_REQUEST)