from django.urls import path

from . import views

app_name = "marketing"

urlpatterns = [
    path("", views.homepage, name="home"),
    path("registered-cars/", views.registered_cars, name="registered_cars"),
    path("foreign-used/", views.foreign_used_cars, name="foreign_used_cars"),
    path("cars/", views.all_cars, name="all_cars"),
    path("cars/<int:variant_id>/", views.vehicle_detail, name="vehicle_detail"),
    path("financing/", views.financing, name="financing"),
    path("api/car-manufacturers/", views.car_manufacturers_api, name="api_car_manufacturers"),
    path("api/car-models/", views.car_models_api, name="api_car_models"),
    path("api/car-variants/", views.car_variants_api, name="api_car_variants"),
]
