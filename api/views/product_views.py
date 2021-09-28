from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from api import models
from api import serializers
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@api_view(['GET'])
def getProducts(request):
    product = models.Product.objects.all().order_by('createdAt')
    page = request.query_params.get('page')
    paginator = Paginator(product, 8)

    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)

    if page is None:
        page = 1

    page = int(page)

    serializer = serializers.ProductSerializers(product, many=True)
    return Response({'products': serializer.data, 'page': page, 'pages': paginator.num_pages})

@api_view(['GET'])
def getTopProducts(request):
    products = models.Product.objects.filter(rating__gte=4).order_by('-rating')[0:5]
    serializer = serializers.ProductSerializers(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProduct(request, pk):
    try:
        product = models.Product.objects.get(_id=pk)
        serializer = serializers.ProductSerializers(product, many=False)
        return Response(serializer.data)
    except:
        return JsonResponse({'success': False, 'message': 'Invalid product ID'}, status=422)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProduct(request, pk):
    try:
        product = models.Product.objects.get(_id=pk)
        product.delete()
        return Response("Product Deleted")
    except:
        return JsonResponse({'success': False, 'message': 'Invalid product ID'}, status=422)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createProduct(request):
    user = request.user
    product = models.Product.objects.create(
        user=user,
        name='sample name',
        price=0,
        brand='sample brand',
        countInStock=0,
        category='sample category',
        description=''
    )
    serializer = serializers.ProductSerializers(product, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
def updateProduct(request, pk):
    data = request.data
    try:
        product = models.Product.objects.get(_id=pk)
        product.name = data['name']
        product.price = data['price']
        product.brand = data['brand']
        product.countInStock = data['countInStock']
        product.category = data['category']
        product.description = data['description']
        product.save()
        serializer = serializers.ProductSerializers(product, many=False)
        return Response(serializer.data)
    except:
        return JsonResponse({'success': False, 'message': 'Invalid product ID'}, status=422)


@api_view(['POST'])
def uploadImage(request):
    data = request.data
    productId = data['product_id']
    product = models.Product.objects.get(_id=productId)
    product.image = request.FILES.get('image')
    product.save()
    return Response("Image Uploaded")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProductReview(request, pk):
    user = request.user
    data = request.data
    try:
        product = models.Product.objects.get(_id=pk)
    except:
        return Response({"message": 'Invalid Product ID'}, status=status.HTTP_400_BAD_REQUEST)

    if product.review_set.filter(user=user).exists():
        content = {'message': 'Product Already Reviewed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    elif data['rating'] == 0:
        content = {'message': 'Please Select a Rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    else:
        review = models.Review.objects.create(
            user=user,
            product=product,
            name=user.first_name,
            rating=data['rating'],
            comment=data['comment']
        )
        reviews = product.review_set.all()
        product.numReviews = len(reviews)
        total = 0
        for i in reviews:
            total += i.rating
        product.rating = total
        product.save()
        return Response("Review Added")
