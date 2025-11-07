"""
Context processors for the marketing app.
"""
from marketing.models import CarModel


def navigation_context(request):
    """Provide navigation-related context to all templates."""
    
    # Get available categories with proper labels
    available_categories = []
    
    # Only include categories that have actual cars
    from django.db.models import Count
    from marketing.views import _inventory_queryset
    
    try:
        base_queryset = _inventory_queryset(listing_type=None)
        category_counts = {
            entry["model__body_type"]: entry["total"]
            for entry in base_queryset.values("model__body_type").annotate(total=Count("id"))
        }
        
        category_mapping = {
            "sedan": {"label": "Sedans", "description": "Comfortable city cars"},
            "suv": {"label": "SUVs", "description": "Spacious family vehicles"},  
            "coupe": {"label": "Coupes", "description": "Stylish performance cars"},
            "hatchback": {"label": "Hatchbacks", "description": "Efficient urban cars"},
            "truck": {"label": "Trucks", "description": "Heavy-duty work vehicles"},
            "van": {"label": "Vans", "description": "Spacious cargo vehicles"},
        }
        
        for body_value, body_label in CarModel.BodyType.choices:
            if category_counts.get(body_value, 0) > 0:
                category_info = category_mapping.get(body_value, {
                    "label": body_label, 
                    "description": f"{body_label} vehicles"
                })
                available_categories.append({
                    "value": body_value,
                    "label": category_info["label"],
                    "description": category_info["description"],
                    "count": category_counts.get(body_value, 0),
                })
    
    except Exception:
        # Fallback to static categories if dynamic loading fails
        available_categories = [
            {"value": "sedan", "label": "Sedans", "description": "Comfortable city cars", "count": 0},
            {"value": "suv", "label": "SUVs", "description": "Spacious family vehicles", "count": 0},
            {"value": "coupe", "label": "Coupes", "description": "Stylish performance cars", "count": 0},
        ]
    
    return {
        "nav_categories": available_categories[:4]  # Limit to 4 items for clean UI
    }