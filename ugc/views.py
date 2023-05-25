from rest_framework.viewsets import ModelViewSet

from ugc.models.score import ScoreItem
from ugc.models.tag import Tag, TaggedItem
from ugc.models.topic import TopicItem
from ugc.serializers.score_serializers import ScoreItemSerializer
from ugc.serializers.tag_serializers import TagSerializer, TaggedItemSerializer
from ugc.serializers.topic_serializers import TopicItemSerializer


# Create your views here.
class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    # permission_classes = [permissions.IsAuthenticated]


class TaggedItemViewSet(ModelViewSet):
    queryset = TaggedItem.objects.select_related('tag').all()
    serializer_class = TaggedItemSerializer

    # permission_classes = [permissions.IsAuthenticated]


class TopicItemViewSet(ModelViewSet):
    queryset = TopicItem.objects.select_related('topic').all()
    serializer_class = TopicItemSerializer

    # permission_classes = [permissions.IsAuthenticated]
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title', 'description']
    # ordering_fields = ['title', 'description']


class ScoreItemViewSet(ModelViewSet):
    queryset = ScoreItem.objects.all()
    serializer_class = ScoreItemSerializer

    # permission_classes = [permissions.IsAuthenticated]
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title', 'description']
    # ordering_fields = ['title', 'description']
