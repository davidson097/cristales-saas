#!/usr/bin/env python3
"""
Seed script for Cristales SaaS demo data.
This is a simplified version that works with the existing database.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def main():
    """Main seed function"""
    print("🌱 Starting Cristales SaaS demo data seeding...")

    # Import and run existing seed functions
    try:
        from .seed_demo_data import seed as seed_demo
        from .seed_permisos import seed as seed_permisos
        from .seed_servicentro import seed as seed_servicentro

        print("Running demo data seed...")
        seed_demo()

        print("Running permisos seed...")
        seed_permisos()

        print("Running servicentro seed...")
        seed_servicentro()

        print("\n🎉 Demo data seeding completed successfully!")
        print("   - Demo data initialized")
        print("   - Permissions configured")
        print("   - Service center data loaded")

    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        raise


if __name__ == "__main__":
    main()