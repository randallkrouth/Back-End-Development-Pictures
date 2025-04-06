from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data), 200
    else:
        return jsonify({"message": "No pictures found"}), 404 

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if data:
        try:
            return jsonify(data[id - 1]), 200
        except IndexError:
            return jsonify({"message": "Picture ID not found"}), 404
        except Exception as e:
            print(f"Error retrieving picture: {e}")
            return jsonify({"message": "Internal server error"}), 500
    else:
        return jsonify({"message": "No picture found"}), 404 

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Creates a new picture."""
    try:
        picture = request.get_json()  # Get JSON data from request body

        # Check for duplicate IDs
        for existing_picture in data:
            if existing_picture.get("id") == picture.get("id"):
                return jsonify({"Message": f"picture with id {picture['id']} already present"}), 302

        data.append(picture)  # Add new picture to data list

        # Optionally, save the updated data to pictures.json here
        # (not shown in this example)

        # Include the id in the response.
        return jsonify({"message": "Picture created successfully", "id": picture["id"]}), 201  # 201 Created

    except (KeyError, TypeError, json.JSONDecodeError):  # Catch specific exceptions
        return jsonify({"message": "Invalid picture data"}), 400  # 400 Bad Request
    except Exception as e:
        print(f"Error creating picture: {e}")
        return jsonify({"message": "Internal server error"}), 500  # 500 Internal Server Error

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Updates a picture with the given ID."""
    try:
        updated_picture = request.get_json()  # Get updated data from request body

        for i, picture in enumerate(data):
            if picture.get("id") == id:
                # Update the picture with the new data
                data[i] = updated_picture

                # Optionally, save the updated data to pictures.json
                # (not shown in this example)

                return jsonify({"message": "Picture updated successfully"}), 200  # 200 OK

        # If the picture with the given ID is not found
        return jsonify({"message": "picture not found"}), 404

    except (KeyError, TypeError, json.JSONDecodeError):  # Handle invalid request data
        return jsonify({"message": "Invalid picture data"}), 400  # 400 Bad Request
    except Exception as e:
        print(f"Error updating picture: {e}")
        return jsonify({"message": "Internal server error"}), 500  # 500 Internal Server Error

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Deletes a picture with the given ID."""
    for i, picture in enumerate(data):
        if picture.get("id") == id:
            del data[i]  # Delete the picture from the list

            # Optionally, save the updated data to pictures.json
            # (not shown in this example)

            return jsonify({"message": "Picture deleted successfully"}), 204  # 200 OK

    # If the picture with the given ID is not found
    return jsonify({"message": "picture not found"}), 404
