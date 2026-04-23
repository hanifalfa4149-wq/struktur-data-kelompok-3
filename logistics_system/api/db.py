"""Supabase client provider for FastAPI backend."""

import os

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

_SUPABASE_URL = os.environ.get("SUPABASE_URL")
_SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

if not _SUPABASE_URL or not _SUPABASE_SERVICE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")

_SUPABASE_CLIENT: Client = create_client(_SUPABASE_URL, _SUPABASE_SERVICE_KEY)


def get_client() -> Client:
    """Return the shared Supabase client instance."""
    return _SUPABASE_CLIENT
