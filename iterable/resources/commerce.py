from .base import BaseResource


class CommerceResource(BaseResource):
    def update_cart(self, data):
        """
        Update the cart

        :param data: dict containing user data
        :return: API response
        """

        return self.client.post("commerce/updateCart", data=data)

    def track_purchase(self, data):
        """
        Track a purchase

        :param data: dict containing user data
        :return: API response
        """

        return self.client.post("commerce/trackPurchase", data=data)
