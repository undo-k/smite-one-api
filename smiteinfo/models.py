import pandas as pd
from django.db import models
from django.db.models import Count, ExpressionWrapper, fields, Avg
from django.urls import reverse
from sklearn.linear_model import LogisticRegression


class Item(models.Model):
    """Model representing a standard purchasable Smite Item."""

    name = models.CharField(max_length=64, unique=True, null=False)
    image = models.ImageField(upload_to="images/", null=True)
    damage_types = [("Magical", "Magical"), ("Physical", "Physical"), ("Both", "Both")]
    damage_type = models.CharField(max_length=64, choices=damage_types, blank=True)

    def __str__(self):
        return self.name


# Create your models here.
class God(models.Model):
    """Model representing a Smite God/Champion."""

    damage_types = [("Magical", "Magical"), ("Physical", "Physical")]

    roles = [
        ("Assassin", "Assassin"),
        ("Guardian", "Guardian"),
        ("Hunter", "Hunter"),
        ("Mage", "Mage"),
        ("Warrior", "Warrior"),
    ]

    name = models.CharField(primary_key=True, max_length=64, unique=True, null=False)
    role = models.CharField(max_length=64, choices=roles, null=False)
    damage_type = models.CharField(max_length=64, choices=damage_types, blank=True)
    win_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    pick_rate = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    ban_rate = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    prev_win_rate = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    prev_pick_rate = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    prev_ban_rate = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    top_items = models.ManyToManyField(Item, blank=True, related_name="top_items_set")
    lr_top_items = models.ManyToManyField(
        Item, blank=True, related_name="lr_top_items_set"
    )

    def save(self, *args, **kwargs):
        role_to_damage_type = {
            "Assassin": "Physical",
            "Guardian": "Magical",
            "Hunter": "Physical",
            "Mage": "Magical",
            "Warrior": "Physical",
        }

        self.damage_type = role_to_damage_type.get(self.role, "")
        self.win_rate = self.calculate_win_rate()
        self.pick_rate = self.calculate_pick_rate()
        self.ban_rate = self.calculate_ban_rate()
        self.top_items.set(self.calculate_top_items())
        self.lr_top_items.set(self.calculate_lr_top_items())

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("god-detail", args=[str(self.name).lower()])

    def calculate_win_rate(self):
        match_players = self.matchplayer_set
        match_players_count = match_players.count()
        if match_players_count != 0:
            return round(
                (match_players.filter(won=True).count() / match_players_count) * 100, 2
            )
        else:
            return 0.00

    def calculate_ban_rate(self):
        total_match_count = Match.objects.count()
        god_banned_match_count = Match.objects.filter(banned_gods__in=[self]).count()

        if total_match_count != 0:
            return round((god_banned_match_count / total_match_count) * 100, 2)
        else:
            return 0.00

    def calculate_pick_rate(self):
        total_match_count = Match.objects.count()
        god_picked_match_count = (
            Match.objects.filter(matchplayer__god=self).distinct().count()
        )

        if total_match_count != 0:
            return round((god_picked_match_count / total_match_count) * 100, 2)
        else:
            return 0.00

    def calculate_top_items(self, item_count=6):
        # items = self.matchplayer_set.filter(items__isnull=False).values("items")
        items = Item.objects.filter(matchplayer__god=self)
        # items = self.matchplayer_set.prefetch_related("god__matchplayer_set__items").values("items")
        items = items.annotate(
            win_rate=ExpressionWrapper(
                Count("id", filter=models.Q(matchplayer__won=True)) / Count("id") * 100,
                output_field=fields.FloatField(),
            )
        )
        return items.order_by("-win_rate")[:item_count]

    def calculate_lr_top_items(self):
        # print("in god: " + self.name)
        num_match_players = len(self.matchplayer_set.all().values("won").distinct())
        if num_match_players < 2:
            return Item.objects.none()
        match_players = list(
            self.matchplayer_set.all().values("id", "match_id", "won", "items")
        )
        damage_types = ["Both", self.damage_type]
        all_item_pks = list(
            Item.objects.filter(damage_type__in=damage_types)
            .values_list("id", flat=True)
            .distinct()
        )
        filtered_mps = {}
        for match_player in match_players:
            mpid = match_player["id"]
            if mpid in filtered_mps:
                filtered_mps[mpid]["items"].append(match_player["items"])
            else:
                filtered_mps[mpid] = {
                    "id": mpid,
                    "match_id": match_player["match_id"],
                    "won": match_player["won"],
                    "items": [match_player["items"]],
                }
        filtered_mps = list(filtered_mps.values())
        # print(filtered_mps)

        normalized_data = {"match_id": [], "won": []}
        for item_pk in all_item_pks:
            if item_pk not in normalized_data:
                normalized_data[item_pk] = []

        for mp in filtered_mps:
            match_id = mp["match_id"]

            normalized_data["match_id"].append(match_id)
            normalized_data["won"].append(mp["won"])
            for item_pk in all_item_pks:
                if item_pk not in mp["items"]:
                    normalized_data[item_pk].append(0)
                else:
                    normalized_data[item_pk].append(1)

        # print(normalized_data)
        df = pd.DataFrame(normalized_data)

        # print(df)

        x = df.drop(["match_id", "won"], axis=1)
        y = df["won"]

        log_regression = LogisticRegression()

        log_regression.fit(x, y)
        coefficients = log_regression.coef_[0]
        x_item_pks = x.columns
        coefficients_df = pd.DataFrame(
            {"Item": x_item_pks, "Coefficient": coefficients}
        )
        coefficients_df = coefficients_df.sort_values(by="Coefficient", ascending=False)
        # print(coefficients_df)
        top_items = coefficients_df.head(6)["Item"].tolist()
        item_dict = Item.objects.in_bulk(top_items)
        queryset = Item.objects.filter(name__in=item_dict.values())

        # print(queryset)

        # list comp for ONLY match_players with finished builds
        # use as an alternative to padding out unfinished builds
        # filtered_mps = [mp for mp in filtered_mps if len(mp["items"]) == 6]

        return queryset

    def avg_kills(self):
        return MatchPlayerDetail.objects.filter(match_player__god=self).aggregate(
            avg_kills=Avg("kills")
        )["avg_kills"]

    def avg_deaths(self):
        return MatchPlayerDetail.objects.filter(match_player__god=self).aggregate(
            avg_deaths=Avg("deaths")
        )["avg_deaths"]

    def avg_assists(self):
        return MatchPlayerDetail.objects.filter(match_player__god=self).aggregate(
            avg_assists=Avg("assists")
        )["avg_assists"]

    def avg_gold(self):
        return MatchPlayerDetail.objects.filter(match_player__god=self).aggregate(
            avg_gold=Avg("gold")
        )["avg_gold"]

    def avg_player_dmg(self):
        return MatchPlayerDetail.objects.filter(match_player__god=self).aggregate(
            avg_player_dmg=Avg("player_damage")
        )["avg_player_dmg"]

    def avg_minion_dmg(self):
        return MatchPlayerDetail.objects.filter(match_player__god=self).aggregate(
            avg_minion_dmg=Avg("minion_damage")
        )["avg_minion_dmg"]

    def avg_dmg_taken(self):
        return MatchPlayerDetail.objects.filter(match_player__god=self).aggregate(
            avg_dmg_taken=Avg("damage_taken")
        )["avg_dmg_taken"]

    def avg_dmg_mitigated(self):
        return MatchPlayerDetail.objects.filter(match_player__god=self).aggregate(
            avg_dmg_mitigated=Avg("damage_mitigated")
        )["avg_dmg_mitigated"]

    def avg_structure_dmg(self):
        return MatchPlayerDetail.objects.filter(match_player__god=self).aggregate(
            avg_structure_dmg=Avg("structure_damage")
        )["avg_structure_dmg"]

    def avg_player_healing(self):
        return MatchPlayerDetail.objects.filter(match_player__god=self).aggregate(
            avg_player_healing=Avg("player_healing")
        )["avg_player_healing"]

    def avg_kda(self):
        return (self.avg_kills() + self.avg_assists()) / (
            self.avg_deaths() if self.avg_deaths() > 0 else 1
        )

    def __str__(self):
        return self.name


