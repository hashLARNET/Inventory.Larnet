from supabase import create_client, Client
from backend.config import settings

def get_supabase_client() -> Client:
    """Get Supabase client instance"""
    return create_client(settings.supabase_url, settings.supabase_anon_key)

def get_supabase_admin_client() -> Client:
    """Get Supabase admin client instance"""
    return create_client(settings.supabase_url, settings.supabase_service_role_key)

# Global client instances
supabase_client = get_supabase_client()
supabase_admin = get_supabase_admin_client()