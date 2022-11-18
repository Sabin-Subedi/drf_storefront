from decimal import Decimal
from store.models import Product, Collection, Review,Cart,CartItem
from rest_framework import serializers


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'collection']

    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)

   
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
    
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']
        
class CartItemSerializer(serializers.ModelSerializer):
    product= SimpleProductSerializer()
    total_price=serializers.SerializerMethodField(read_only=True,method_name='get_total_price')
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity','total_price']
        
    def get_total_price(self,cart_item:CartItem):
        return cart_item.product.unit_price * cart_item.quantity
    
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    
    def validate_product_id(self,value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("No Product with the given id is found.")
        return value
        
    def save(self,**kwargs):
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        card_id = self.context['cart_id']
        
        try:
            cart_item = CartItem.objects.get(cart_id=card_id,product_id=product_id)
            cart_item += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
           self.instance =  CartItem.objects.create(cart_id=card_id,**self.validated_data)
        
        return self.instance
    class Meta:
        model = CartItem
        fields = ['id','product_id', 'quantity']

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [ 'quantity']

  

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Cart
        fields = ['id','items','total_price']
    
    def get_total_price(self,cart):
        return sum([item.quantity * item.product.unit_price  for item in cart.items.all()])
        