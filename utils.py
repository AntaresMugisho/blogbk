import os
import uuid

def random_filename(instance, filename):
    extension = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4().hex}{extension}"
    return os.path.join(f"{instance.__class__.__name__.lower()}s", filename)
