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

    def delete(self, email):
        """
        Delete a user by email.

        :param email: user's email address
        :return: API response
        """
        return self.client.post("users/delete", data={"email": email})

    def get(self, email):
        """
        Get user data by email.

        :param email: user's email address
        :return: API response
        """
        return self.client.get("users/get", params={"email": email})
