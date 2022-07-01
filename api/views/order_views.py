from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from api import models
from api import serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from rest_framework import status
from datetime import datetime
from api.email import sendEmail
from datetime  import date



def orderIdGenerator(id):
    today = date.today()
    orderId = f"OR-{str(today).replace('-', '')}-{id}"
    return orderId

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrder(request):
    user = request.user
    data = request.data

    orderItems = data['orderItems']

    if orderItems and len(orderItems) == 0:
        return Response({'message': 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)

    else:
        order = models.Order.objects.create(
            user=user,
            taxPrice=float(data['taxPrice']),
            shippingPrice=float(data['shippingPrice']),
            totalPrice=float(data['totalPrice']),
            paymentMethod=data['paymentMethod']
        )
        order.orderId = orderIdGenerator(order._id)
        order.save()
        shipping = models.ShippingAddress.objects.create(
            order=order,
            address=data['shippingAddress']['address'],
            city=data['shippingAddress']['city'],
            postalCode=data['shippingAddress']['postalCode'],
            country=data['shippingAddress']['country']

        )

        for i in orderItems:
            product = models.Product.objects.get(_id=i['product'])
            item = models.OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                qty=i['qty'],
                price=i['price'],
                image=product.image.url
            )
            product.countInStock -= item.qty
            product.save()


        serializer = serializers.OrderSerializer(order, many=False)
        return Response(serializer.data)





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request,pk):
    print(f'id:{pk}')
    user = request.user
    try:
        order = models.Order.objects.get(_id=pk)
        if user.is_staff or order.user ==user:
            serializer = serializers.OrderSerializer(order,many=False)
            return Response(serializer.data)
        else:
            return Response({"Message": "You are not authorised to view this order"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Message":"Invalid Order ID"},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
    user = request.user
    orders = user.order_set.all()
    serializer = serializers.OrderSerializer(orders,many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getOrders(request):
    orders = models.Order.objects.all()
    serializer = serializers.OrderSerializer(orders,many=True)
    return Response(serializer.data)




@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request,pk):
    try:
        order = models.Order.objects.get(_id=pk)
        order.isPaid = True
        order.paidAt = datetime.now()
        order.save()
        return Response("Order Was Paid")
    except:
        return Response({'message':'Invalid Order ID'},status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateOrderToDelivered(request,pk):
    try:
        order = models.Order.objects.get(_id=pk)
        order.isDelivered = True
        order.deliveredAt = datetime.now()
        order.save()
        return Response("Order Was Delivered")
    except:
        return Response({'message':'Invalid Order ID'},status=status.HTTP_400_BAD_REQUEST)