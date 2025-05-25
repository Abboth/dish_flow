from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Restaurant

User = get_user_model()


class RestaurantSerializers:
    class RestaurantBaseSerializer(serializers.ModelSerializer):
        name = serializers.CharField(max_length=50, required=True)
        city = serializers.CharField(max_length=32, required=True)
        address = serializers.CharField(max_length=100, required=True)

        class Meta:
            model = Restaurant
            fields = ["name", "city", "address"]

        def to_representation(self, instance):
            owner = user_serializers.UserDetailSerializer(instance.owner).data
            return {
                "id": instance.id,
                "name": instance.name,
                "city": instance.city,
                "address": instance.address,
                "owner": owner
            }

    class RestaurantCreateSerializer(RestaurantBaseSerializer):
        def create(self, validated_data):
            validated_data['owner'] = self.context['request'].user
            return Restaurant.objects.create(**validated_data)

    class RestaurantUpdateSerializer(RestaurantBaseSerializer):
        pass

    class RestaurantListSerializer(RestaurantBaseSerializer):
        class Meta:
            model = Restaurant
            fields = ["id", "name", "city", "address", "owner"]

    class RestaurantDetailSerializer(RestaurantBaseSerializer):
        class Meta:
            model = Restaurant
            fields = ["id", "name", "city", "address", "owner"]


class UserSerializers:
    class UserGetBaseSerializer(serializers.ModelSerializer):
        email = serializers.EmailField(max_length=50, required=True)
        username = serializers.CharField(max_length=20, required=True)
        password = serializers.CharField(min_length=8, max_length=12, required=True, write_only=True)
        first_name = serializers.CharField(max_length=20, required=True)
        last_name = serializers.CharField(max_length=25, required=True)

        class Meta:
            model = User
            fields = ["id", "email", "first_name", "last_name", "is_restaurant", "is_driver", "is_customer"]

    class UserCreateSerializer(UserGetBaseSerializer):
        class Meta:
            model = User
            fields = ["username", "email", "password"]

        def create(self, validated_data):
            return User.objects.create_user(**validated_data)

        def to_representation(self, instance):
            return {
                "id": instance.id,
                "email": instance.email,
                "status": 'created'
            }

    class UserUpdateSerializer(UserGetBaseSerializer):
        class Meta:
            model = User
            fields = ["first_name", "last_name"]

        def to_representation(self, instance):
            return {
                "id": instance.id,
                "email": instance.email,
                "status": 'updated'
            }

    class UserListSerializer(UserGetBaseSerializer):
        pass

    class UserDetailSerializer(UserGetBaseSerializer):
        pass


user_serializers = UserSerializers()
restaurant_serializers = RestaurantSerializers()
