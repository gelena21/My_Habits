from rest_framework import serializers

from habits.models import Habit
from habits.validators import (
    RewardHabitValidator,
    HabitRelatedIsNiceValidator,
    NiceHabitValidator,
    DurationValidator,
    PeriodicValidator,
)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            RewardHabitValidator("related_habit", "reward"),
            HabitRelatedIsNiceValidator("related_habit"),
            NiceHabitValidator("related_habit", "reward",
                               "is_nice"),
            DurationValidator("time_duration"),
            PeriodicValidator("periodicity"),
        ]
