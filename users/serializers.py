from rest_framework import serializers

from users.models import User, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class UserLocationSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=True)

    class Meta:
        model = User
        fields = ['username', 'location']


class UserSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=True)

    # location = serializers.SlugRelatedField(many=True, slug_field="name", queryset=Location.objects.all())
    class Meta:
        model = User
        exclude = ['password']


class UserListSerializer(serializers.ModelSerializer):
    total_ads = serializers.IntegerField()

    class Meta:
        model = User
        exclude = ['password', 'location']


class UserCreateSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(required=False, many=True, slug_field="name",
                                            queryset=Location.objects.all())

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        # user = User.objects.create(**validated_data)
        user = super().create(validated_data)

        # for loc in self._locations:
        #     loc, created = Location.objects.get_or_create(name=loc)
        #     user.location.add(loc)
        #
        # user.set_password(user.password)
        # user.save()

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(required=False, many=True, slug_field="name",
                                            queryset=Location.objects.all())

    class Meta:
        model = User
        fields = '__all__'

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    created = serializers.DateField(read_only=True)

    def is_valid(self, *, raise_exception=False):
        self._locations = self.initial_data.pop("location", [])
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        user = super().save()

        for loc in self._locations:
            loc, _ = Location.objects.get_or_create(name=loc)
            user.location.add(loc)

        user.save()
        return user
