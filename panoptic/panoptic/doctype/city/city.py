# Copyright (c) 2022, Internet Freedom Foundation and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from panoptic.panoptic.search import update_index_for_doc, remove_document_from_index


class City(WebsiteGenerator):
    def make_route(self):
        return "cities/" + self.scrub(self.for_city)

    def get_context(self, context):
        context.metatags = {
            "name": "Panoptic: {0}".format(self.title),
            "description": self.description,
            "image": "/assets/panoptic/images/meta/cities.png",
            "og:type": "article",
        }

    def on_update(self):
        if self.published:
            update_index_for_doc(self.doctype, self.name)
        else:
            remove_document_from_index(self.doctype, self.name)
        return super().on_update()

    def on_trash(self):
        remove_document_from_index(self.doctype, self.name)
        return super().on_trash()

    def get_search_doc(self):
        return frappe._dict(
            name=f"{self.doctype}////{self.name}",
            title=self.name,
            type="City",
            content=self.content,
            path=self.route,
            keywords=", ".join([str(self.state), str(self.for_city)]),
        )