class Match(models.Model):
    """Model representing a Smite Match."""

    modes = [
        ("Arena", "Arena"),
        ("Assault", "Assault"),
        ("Conquest", "Conquest"),
        ("Joust", "Joust"),
        ("Slash", "Slash"),
    ]

    teams = [
        ("Chaos", "Chaos"),
        ("Order", "Order"),
    ]

    id = models.PositiveBigIntegerField(primary_key=True)
    game_mode = models.CharField(max_length=64, choices=modes)
    match_date = models.DateField()
    winning_team = models.CharField(max_length=64, choices=teams)
    banned_gods = models.ManyToManyField(God, blank=True)

    def __str__(self):
        return str(self.id) + "-" + self.game_mode


class MatchPlayer(models.Model):
    """Model representing a Player in a Smite Match."""

    teams = [
        ("Chaos", "Chaos"),
        ("Order", "Order"),
    ]

    # General match info
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.CharField(max_length=64, choices=teams)

    # General god info
    god = models.ForeignKey(God, on_delete=models.PROTECT)
    items = models.ManyToManyField(Item)

    won = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.team == self.match.winning_team:
            self.won = True
        else:
            self.won = False
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.match.id) + "-" + self.team + "-" + self.god.name


class MatchPlayerDetail(models.Model):
    """Model representing Player performance details in a Smite Match."""

    match_player = models.OneToOneField(MatchPlayer, on_delete=models.CASCADE)
    kills = models.PositiveIntegerField()
    deaths = models.PositiveIntegerField()
    assists = models.PositiveIntegerField()
    gold = models.PositiveIntegerField()
    player_damage = models.PositiveIntegerField()
    minion_damage = models.PositiveIntegerField()
    damage_taken = models.PositiveIntegerField()
    damage_mitigated = models.PositiveIntegerField()
    structure_damage = models.PositiveIntegerField()
    player_healing = models.PositiveIntegerField()

    def __str__(self):
        return str(self.match_player)
