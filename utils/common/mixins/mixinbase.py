"""
fied : {
    authentication_classes : 验证
    permission_classes : 权限
    msg ; {
        "msg_create" : Create,返回时显示的消息,
        "msg_delete" : Delete,返回时显示的消息,
        "msg_update" : Put,返回时显示的消息,
        "msg_list" : Get,返回时显示的消息,
        "msg_detail" : Get,返回时显示的消息,
    }
    lookup_field : PUT or DELETE, 定义的字段
    pagination_class : 自定义分页
},
自定义异常 : [ "Create", "Put" ]
"""
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,DestroyModelMixin,
    UpdateModelMixin,ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from utils.common.paginations.pagination import MyPagination
from utils.common.base.unitbase import MyUnitBase


class CreateModel(CreateModelMixin,GenericViewSet,MyUnitBase):

    authentication_classes = () # 验证
    permission_classes = () # 权限
    msg_create = "创建成功" # 返回时显示的消息
    results_display = True  # 是否显示序列化信息, 默认显示

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        self.validation_error(serializer=serializer)  # 自定义Serializer异常处理
        # serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)

        data = serializer.data if self.results_display else None #

        return Response({
            "success": True,
            "msg": self.msg_create,
            "results": data
        }, status=status.HTTP_201_CREATED)

class DestroyModel(DestroyModelMixin,GenericViewSet,MyUnitBase):

    authentication_classes = ()
    permission_classes = ()
    msg_delete = "成功删除" # 返回时显示的消息
    lookup_field = "pk"  # 主键

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()
        self.perform_destroy(instance)

        return Response({
            "success": True,
            "msg": self.msg_delete,
            "results": None
        }, status=status.HTTP_200_OK)

class UpdateModel(UpdateModelMixin,GenericViewSet,MyUnitBase):

    authentication_classes = ()
    permission_classes = ()
    msg_update = "修改成功"
    lookup_field = "pk"  # 主键
    results_display = True

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        self.validation_error(serializer=serializer)  # 自定义Serializer异常处理
        # serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        data = serializer.data if self.results_display else None

        return Response({
            "success": True,
            "msg": self.msg_update,
            "results": data
        }, status=status.HTTP_200_OK)

class ListModel(ListModelMixin,GenericViewSet,MyUnitBase):
    authentication_classes = ()
    permission_classes = ()
    pagination_class = MyPagination  # 分页
    msg_list = "成功获取列表数据"

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response({
            "success": True,
            "msg": self.msg_list,
            "results": serializer.data
        }, status=status.HTTP_200_OK)

class RetrieveModel(RetrieveModelMixin,GenericViewSet,MyUnitBase):

    authentication_classes = ()
    permission_classes = ()
    msg_detail = "成功获取详细数据"
    lookup_field = "pk"  # 主键

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({
            "success": True,
            "msg": self.msg_detail,
            "results": [serializer.data] # 以列表的格式给
        }, status=status.HTTP_200_OK)

class APIViewModel(APIView,MyUnitBase):

    authentication_classes = ()
    permission_classes = ()
    msg_api = "POST API"

    def post(self,request):
        # serializer = self.get_serializer(data=request.data)
        # self.validation_error(serializer=serializer)  # 自定义Serializer异常处理
        return Response({
            "success": False,
            "msg": "基类POST,请重新封装",
            "results": ""
        }, status=status.HTTP_400_BAD_REQUEST)
