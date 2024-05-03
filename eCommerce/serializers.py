from rest_framework.serializers import ModelSerializer, EmailField, CharField, ValidationError
from eCommerce.models import Post, Product, User
from drf_extra_fields.fields import Base64ImageField
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class UserSerializer(ModelSerializer):
  class Meta:
    model = User
    fields = ["id", "name", "email", "username"]

    #Serializer to Register User
class RegisterSerializer(ModelSerializer):
  email = EmailField(
    required=True,
    validators=[UniqueValidator(queryset=User.objects.all())]
  )
  password = CharField(
    write_only=True, required=True, validators=[validate_password])
  class Meta:
    model = User
    fields = ('password',
         'email', 'name')

 
  def create(self, validated_data):
    user = User.objects.create(
      username=validated_data['email'],
      email=validated_data['email'],
      name=validated_data['name'],
    )
    user.set_password(validated_data['password'])
    user.save()
    return user


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'body')

class ProductSerializer(ModelSerializer):
    image = Base64ImageField()
    class Meta:
        model=Product
        fields='__all__'
        # fields=('name','category', 'description', 'barcode','unit', 'size', 'price', 'image', 'category')

        

