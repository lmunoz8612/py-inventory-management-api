from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ViewSet):
    def list(self, request):
        products = Product.objects.all()

        category = request.query_params.get('category')
        price = request.query_params.get('price')
        sku = request.query_params.get('sku')

        if category:
            products = products.filter(category__iexact = category)
        if price:
            try:
                products = products.filter(price = float(price))
            except ValueError:
                return Response({'error': 'Invalid price.'}, status = status.HTTP_400_BAD_REQUEST)
        if sku:
            try:
                products = products.filter(sku = sku)
            except ValueError:
                return Response({'error': 'Invalid sku.'}, status = status.HTTP_400_BAD_REQUEST)

        serializer = ProductSerializer(products, many = True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk = None):
        try:
            product = Product.objects.get(pk = pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status = status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk = None):
        try:
            product = Product.objects.get(pk = pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status = status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def destroy(self, request, pk = None):
        try:
            product = Product.objects.get(pk = pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status = status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response({'message': 'Product successfully deleted.'}, status = status.HTTP_204_NO_CONTENT)
