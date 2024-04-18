from rest_framework.viewsets import ModelViewSet
from .models import Post, Product, Category
from .serializers import PostSerializer, ProductSerializer
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render
from .forms.userForms import UserCreationForm
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product
import base64
import os


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

def create_user(request):
    form = UserCreationForm(request.POST)
    if request.method == 'POST':         
        if form.is_valid():
                form.save()
                username = form.cleaned_data.get('email')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('')
        else:
            form = UserCreationForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})

def product_view(request):
    product=Product.objects.all()
    return render(request, 'products.html',{'products':product})

class ProductViewSet(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        name = request.data["name"]
        category=request.data["category"]
        description=request.data["description"]
        barcode=request.data["barcode"]
        unit=request.data["unit"]
        size=request.data["size"]
        price=request.data["price"]
        image=request.data["image"]

        image_data = request.POST.get('image', '')
        if image_data:
            # Decode base64 image data
            try:
                image_bytes = base64.b64decode(image_data)
            except Exception as e:
                return JsonResponse({'error': 'Invalid image data'}, status=400)

            # Save the image file
            image_name = f'{name}_image.jpg'  # Customize the image name as needed
            image_path = os.path.join('media', 'products', image_name)  # Adjust the path as needed
            with open(image_path, 'wb') as f:
                f.write(image_bytes)


        Product.objects.create(name=name,
                                category=Category.objects.get(category=category),
                               description=description,
                               barcode=barcode,
                               unit=unit,
                               size=size,
                               price=price,
                               image=image_path
                               )
        return Response("Product created sucessfully", status=status.HTTP_200_OK)
    
@csrf_exempt
def upload_product(request):
    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        barcode = request.POST.get('barcode', '')
        unit = request.POST.get('unit', '')
        size = request.POST.get('size', '')
        price = request.POST.get('price', '')
        category = request.POST.get('category', '')

        # Get image data
        image_data = request.POST.get('image', '')
        if image_data:
            # Decode base64 image data
            try:
                image_bytes = base64.b64decode(image_data)
            except Exception as e:
                return JsonResponse({'error': 'Invalid image data'}, status=400)

            # Save the image file
            image_name = f'{name}_image.jpg'  # Customize the image name as needed
            image_path = os.path.join( 'products', image_name)  # Adjust the path as needed
            with open(image_path, 'wb') as f:
                f.write(image_bytes)

        # Create the product instance
        product = Product.objects.create(
            name=name,
            description=description,
            barcode=barcode,
            unit=unit,
            size=size,
            price=price,
            category=category,
            image=image_path  # Update the image path accordingly
        )

        # You can return a success response
        return JsonResponse({'message': 'Product uploaded successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
