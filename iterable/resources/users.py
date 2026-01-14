from .base import BaseResource


class UsersResource(BaseResource):
    def update(self, data):
        """
        Update or create a user.

        :param data: dict containing user data
        :return: API response
        """

        return self.client.post("users/update", data=data)

    def bulk_update(self, data):
        """
        Bulk update or create users.

        :param data: dict containing user data
        :return: API response
        """

        return self.client.post("users/bulkUpdate", data=data)

    def delete(self, user_id):
        """
        Delete a user by userId.

        Uses DELETE /api/users/byUserId/{userId} endpoint. Works for all
        project types (email-based, userID-based, and hybrid projects).

        If multiple users share the same userId, they'll all be deleted.

        WARNING: This endpoint completely deletes the specified user profile,
        including subscription settings and event history. If the user is ever
        re-added, their profile will be empty and subscribed to everything by
        default. Deleting a user removes their historic campaign metrics, too.

        Rate limit: 100 requests/second, per project.

        :param user_id: user's ID (required)
        :return: API response
        """
        return self.client.delete(f"users/byUserId/{user_id}")

    def get(self, email):
        """
        Get user data by email.

        :param email: user's email address
        :return: API response
        """
        return self.client.get("users/get", params={"email": email})
