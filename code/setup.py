"""
This file is part of the django_relational_db service module.

Copyright (C) 2025 Shoestring and University of Cambridge

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from django.core.management.utils import get_random_secret_key
from pathlib import Path

secret_key_file = Path("/app/data/secret_key")

if not secret_key_file.exists():
    with open(secret_key_file, "w") as f:
        f.write(get_random_secret_key())


intial_admin_pw_file = Path("/app/data/admin_pw")

if intial_admin_pw_file.exists():
    print("initial admin password already set")
else:
    admin_password = None
    while not admin_password:
        admin_password = input("Enter an initial password for the admin account:")
        if admin_password:
            with open(intial_admin_pw_file, "w") as f:
                f.write(admin_password)
            print("Initial admin password saved")
        else:
            print("No admin password provided")
