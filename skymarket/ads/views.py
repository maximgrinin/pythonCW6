from django.shortcuts import get_object_or_404
from rest_framework import pagination, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, extend_schema_view

from ads.models import Ad, Comment
from ads.permissions import IsOwner, IsAdmin
from ads.serializers import AdDetailSerializer, AdListSerializer, CommentSerializer
from ads.filters import AdFilter


class AdPagination(pagination.PageNumberPagination):
    page_size = 4


@extend_schema_view(
    list=extend_schema(
        description="Получение списка объявлений",
        summary="Список объявлений",
    ),
    retrieve=extend_schema(
        description="Получение объявления",
        summary="Объявление",
    ),
    create=extend_schema(
        description="Создание нового объявления",
        summary="Создание объявления",
    ),
    destroy=extend_schema(
        description="Удаление объявления",
        summary="Удаление объявления",
    ),
    update=extend_schema(
        description="Изменение объявления",
        summary="Изменение объявление",
    ),
    partial_update=extend_schema(
        description="Частичное изменение объявления",
        summary="Частичное изменение объявления",
    ),
    me=extend_schema(
        description="Список объявлений пользователя",
        summary="Объявления пользователя",
    ),
)
class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdListSerializer
    pagination_class = AdPagination
    permission_classes = (AllowAny, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdFilter

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)

    def get_serializer_class(self):
        if self.action in ["retrieve", "create", "update", "partial_update", "destroy"]:
            return AdDetailSerializer
        return AdListSerializer

    def get_permissions(self):
        permission_classes = (AllowAny, )
        if self.action in ["retrieve"]:
            permission_classes = (AllowAny, )
        elif self.action in ["create", "update", "partial_update", "destroy", "me"]:
            permission_classes = (IsOwner | IsAdmin,)
        return tuple(permission() for permission in permission_classes)

    def get_queryset(self):
        if self.action == "me":
            return Ad.objects.filter(author=self.request.user).all()
        return Ad.objects.all()


    @action(
        detail=False,
        methods=["get",
                 ],
    )
    def me(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)


@extend_schema_view(
    list=extend_schema(
        description="Получение списка комментариев",
        summary="Список комментариев",
    ),
    retrieve=extend_schema(
        description="Получение комментария",
        summary="Комментарий",
    ),
    create=extend_schema(
        description="Создание нового комментария",
        summary="Создание комментария",
    ),
    destroy=extend_schema(
        description="Удаление комментария",
        summary="Удаление комментария",
    ),
    update=extend_schema(
        description="Изменение комментария",
        summary="Изменение комментария",
    ),
    partial_update=extend_schema(
        description="Частичное изменение комментария",
        summary="Частичное изменение комментария",
    ),
)
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


    def perform_create(self, serializer):
        ad_id = self.kwargs.get("ad_pk")
        ad_instance = get_object_or_404(Ad, id=ad_id)
        user = self.request.user
        serializer.save(author=user, ad=ad_instance)

    def get_queryset(self):
        ad_id = self.kwargs.get("ad_pk")
        ad_instance = get_object_or_404(Ad, id=ad_id)
        return ad_instance.comments.all()

    def get_permissions(self):
        permission_classes = (IsAuthenticated,)
        if self.action in ["list", "retrieve"]:
            permission_classes = (IsAuthenticated,)
        elif self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = (IsOwner | IsAdmin,)
        return tuple(permission() for permission in permission_classes)
