from typing import Optional

from django.contrib.auth import get_user_model
from django.template.context_processors import request
from jsonschema.validators import validate
from rest_framework import serializers

from .models import Order, OrderItem
from accounts.models import Restaurant

from menu.models import Dish

User = get_user_model()


class OrderItemSerializer(serializers.ModelSerializer):
    dish_name = serializers.CharField(source="dish.name", read_only=True)
    dish_price = serializers.DecimalField(source="dish.price", max_digits=6, decimal_places=2, read_only=True)
    restaurant = serializers.CharField(source="dish.restaurant.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["dish_name", "dish_price", "restaurant", "quantity"]

class OrderItemCreateSerializer(serializers.Serializer):
    dish = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all())
    quantity = serializers.IntegerField(min_value=1)

class OrderSerializers:
    class OrderBaseSerializer(serializers.ModelSerializer):
        restaurant: Restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())
        user = serializers.HiddenField(default=None)

        delivery_address: Optional[str] = serializers.CharField(max_length=100, required=False)
        customer_email: Optional[str] = serializers.EmailField(max_length=50, required=False)
        customer_phone: str = serializers.CharField(max_length=20, required=True)

        total_price: float = serializers.HiddenField(default=0.0)

        order_items = OrderItemSerializer(many=True, read_only=True)

        class Meta:
            model = Order
            fields = [
                "id", "restaurant", "user", "delivery_address", "customer_email",
                "customer_phone", "order_items", "total_price", "status"
            ]

        def validate(self, attrs):
            if not attrs.get("customer_phone"):
                raise serializers.ValidationError("Customer phone number is required.")

            return attrs

    class OrderCreateSerializer(OrderBaseSerializer):
        order_items = OrderItemCreateSerializer(many=True, write_only=True)

        def create(self, validated_data):
            request = self.context.get("request")
            order_items_data = validated_data.pop("order_items")
            validated_data["user"] = request.user if request and request.user.is_authenticated else None
            order = Order.objects.create(**validated_data)

            total = 0
            for item_data in order_items_data:
                dish = item_data["dish"]
                quantity = item_data["quantity"]
                OrderItem.objects.create(order=order, dish=dish, quantity=quantity)
                total += dish.price * quantity

            order.total_price = total
            order.save()

            return order

    class OrderUpdateSerializer(OrderBaseSerializer):
        pass

    class OrderDetailSerializer(OrderBaseSerializer):
        pass

    class OrderListSerializer(OrderBaseSerializer):
        pass

order_serializers = OrderSerializers()