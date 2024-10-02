from .base import BaseResource


class EventsResource(BaseResource):
    def track(self, data):
        """
        Track an event.

        :param data: dict containing user data
        :return: API response
        """

        return self.client.post("events/track", data=data)
