from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer, UserProfileSerializer, DeliveryAddressSerializer
from .models import DeliveryAddress


@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LoginView(View):
#     def validate_username(self, username):
#         return re.match(r'\s+', username)
#
#     @method_decorator(csrf_exempt)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         data = json.loads(request.body)
#         username = data.get('username')
#         password = data.get('password')
#
#         if self.validate_username(username):
#             return JsonResponse({'error': 'No whitespace characters'}, status=400)
#         if len(password) < 6:
#             return JsonResponse({'error': 'Password must be at least 6 characters'}, status=400)
#
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             token, _ = Token.objects.get_or_create(user=user)
#             return JsonResponse({'token': token.key})
#         else:
#             return JsonResponse({'error': 'Invalid credentials'}, status=400)


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class DeliveryAddressViewSet(viewsets.ModelViewSet):
    queryset = DeliveryAddress.objects.all()
    serializer_class = DeliveryAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
