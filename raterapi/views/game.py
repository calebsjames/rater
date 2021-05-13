from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from raterapi.models import Game, Gamer, Category
from django.contrib.auth.models import User


class GameViewSet(ViewSet):
    
    # Get a single record
    def retrieve(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            # categories = Category.objects.filter(categorygame__)
            
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        
        except Exception as ex:
            return HttpResponseServerError(ex)
    

    # Get a list of all records
    def list(self, request):
        games = Game.objects.all()
        

        serializer = GameSerializer(
            games, many=True, context={'request': request})
        return Response(serializer.data)


    # Get a list of all records
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """

        # Uses the token passed in the `Authorization` header
        gamer = Gamer.objects.get(user=request.auth.user)

        
        game = Game()
        game.ages = request.data["ages"]
        game.description = request.data["description"]
        game.est_time = request.data["est_time"]
        game.maker = request.data["maker"]
        game.number_of_players = request.data["number_of_players"]
        game.title = request.data["title"]
        game.year = request.data["year"]
        

        # Use the Django ORM to get the record from the database
        # whose `id` is what the client passed as the
        # `gameTypeId` in the body of the request.
        # gametype = GameType.objects.get(pk=request.data["gameTypeId"])
        # game.gametype = gametype

        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request
        try:
            game.save()
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
    
    


    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        gamer = Gamer.objects.get(user=request.auth.user)

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game, get the game record
        # from the database whose primary key is `pk`
        game = Game.objects.get(pk=pk)
        game.ages = request.data["ages"]
        game.description = request.data["description"]
        game.est_time = request.data["est_time"]
        game.maker = request.data["maker"]
        game.number_of_players = request.data["number_of_players"]
        game.title = request.data["title"]
        game.year = request.data["year"]

        # gametype = GameType.objects.get(pk=request.data["gameTypeId"])
        # game.gametype = gametype
        game.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)
   

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            game = Game.objects.get(pk=pk)
            game.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')
        

class GameSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Game
        fields = ('id', 'ages', 'description', 'est_time', 'maker', 'number_of_players', 'title', 'year', 'categories')
        depth = 1