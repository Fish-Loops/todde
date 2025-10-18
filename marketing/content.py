from __future__ import annotations

from dataclasses import dataclass
from typing import List, Mapping


@dataclass(frozen=True)
class NavigationLink:
    label: str
    href: str
    description: str = ""


@dataclass(frozen=True)
class VehicleCategory:
    name: str
    icon: str
    description: str


@dataclass(frozen=True)
class VehicleListing:
    name: str
    price: str
    payment_plan: str
    image_url: str
    location: str
    badge: str


@dataclass(frozen=True)
class ValueProposition:
    title: str
    description: str
    icon: str


@dataclass(frozen=True)
class FinancingStep:
    title: str
    description: str


def get_navigation_links() -> List[NavigationLink]:
    return [
        NavigationLink("Home", "/"),
        NavigationLink("Buy a Car", "/#inventory", "Browse available inventory"),
        NavigationLink("Financing", "/financing/", "See financing options"),
        NavigationLink("About", "/#about", "Learn about Todde"),
        NavigationLink("Contact", "/#contact", "Get in touch with our team"),
    ]


def get_vehicle_categories() -> List[VehicleCategory]:
    return [
        VehicleCategory("Sedans", "heroicons:car", "Comfortable daily drivers"),
        VehicleCategory("SUVs", "heroicons:truck", "Spacious family rides"),
    VehicleCategory("Electric", "heroicons:bolt", "Energy-efficient innovation"),
    VehicleCategory("Luxury", "heroicons:sparkles", "Premium experience"),
    ]


def get_featured_vehicles() -> List[VehicleListing]:
    return [
        VehicleListing(
            name="2023 Toyota Corolla XLE",
            price="₦17,800,000",
            payment_plan="₦2,150,000 down • ₦420,000 / month",
            image_url="https://images.unsplash.com/photo-1549921296-3b4a6b789555?auto=format&fit=crop&w=800&q=80",
            location="Lagos, Nigeria",
            badge="Top Choice",
        ),
        VehicleListing(
            name="2022 Honda HR-V Sport",
            price="₦23,400,000",
            payment_plan="₦2,990,000 down • ₦560,000 / month",
            image_url="https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=800&q=80",
            location="Abuja, Nigeria",
            badge="New Arrival",
        ),
        VehicleListing(
            name="2021 Mercedes-Benz C300",
            price="₦38,750,000",
            payment_plan="₦4,850,000 down • ₦870,000 / month",
            image_url="https://images.unsplash.com/photo-1503736334956-4c8f8e92946d?auto=format&fit=crop&w=800&q=80",
            location="Port Harcourt, Nigeria",
            badge="Executive",
        ),
        VehicleListing(
            name="2023 Hyundai Kona EV",
            price="₦28,500,000",
            payment_plan="₦3,500,000 down • ₦645,000 / month",
            image_url="https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=800&q=80",
            location="Lagos, Nigeria",
            badge="Electric",
        ),
    ]


def get_value_propositions() -> List[ValueProposition]:
    return [
        ValueProposition(
            title="Certified Quality",
            description="Every vehicle passes a 200-point inspection with transparent history reports.",
            icon="heroicons:shield-check",
        ),
        ValueProposition(
            title="Smart Pricing",
            description="We leverage market data and Todde partner network to deliver unmatched deals.",
            icon="heroicons:banknotes",
        ),
        ValueProposition(
            title="Always-On Support",
            description="Dedicated advisors guide you through selection, financing, and ownership.",
            icon="heroicons:lifebuoy",
        ),
        ValueProposition(
            title="Flexible Financing",
            description="Pay only 30% upfront and spread the balance over up to 36 months.",
            icon="heroicons:sparkles",
        ),
    ]


def get_financing_steps() -> List[FinancingStep]:
    return [
        FinancingStep("Create your Todde account", "Start with your BVN and contact details."),
        FinancingStep("Choose your vehicle", "Browse inspected inventory or request a custom sourcing."),
        FinancingStep("Submit quick application", "Provide employment, income, and preferred repayment tenor."),
        FinancingStep("Get instant decision", "Receive a tailored repayment plan in under 24 hours."),
        FinancingStep("Pay 30% deposit", "Secure your car with Todde’s low upfront commitment."),
        FinancingStep("Drive home", "Pick-up from a Todde hub or request doorstep delivery."),
        FinancingStep("Make monthly payments", "Automated reminders and flexible payment channels."),
        FinancingStep("Own it outright", "Complete your instalments and receive your ownership certificate."),
    ]


def get_financing_highlights() -> List[Mapping[str, str]]:
    return [
        {"title": "Up to 36 months", "description": "Flexible tenors that match your income cycle."},
        {"title": "Low interest rates", "description": "Negotiated rates through Todde financial partners."},
        {"title": "Insurance & maintenance", "description": "Bundled coverage keeps you protected on the road."},
    ]


def get_brand_metrics() -> List[Mapping[str, str]]:
    return [
        {"value": "15K+", "label": "Customers empowered"},
        {"value": "300+", "label": "Cars financed this year"},
        {"value": "48hrs", "label": "Average approval time"},
    ]
