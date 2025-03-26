from django.db import models
from django.core.exceptions import ValidationError

from utils.generators import unique_slugify
from utils.generic_numgen import unique_gen


PLAYER_POSITION = (
    ("GK", "Goalkeeper"),
    ("CB", "Centre Back"),
    ("LCB", "Left Centre Back"),
    ("RCB", "Right Centre Back"),
    ("RB", "Right Back"),
    ("LB", "Left Back"),
    ("CM", "Center Midfield"),
    ("CDM", "Center Defensive Midfield"),
    ("CAM", "Center Attacking Midfield"),
    ("LAM", "Left Attacking Midfield"),
    ("RAM", "Right Attacking Midfield"),
    ("LWB", "Left Wing Back"),
    ("RWB", "Right Wing Back"),
    ("ST", "Striker"),
    ("CF", "Center Forward"),
    ("LW", "Left Wing"),
    ("RW", "Right Wing"),
)

COMPETITION_CHOICES = (
    ("NLWL Winter League", "NLWL Winter League"),
    ("Fintan Goss Cup", "Fintan Goss Cup"),
    ("Summer League", "Summer League"),
    ("Cup", "Cup"),
    ("Friendly", "Friendly"),
    ("Tournament", "Tournament"),
    ("Training", "Training"),
)


MINUTES_CHOICES = [(i, f"{i}'") for i in range(1, 121)]

EVENT_CHOICES = (
    ('GOAL', 'Goal'),
    ('ASSIST', 'Assist'),
    ('YELLOW_CARD', 'Yellow Card'),
    ('RED_CARD', 'Red Card'),
    ('SUBSTITUTION', 'Substitution'),
    ('HALFTIME', 'Halftime'),
    ('FULLTIME', 'Fulltime'),
)


class Player(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    name = models.CharField(max_length=100, blank=True, verbose_name="Preferred Name")
    slug = models.SlugField(null=True, blank=True, unique=True)
    position = models.CharField(max_length=30, blank=True, choices=PLAYER_POSITION)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        new_slug = f"{self.first_name} {self.last_name}"
        unique_slugify(self, new_slug)
        super().save(*args, **kwargs)


class Match(models.Model):
    opposition_team = models.CharField(max_length=250, blank=False, null=False)
    venue = models.CharField(max_length=20, blank=False, null=False)
    match_date = models.DateTimeField()
    slug = models.SlugField(null=True, blank=True, unique=True)
    competition = models.ForeignKey("Competition", on_delete=models.CASCADE)
    line_up = models.JSONField(default=list, blank=True)
    substitutes = models.JSONField(default=list, blank=True)
    # max_substitutions = 5
    

    is_fixture = models.BooleanField(default=True)
    has_result = models.BooleanField(default=False)
    away_fixture = models.BooleanField(default=False)

    class Meta:
        # unique_together = ['match_date']
        ordering = ['match_date']    

    def save(self, *args, **kwargs):
        self.clean()
        new_slug = f"{unique_gen()}"
        unique_slugify(self,new_slug)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.opposition_team} on {self.match_date}"
    
    def clean(self):
        """
        Ensures that no player is both in the starting lineup and substitutes.
        The line-up cannot exceed 11 players.
        """
        if self.line_up.count() > 11:
            raise ValidationError("A starting lineup can have at most 11 players.")
        
        overlap = set(self.line_up) & set(self.substitutes)
        if overlap:
            raise ValidationError(f"Players {', '.join(overlap)} cannot be both in line-up and substitutes.")
    

class Result(models.Model):
    match = models.OneToOneField("Match", on_delete=models.CASCADE)
    opposition_score = models.IntegerField()
    team_score = models.IntegerField()

    def __str__(self):
        return f"{self.match}: {self.opposition_score} - {self.team_score}"
    

class Competition(models.Model):
    category = models.CharField(max_length=120, choices=COMPETITION_CHOICES)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.category} - {self.year}"


# class Formation(models.Model):
#     """
#     Stores different football formations.
#     Example: "4-3-3" (4 Defenders, 3 Midfielders, 3 Forwards)
#     """
#     name = models.CharField(max_length=10, unique=True)  # "4-3-3", "4-4-2"
#     defenders = models.PositiveIntegerField()
#     midfielders = models.PositiveIntegerField()
#     forwards = models.PositiveIntegerField()

#     def total_players(self):
#         """Returns the total number of outfield players + 1 goalkeeper"""
#         return self.defenders + self.midfielders + self.forwards + 1  # +1 for GK

#     def __str__(self):
#         return self.name
    

# class Substitution(models.Model):
#     match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="substitutions")
#     player_out = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="subbed_out")
#     player_in = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="subbed_in")
#     minute = models.PositiveIntegerField()

#     def clean(self):
#         """Ensure substitutions are valid."""
#         if self.player_out == self.player_in:
#             raise ValidationError("A player cannot substitute themselves.")

#         if self.player_out not in self.match.line_up.all():
#             raise ValidationError(f"{self.player_out} is not in the starting lineup.")

#         if self.player_in not in self.match.substitutes.all():
#             raise ValidationError(f"{self.player_in} is not in the substitutes bench.")

#         if self.match.substitutions.count() >= self.match.max_substitutions:
#             raise ValidationError(f"Maximum {self.match.max_substitutions} substitutions allowed.")

#         if not (0 <= self.minute <= 120):  # Extra time included
#             raise ValidationError("Substitution minute must be between 0 and 120.")

#     def save(self, *args, **kwargs):
#         self.clean()
#         # Remove the player_out from the lineup and replace with player_in
#         self.match.line_up.remove(self.player_out)
#         self.match.line_up.add(self.player_in)
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.player_in} replaced {self.player_out} at {self.minute}'"
    


