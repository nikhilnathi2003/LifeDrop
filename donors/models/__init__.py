"""
LifeDrop models package.

The ten models are split two per group member, one file each, so every member
owns their own file in the shared repository:

  m_sujith.py  -> BloodType, BloodRequest            (Sujith)
  m_charan.py  -> RequestImage, SearchQuery           (Charan Sai)
  m_sneha.py   -> ContactMessage, Review              (Sneha)
  m_nikhil.py  -> DonorProfile, DonorVerification     (Nikhil)
  m_sai.py     -> Message, UserVisit                  (Sai Srinivas)

Imported here in dependency order so Django registers them all.
"""
from .m_sujith import BloodType, BloodRequest
from .m_charan import RequestImage, SearchQuery
from .m_sneha import ContactMessage, Review
from .m_nikhil import DonorProfile, DonorVerification
from .m_sai import Message, UserVisit

__all__ = [
    "BloodType", "BloodRequest", "RequestImage", "SearchQuery",
    "ContactMessage", "Review", "DonorProfile", "DonorVerification",
    "Message", "UserVisit",
]
