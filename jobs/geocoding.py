
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError

from .models import Job


def set_coordinates(job):
    location = (job.location or "").strip()

    if not location or location.lower() == "remote":
        job.latitude = None
        job.longitude = None
        return False

    existing = Job.objects.filter(
        location__iexact=location,
        latitude__isnull=False,
        longitude__isnull=False
    ).values_list("latitude", "longitude").first()

    if existing:
        job.latitude, job.longitude = existing
        return True

    query = urlencode({
        "q": location,
        "format": "json",
        "limit": 1
    })

    url = (
        "https://nominatim.openstreetmap.org/search?"
        + query
    )

    request = Request(
        url,
        headers={
            "User-Agent": (
                "CS2340-RecruitingBoard/1.0 "
                "(https://github.com/Aishi25/cs2340-project2)"
            )
        }
    )

    try:
        with urlopen(request, timeout=5) as response:
            results = json.load(response)

        if results:
            job.latitude = float(results[0]["lat"])
            job.longitude = float(results[0]["lon"])
            return True

    except (URLError, OSError, ValueError, KeyError, TypeError):
        pass

    job.latitude = None
    job.longitude = None
    return False
