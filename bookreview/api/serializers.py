from rest_framework import serializers
from api.models import SearchResult, BookList, Profile, BookComment, Rating


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class SearchResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchResult
        fields = ('title', 'author', 'publication_dt', 'url', 'description')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

class BookListSerializer(serializers.ModelSerializer):
    comments = RatingSerializer(many=True, read_only=True)
    total_ratings = serializers.SerializerMethodField()
    class Meta:
        model = BookList
        fields = ('title', 'author', 'book_image', 'description', 'publisher','total_ratings','comments')

    def get_total_ratings(self, obj):
        ratings = obj.ratings.all()
        if ratings:
            total_rating = sum(rating.value for rating in ratings)
            return total_rating / len(ratings)
        else:
            return None
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookComment

        fields = '__all__'
