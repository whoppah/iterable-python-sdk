from .base import BaseResource


class CatalogResource(BaseResource):
    def bulk_create_items(self, catalog_name, documents, replace_uploaded_fields_only=False):
        """
        Asynchronously create up to 1000 catalog items with a single request.

        :param catalog_name: Name of the catalog [Alphanumeric, dashes, case insensitive, 255 characters max]
        :param documents: List of dictionaries, each representing a catalog item
        :param replace_uploaded_fields_only: If True, only replace fields provided in the request
        :return: API response
        """
        endpoint = f"/api/catalogs/{catalog_name}/items"
        data = {
            "documents": documents,
            "replaceUploadedFieldsOnly": replace_uploaded_fields_only
        }
        return self.client.post(endpoint, data=data)

    def delete_item(self, catalog_name, item_id):
        """
        Asynchronously delete a specific item from the catalog.

        :param catalog_name: Name of the catalog [Alphanumeric, dashes, case insensitive, 255 characters max]
        :param item_id: ID of the item to delete [Alphanumeric, dashes, case sensitive, 255 characters max]
        :return: API response
        """
        endpoint = f"/api/catalogs/{catalog_name}/items/{item_id}"
        return self.client.delete(endpoint)
