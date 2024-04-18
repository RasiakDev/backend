from rest_framework.serializers import ModelSerializer
from eCommerce.models import Post, Product
from drf_extra_fields.fields import Base64ImageField


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'body')

class ProductSerializer(ModelSerializer):
    image = Base64ImageField()
    class Meta:
        model=Product
        fields=('name','category', 'description', 'barcode','unit', 'size', 'price', 'image', 'category')

