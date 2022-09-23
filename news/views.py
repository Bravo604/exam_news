from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from .serializers import NewsSerializer, CommentSerializer, StatusSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from .models import News, Comment, NewsStatus, CommentStatus, Status

from .permissions import IsAuthorPermission, IsStuffPermission


# from .paginations import StandardPagination


class NewsViewSet(ModelViewSet):
    serializer_class = NewsSerializer
    queryset = News.objects.all()
    authentication_classes = [SessionAuthentication, TokenAuthentication, ]
    permission_classes = [IsAuthorPermission, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author)

    def get_queryset(self):
        return self.queryset


class NewsUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthorPermission, ]


class CommentListCreateAPIView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication, ]
    permission_classes = [IsAuthorPermission, ]

    # pagination_class = StandardPagination

    def get_queryset(self):
        return self.queryset.filter(news_id=self.kwargs['news_id'])

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user.author,
            news=get_object_or_404(News, id=self.kwargs['news_id'])
        )


class CommentRetrieveDestroyUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication, ]
    permission_classes = [IsAuthorPermission, ]


class StatusViewSet(ModelViewSet):
    serializer_class = StatusSerializer
    queryset = Status.objects.all()
    authentication_classes = [SessionAuthentication, TokenAuthentication, ]
    permission_classes = [IsStuffPermission, ]

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        return self.queryset


class StatusUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsStuffPermission, ]


class NewsStatusView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, ]

    def get(self, request, news_id, status_slug):
        news = get_object_or_404(News, id=news_id)
        news_status = get_object_or_404(Status, slug=status_slug)
        try:
            statuses = NewsStatus.objects.create(news=news, author=request.user.author, status=news_status)
        except IntegrityError:
            statuses = NewsStatus.objects.get(news=news, author=request.user.author)
            if statuses.status == news_status:
                statuses.status = None
            else:
                statuses.status == news_status
            statuses.save()
            data = {
                'message': f'{news_id} changed status by {request.user.author}'
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                'message': f'news {news_id} got status from {request.user.author}'
            }
            return Response(data, status=status.HTTP_201_CREATED)


class CommentStatusView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, ]

    def get(self, request, news_id, comment_id, status_slug):
        comments = get_object_or_404(Comment, id=comment_id)
        comment_status = get_object_or_404(Status, slug=status_slug)
        try:
            statuses = CommentStatus.objects.create(comment=comments, author=request.user.author, status=comment_status)
        except IntegrityError:
            statuses = CommentStatus.objects.get(comment=comments, author=request.user.author)
            if statuses.status == comment_status:
                statuses.status = None
            else:
                statuses.status == comment_status
            statuses.save()
            data = {
                'message': f'{comment_id} changed status by {request.user.author}'
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                'message': f'comment {comment_id} got status from {request.user.author}'
            }
            return Response(data, status=status.HTTP_201_CREATED)
