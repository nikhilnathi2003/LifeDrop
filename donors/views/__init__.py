"""LifeDrop views package — one file per member (see GROUP ROLES slide)."""
from .v_sujith import (RequestListView, RequestDetailView,
                       post_request, edit_request, my_requests)
from .v_charan import upload_images
from .v_sneha import contact, about, team
from .v_nikhil import register, profile, upload_card
from .v_sai import send_message, offer_to_donate

__all__ = [
    "RequestListView", "RequestDetailView", "post_request", "edit_request",
    "my_requests", "upload_images", "contact", "about", "team",
    "register", "profile", "upload_card", "send_message", "offer_to_donate",
]
