from rest_framework import serializers
from .models import Dish, Tag
from accounts.models import Restaurant # noqa


class DishSerializers:
    class DishBaseSerializer(serializers.ModelSerializer):
        restaurant = serializers.PrimaryKeyRelatedField(
            queryset=Restaurant.objects.all(),
            write_only=True
        )
        name: str = serializers.CharField(max_length=50, required=True)
        price: float = serializers.DecimalField(max_digits=5, decimal_places=2, required=True)
        description: str = serializers.CharField(allow_blank=True)

        tags: list[str] = serializers.ListField(
            child=serializers.CharField(), write_only=True
        )

        class Meta:
            model = Dish
            fields = ["restaurant", 'id', 'name', 'price', 'description', 'tags']

        def validate_restaurant(self, restaurant):
            request = self.context.get("request")
            if restaurant.owner != request.user:
                raise serializers.ValidationError("You are not the owner of this restaurant.")
            return restaurant

        def to_representation(self, instance):
            rep = super().to_representation(instance)
            rep["tags"] = [tag.name for tag in instance.tags.all()]
            return rep

    class DishCreateSerializer(DishBaseSerializer):
        def create(self, validated_data):

            tag_names = validated_data.pop('tags', [])
            dish = Dish.objects.create(**validated_data)

            tag_objects = []
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name)
                tag_objects.append(tag)

            dish.tags.set(tag_objects)
            return dish

    class DishUpdateSerializer(DishBaseSerializer):
        def update(self, instance, validated_data):
            tag_names = validated_data.pop('tags', None)
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            if tag_names is not None:
                tag_objects = []
                for name in tag_names:
                    tag, _ = Tag.objects.get_or_create(name=name)
                    tag_objects.append(tag)
                instance.tags.set(tag_objects)

            return instance

    class DishDetailSerializer(DishBaseSerializer):
        pass

    class DishListSerializer(DishBaseSerializer):
        pass

dish_serializers = DishSerializers()

