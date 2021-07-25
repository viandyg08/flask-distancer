import logging
from flask import Blueprint, request
from werkzeug.exceptions import NotFound
from distancer.utils import YandexResponse


distancer_logger = logging.getLogger("distancer")

distancer = Blueprint("distancer", __name__)


@distancer.route("/")
def index():
    # Get the address input parameter
    address = request.args.get("address")

    # Raise error and add to log if no input address is found
    if not address:
        distancer_logger.error("No input address was found")
        raise NotFound("No input address was found")

    # Get coordinates for MKAD and the input address
    mkad = YandexResponse("МКАД")
    target = YandexResponse(address)

    # Raise error and add to log if input address is located in MKAD
    if target.check_in_mkad():
        distancer_logger.error(f"The input {address} is located within MKAD.")
        return "The address is located in MKAD"

    # Calculate the distance from MKAD
    dist = mkad.get_distance(target.coordinate)

    # Return the distance with 2 decimal places
    return f"The distance from MKAD is <b><u>{dist:.2f} km</u></b>"
