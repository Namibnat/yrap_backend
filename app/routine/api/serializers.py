from rest_framework import serializers


from routine.models import (
    Author, JustDoIt, StudyChunkScoreCard
)


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = "__all__"


class StudyChunkScoreCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudyChunkScoreCard
        fields = "__all__"


class JustDoItSerializer(serializers.ModelSerializer):

    class Meta:
        model = JustDoIt
        fields = "__all__"
