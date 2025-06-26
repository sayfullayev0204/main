from django.contrib import admin
from .models import CustomUser, Region, District, Village,Citizn,Nation,GoalLeaave,FieldWork,State,Leave,Apartment,PersonalCategroy,PersonalStatus,Service,ServiceCategory,ServiceImage

admin.site.register(CustomUser)
admin.site.register(Region)
admin.site.register(District)
admin.site.register(Village)

admin.site.register(Citizn)
admin.site.register(Nation)
admin.site.register(GoalLeaave)
admin.site.register(FieldWork)
admin.site.register(State)
admin.site.register(Leave)
admin.site.register(Apartment)
admin.site.register(PersonalCategroy)
admin.site.register(PersonalStatus)
admin.site.register(Service)
admin.site.register(ServiceCategory)
admin.site.register(ServiceImage)