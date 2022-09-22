from rest_framework import serializers

from .models import News, Comment, Status


class NewsSerializer(serializers.ModelSerializer):
    news_username = serializers.ReadOnlyField()
    get_status = serializers.ReadOnlyField()

    class Meta:
        model = News
        fields = '__all__'
        read_only_fields = ['author', ]


class CommentSerializer(serializers.ModelSerializer):
    comment_username = serializers.ReadOnlyField()
    get_status = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['comment', 'news', ]


class StatusSerializer(serializers.ModelSerializer):
    status_username = serializers.ReadOnlyField()

    class Meta:
        model = Status
        fields = '__all__'
        # read_only_fields = ['comment', 'news', ]
