from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.

class TileTemplate(models.Model):
    letter = models.CharField(max_length = 1)
    point_value = models.IntegerField(default = 0)

class Game(models.Model):
    name = models.CharField(max_length = 16)
    num_players = models.PositiveIntegerField(default = 2)

class User(models.Model):
    name = models.CharField(max_length = 16)
    games = models.ManyToManyField(
        Game,
        through = 'GamePlayer',
        through_fields = ['user', 'game']
        )

class GamePlayer(models.Model):
    """ A single user in a game. """

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    order = models.PositiveIntegerField(
        validators = [
            MaxValueValidator(3),]
        )

    score = models.PositiveIntegerField()

    class Meta:
        ordering = ['order',]


class Square(models.Model):
    tile = models.ForeignKey(
        'Tile', 
        on_delete = models.SET_NULL,
        blank = True,
        null = True)

class Tile(models.Model):
    TILE_CONTAINERS = (
        ('BO', 'Board'),
        ('BA', 'Bag'),
        ('P1', 'Player 1'),
        ('P2', 'Player 2'),
        ('P3', 'Player 3'),
        ('P4', 'Player 4'),
    )
    game = models.ForeignKey(Game, on_delete = models.CASCADE)
    tile_template = models.ForeignKey(TileTemplate, on_delete = models.PROTECT)

    # Owner is either a player, the bag, or the board
    owner = models.CharField(max_length = 2, choices = TILE_CONTAINERS)
    # Position within its owner
    position = models.IntegerField(default = 0)

    class Meta:
        indexes = [
            models.Index(fields=['owner', 'position'])
        ]





