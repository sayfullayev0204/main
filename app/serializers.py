from rest_framework import serializers
from .models import Service, ServiceCategory, ServiceImage, Village, CustomUser, Citizn, Leave, PersonalStatus, PersonalCategroy, Apartment

class VillageSerializer(serializers.ModelSerializer):
    district = serializers.SerializerMethodField()

    class Meta:
        model = Village
        fields = ['id', 'name', 'district']
    
    def get_district(self, obj):
        return {
            "id": obj.district.id,
            "name": obj.district.name,
            "region": {
                "id": obj.district.region.id,
                "name": obj.district.region.name
            }
        }

class CitiznVillageSerializer(serializers.ModelSerializer):
    district = serializers.CharField(source="district.name", read_only=True)
    region = serializers.CharField(source="district.region.name", read_only=True)

    class Meta:
        model = Village
        fields = ["id", "name", "district", "region"]

class CustomUserSerializer(serializers.ModelSerializer):
    village = VillageSerializer()

    class Meta:
        model = CustomUser
        fields = ["id", "jshshir", "username", "first_name", "last_name", "role", "birthday", 
                  "gender", "phone", "address", "rank", "photo", "village", "nation", 
                  "position", "work_addres"]

class LeaveSerializer(serializers.ModelSerializer):
    goal = serializers.CharField(source="goal.name", read_only=True)
    work_field = serializers.CharField(source="work_field.name", read_only=True)
    state = serializers.CharField(source="state.name", read_only=True)

    class Meta:
        model = Leave
        fields = [
            "id", "start_add_date", "end_add_date", "start_leave_date", 
            "end_leave_date", "deadline", "goal", "work_field", "state", 
            "address", "start_come_date", "end_come_date", "reason_come", 
            "deport", "violation"
        ]

class PersonalStatusSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = PersonalStatus
        fields = ["id", "category", "count"]

class CitiznBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citizn
        fields = ["id", "first_name", "last_name", "middle_name", "phone"]

class ApartmentSerializer(serializers.ModelSerializer):
    village = VillageSerializer(read_only=True)

    class Meta:
        model = Apartment
        fields = ["id", "name", "village", "area"]

class ApartmentDetailSerializer(serializers.ModelSerializer):
    village = VillageSerializer(read_only=True)
    citizen_count = serializers.SerializerMethodField()
    personal_status_summary = serializers.SerializerMethodField()
    xonadon_egasi = serializers.SerializerMethodField()

    class Meta:
        model = Apartment
        fields = ["id", "name", "village", "area", "citizen_count", "personal_status_summary", "xonadon_egasi"]

    def get_citizen_count(self, obj):
        return obj.citizens.count()

    def get_personal_status_summary(self, obj):
        from django.db.models import Sum
        personal_statuses = PersonalStatus.objects.filter(citzen__apartment=obj)  # Changed 'citizen' to 'citzen'
        summary = personal_statuses.values('category__name').annotate(total_count=Sum('count')).order_by('category__name')
        return [
            {"category": item['category__name'], "total_count": item['total_count']}
            for item in summary
        ]

    def get_xonadon_egasi(self, obj):
        try:
            landlord = obj.citizens.get(landlord=True)
            return CitiznBasicSerializer(landlord).data  # Use lightweight serializer
        except Citizn.DoesNotExist:
            return None

class CitiznSerializer(serializers.ModelSerializer):
    village = CitiznVillageSerializer(source="Village", read_only=True)
    leave = LeaveSerializer(source="leaves", many=True, read_only=True)
    personal_status = PersonalStatusSerializer(source="personal_statuses", many=True, read_only=True)
    apartment = serializers.CharField(source="apartment.name", read_only=True, allow_null=True)

    class Meta:
        model = Citizn
        fields = [
            "id", "first_name", "last_name", "middle_name", "birthday", "phone", 
            "gender", "photo", "marital_status", "children_count", "income_level",
            "employment_status", "house_ownership", "is_at_risk", "needs_support", 
            "under_supervision", "village", "leave", "personal_status", "apartment"
        ]


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ["id", "name"]

class ServiceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceImage
        fields = ["id", "image"]

class ServiceDetailSerializer(serializers.ModelSerializer):
    category = ServiceCategorySerializer(read_only=True)
    images = ServiceImageSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = ["category", "description", "created_at", "images"]

class ServiceSerializer(serializers.ModelSerializer):
    service = ServiceDetailSerializer(source='*', read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceCategory.objects.all(), source="category", write_only=True
    )
    image_files = serializers.ListField(
        child=serializers.ImageField(), write_only=True, max_length=5, required=True
    )

    class Meta:
        model = Service
        fields = ["id", "service", "category_id", "image_files"]

    def validate_image_files(self, value):
        if len(value) > 5:
            raise serializers.ValidationError("Maximum 5 images allowed.")
        return value

    def create(self, validated_data):
        image_files = validated_data.pop("image_files")
        user = self.context["request"].user
        service = Service.objects.create(user=user, **validated_data)
        for image_file in image_files:
            ServiceImage.objects.create(service=service, image=image_file)
        return service