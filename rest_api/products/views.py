from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions, viewsets, status
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    lookup_field = 'sku'
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [permissions.AllowAny]
    
    def get_object(self):
        sku = self.kwargs['sku']
        return self.queryset.get(sku=sku)
        
    """
    Changes quantity by quantity_delta in product with matching sku
    """
    @action(detail=True, methods=['post'], url_path='action')
    def change_quantity(self,request,sku):
        product = self.queryset.get(sku=sku)
        data = {"qty": product.qty + request.data['quantity_delta']}
        product_serializer = ProductSerializer(product, data=data, partial=True)
        if product_serializer.is_valid(): 
            product_serializer.save() 
            return Response(product_serializer.data) 
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    Returns all products with quantity less than 0
    """
    @action(detail=False, methods=['GET'])
    def available(self,request):
        products = Product.objects.filter(qty__gt=0)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    """
    Returns all products with quantity equals 0
    """
    @action(detail=False, methods=['GET'])
    def sold_out(self,request):
        products = Product.objects.filter(qty=0)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)