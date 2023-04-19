from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import SearchResult,BookList,Profile,BookComment,Rating
from api.serializers import SearchResultSerializer,BookListSerializer,ProfileSerializer,CommentSerializer,RatingSerializer
import requests
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import generics, permissions

search_url = "https://api.nytimes.com/svc/books/v3/reviews.json?"
main_url = "https://api.nytimes.com/svc/books/v3/lists/full-overview.json?api-key=TfdRGKWnppkgBQKL77qKyQfT9GzR0JqN"

class CreateUserView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_409_CONFLICT)
        user = User.objects.create_user(username, email, password)
        profile = Profile.objects.create(user=user)
        profile.save()

        user.save()
        return Response({'success': 'User created'}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        print("::::::::::::::::::::::::;;",request)
        username = request.data.get('username')
        password = request.data.get('password')
        print("::::::::",username)
        print(":::::::::::",password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("::::::::::;login user::::::::::::")
            login(request, user)
            profile = Profile.objects.get(user=user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'success': 'Logged out'})

class MainView(APIView):
    queryset = BookList.objects.all()
    serializer_class = BookListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get(self, request):

        response = requests.get(main_url)

        # Handle any errors that occurred during the request
        if response.status_code != 200:
            return Response({'error': 'Failed to retrieve search results'})

        # Parse the JSON data returned by the third-party API
        data = response.json().get('results').get('lists')

        # Map the search results to a list of SearchResult objects
        results = []
        for result in data:
            book_list = result.get('books')
            for book in book_list:
                book_result = BookList(
                    title=book.get('title'),
                    author=book.get('author'),
                    book_image=book.get('book_image'),
                    description=book.get('description'),
                    publisher=book.get('publisher'),
                    # Map any other fields you want to store
                )
                book_result.save()
                results.append(book_result)


        # Serialize the search results and return them as a JSON response
        serializer = BookListSerializer(results, many=True)
        return Response(serializer.data)


class SearchView(APIView):
    def get(self, request):
        query = request.GET.get('q')
        print("*****************************************",query)
        if not query:
            return Response({'error': 'Missing search query parameter'})

        # Replace `https://example.com/search?q={}` with the URL of the third-party API
        url = search_url+"author="+query+"&api-key=TfdRGKWnppkgBQKL77qKyQfT9GzR0JqN"
        print("&&&&&&&&&&&&&&&&&&",url)
        response = requests.get(url)
        print(response)

        # Handle any errors that occurred during the request
        if response.status_code != 200:
            return Response({'error': 'Failed to retrieve search results'})

        # Parse the JSON data returned by the third-party API
        data = response.json().get('results')

        print(data)

        # Map the search results to a list of SearchResult objects
        results = []
        for result in data:
            print(":::::",result.get('book_title'))
            search_result = SearchResult(
                title=result.get('book_title'),
                author=result.get('book_author'),
                publication_dt=result.get('publication_dt'),
                url=result.get('url'),
                description=result.get('summary'),
                # Map any other fields you want to store
            )
            results.append(search_result)

        # Serialize the search results and return them as a JSON response
        serializer = SearchResultSerializer(results, many=True)
        return Response(serializer.data)

class CommentCreateAPIView(generics.CreateAPIView):
    queryset = BookComment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RatingCreateAPIView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)