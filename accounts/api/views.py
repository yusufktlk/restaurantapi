from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import generics, permissions
from rest_framework.generics import get_object_or_404
from accounts.models import CustomerProfile, RestaurantProfile, ProductCategory, Order, OrderItem, Product, OrderUser

from accounts.api.serializer import (
    CustomerProfileSerializer,
    ProductCategorySerializer,
    OrderSerializer,
    OrderItemSerializer,
    ProductSerializer,
    RestaurantProfileSerializer,
    CustomerRegisterSerializer,
    RestaurantRegisterSerializer
)
from accounts.api.permissons import IsRestaurantOwnerOrReadOnly, IsOwnerOrReadOnly
from rest_framework import status
from dj_rest_auth.registration.views import RegisterView 

class CustomerProfileAPIView(generics.ListCreateAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CustomerProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

class ProductCategoryAPIView(generics.ListCreateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    # permission_classes = [permissions.IsAuthenticated]

class ProductCategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrderCreateView(APIView):
    def post(self, request, *args, **kwargs):
        user_data = request.data['order_user']
        orderUser = OrderUser.objects.create(**user_data)
        customer = User.objects.get(id = request.user.id)
        serializer_data = {
            'user': customer.id,
            'restaurant': request.data['restaurant'],
            'order_note': request.data['order_note'],
            'order_items': request.data['order_items'],
            'order_user': orderUser.id,
        }
        serializer = OrderSerializer(data=serializer_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class RestaurantProfileAPIView(generics.ListCreateAPIView):
    queryset = RestaurantProfile.objects.all()
    serializer_class = RestaurantProfileSerializer
    # permission_classes = [permissions.IsAuthenticated]

class RestaurantProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RestaurantProfile.objects.all()
    serializer_class = RestaurantProfileSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwnerOrReadOnly ]
    

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    

class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        category = serializer.validated_data.get('category')
        restaurant = self.request.user.restaurantprofile  
        serializer.save(category=category, restaurant=restaurant) 


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsRestaurantOwnerOrReadOnly]

### Login
class LoginView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=400)
        
### Register

# class RegisterView(DefaultRegisterView):
#     permission_classes = [AllowAny]
#     serializer_class = CustomRegisterSerializer

#     def post(self, request):
#         username = request.data.get('username')
#         email = request.data.get('email')
#         password1 = request.data.get('password1')
#         password2 = request.data.get('password2')
#         account_type = request.data.get('account_type')

#         if User.objects.filter(username__iexact=username).exists():
#             return JsonResponse({'error': 'Username already exists'}, status=400)
#         if User.objects.filter(email__iexact=email).exists():
#             return JsonResponse({'error': 'Email already exists'}, status=400)
#         if password1 != password2:
#             return JsonResponse({'error': "Passwords don't match"}, status=400)

#         user = User.objects.create_user(username=username, email=email, password=password1)


#         if account_type == 'customer':
#             CustomerProfile.objects.create(user=user)
#         elif account_type == 'restaurant':
#             # adress = request.data["adress"]
#             # x = RestaurantProfile.objects.create(
#             #     adress = request.data["adress"],
#             # )
#             RestaurantProfile.objects.create(user=user)

    
#         else:
#             return JsonResponse({'error': "Invalid account type"}, status=400)


#         token, _ = Token.objects.get_or_create(user=user)

#         return Response({'token': token.key})

# class CustomerRegisterView(DefaultRegisterView):
#     permission_classes = [AllowAny]
#     serializer_class = CustomRegisterSerializer

#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)
#         if response.status_code == 201:
#             user = User.objects.get(username=request.data.get('username'))
#             CustomerProfile.objects.create(user=user)
#         return response


# class RestaurantRegisterView(DefaultRegisterView):
#     permission_classes = [AllowAny]
#     serializer_class = CustomRegisterSerializer

#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)
#         if response.status_code == 201:
#             user = User.objects.get(username=request.data.get('username'))
#             RestaurantProfile.objects.create(user=user)
#         return response


class CustomerRegisterView(RegisterView):
    serializer_class = CustomerRegisterSerializer

    def post(self, request):
        print(request.data)
        username = request.data.get('username')
        email = request.data.get('email')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')
        adres = request.data.get('adres')
        telefon = request.data.get('telefon')
        
        if User.objects.filter(username__iexact=username).exists():
            print("denem1")
            return JsonResponse({'error': 'Username already exists'}, status=400)
        if User.objects.filter(email__iexact=email).exists():
            print("denem2")
            return JsonResponse({'error': 'Email already exists'}, status=400)
        if password1 != password2:
            print("deneme3")
            return JsonResponse({'error': "Passwords don't match"}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password1)

        customer_profile = CustomerProfile.objects.create(user=user, telefon=telefon, adres=adres)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

class RestaurantRegisterView(RegisterView):
    serializer_class = RestaurantRegisterSerializer

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')
        name = request.data.get('name')
        address = request.data.get('address')
        image = request.data.get('image')
        minimum_order_amount = request.data.get('minimum_order_amount')
        categories = request.data.getlist('categories')  
        print(request.data["categories"])
        if User.objects.filter(username__iexact=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=401)
        if User.objects.filter(email__iexact=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=402)
        if password1 != password2:
            return JsonResponse({'error': "Passwords don't match"}, status=403)

        user = User.objects.create_user(username=username, email=email, password=password1)

        # RestaurantProfile oluşturun ve ilişkilendirin
        restaurant_profile = RestaurantProfile.objects.create(
            user=user,
            name=name,
            address=address,
            image=image,
            minimum_order_amount=minimum_order_amount
        )
        restaurant_profile.categories.set(categories) 

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})