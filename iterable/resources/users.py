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

    def delete(self, email=None, user_id=None):
        """
        Delete a user by email or userId.

        Uses DELETE /api/users/{email} for email-based deletion (works for
        email-based and hybrid projects, not userID-based projects).

        Uses DELETE /api/users/byUserId/{userId} for userId-based deletion
        (works for all project types).

        If both are provided, userId takes priority as it works across all
        project types.

        WARNING: This endpoint completely deletes the specified user profile,
        including subscription settings and event history. If the user is ever
        re-added, their profile will be empty and subscribed to everything by
        default. Deleting a user removes their historic campaign metrics, too.

        Rate limit: 100 requests/second, per project.

        :param email: user's email address (optional if user_id provided)
        :param user_id: user's ID (optional if email provided)
        :return: API response
        """
        if not email and not user_id:
            raise ValueError("Either email or user_id must be provided")

        if user_id:
            return self.client.delete(f"users/byUserId/{user_id}")

        return self.client.delete(f"users/{email}")

    def get(self, email):
        """
        Get user data by email.

        :param email: user's email address
        :return: API response
        """
        return self.client.get("users/get", params={"email": email})
