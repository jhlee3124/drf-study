from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import action, api_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Post
from .serializers import PostSerializer

"""
추상화 레벨
APIView -> mixins -> generics -> viewset
APIView: get, post, delete, put, ... 직접 다 구현해야 함

mixins: create, list, retrieve, destory, partial_update, ... 지원됨
그러나, post-create, get-list 등 method별 mapping 직접 해야 함
ex:
class PostListAPIView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
        
generics: 미리 mapping을 해 두었음
ex:
generics.ListAPIView: get-list 

viewset: generics를 묶어준 형태
ex:
generics라면 아래처럼 별도로 list, detail 구현
class PostListGenericAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetailGenericAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

viewset은 이를 묶어서 제공
class PostViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
"""

# # generic 사용
# class PublicPostListAPIView(generics.ListAPIView):
#     queryset = Post.objects.filter(is_public=True)
#     serializer_class = PostSerializer


# # APIView 이용 직접 구현
# class PublicPostListAPIView(APIView):
#     def get(self, request):
#         queryset = Post.objects.filter(is_public=True)
#         serializer = PostSerializer(queryset, many=True)  # 다수 queryset은 many=True 지정 필요
#         return Response(serializer.data)


# public_post_list = PublicPostListAPIView.as_view()


# FBV로 구현
@api_view(["GET"])
def public_post_list(request):
    queryset = Post.objects.filter(is_public=True)
    serializer = PostSerializer(queryset, many=True)  # 다수 queryset은 many=True 지정 필요
    return Response(serializer.data)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission은 settings.py에서 default 전역 설정 변경도 가능
    # REST_FRAMEWORK = {
    #     'DEFAULT_PERMISSION_CLASSES':[
    #         'rest_framework.permissions.IsAuthenticated'
    #     ]
    # }
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = [
        "message"
    ]  # ?search= : queryset 조건절에 추가할 필드 지정. 모델 필드 중 문자열 필드만을 지정, get_search_fields 함수로도 구현 가능
    ordering_fields = [
        "id"
    ]  # ?ordering= : 정렬을 허용할 필드의 화이트리스트. 미지정시 serializer_class에 지정된 필드들
    ordering = ["id"]  # 디폴트 정렬 지정
    throttle_classes = UserRateThrottle  # 호출 횟수 제한 설정(넘기면 419 Too Many Requests 응답)

    """
    create시에 추가로 저장할 field 설정
    참고: mixins에서 perform_create, perform_update, perform_destory등 지원
    """

    def perform_create(self, serializer):
        author = self.request.user
        ip = self.request.META["REMOTE_ADDR"]
        serializer.save(ip=ip, author=author)

    """
    action 장식자
    - viewset에 새로운 endpoint 추가
    - detail: url상에서 pk등 사용 여부
    - URL_Reverse명: basename-함수명(언더바는 하이픈으로 변경)
    - 호출 주소 ex:
        - http://127.0.0.1:8000/post/public/
        - http://127.0.0.1:8000/post/1/set_public/
    """

    @action(detail=False, methods=["GET"])
    # URL_Reverse명: post-public
    def public(self, request):
        qs = self.get_queryset().filter(is_public=True)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["PATCH"])
    def set_public(self, request, pk):
        instance = self.get_object()
        instance.is_public = True
        instance.save(update_fields=["is_public"])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # def dispatch(self, request, *args, **kwargs):
    #     print("request.body :", request.body)
    #     print("request.POST :", request.POST)
    #     return super().dispatch(request, *args, **kwargs)
