from rest_framework import serializers
from wiki.models.article import Article

class ArticleSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'id', 'created', 'modified', 'current_revision',
            'owner', 'title', 'content' 
        ]

    def get_title(self, obj):
        return obj.current_revision.title if obj.current_revision else ''

    def get_content(self, obj):
        return obj.current_revision.content if obj.current_revision else ''
