from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions, viewsets, status
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['PATCH'])
    def change_quantity(self,request):
        product = self.queryset.get(sku=request.data['sku'])
        data = {"qty": product.qty + request.data['quantity_delta']}
        product_serializer = ProductSerializer(product, data=data, partial=True)
        if product_serializer.is_valid(): 
            product_serializer.save() 
            return Response(product_serializer.data) 
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def available(self,request):
        products = Product.objects.filter(qty__gt=0)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def sold_out(self,request):
        products = Product.objects.filter(qty=0)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)