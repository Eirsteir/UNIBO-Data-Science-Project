class IdentifiableEntity:
    def __init__(self, id):
        """

        :param id: str
        """
        self.id = id

    def get_id(self):
        return self.id


class Image(IdentifiableEntity):
    pass


class Annotation(IdentifiableEntity):
    def __init__(self, id, motivation, body, target):
        """

        :param id: str
        :param motivation: str
        :param body: Image
        :param target: IdentifiableEntity
        """
        super().__init__(id)
        self.motivation = motivation
        self.body = body
        self.target = target

    def get_body(self):
        return self.body

    def get_motivation(self):
        return self.motivation

    def get_target(self):
        return self.target


class EntityWithMetadata(IdentifiableEntity):
    def __init__(self, id, label, title, creators):
        """

        :param id: str
        :param label: str
        :param title: str or None
        :param creators: list[str]
        """
        super().__init__(id)
        self.label = label
        self.title = title
        self.creators = creators

    def get_label(self):
        return self.label

    def get_title(self):
        return self.title

    def get_creators(self):
        return self.creators


class Collection(IdentifiableEntity):
    def __init__(self, id, items):
        """

        :param id: str
        :param items: List[Manifest]
        """
        super().__init__(id)
        self.items = items


class Manifest(IdentifiableEntity):
    def __init__(self, id, items):
        """

        :param id: str
        :param items: List[Canvas]
        """
        super().__init__(id)
        self.items = items

    def get_items(self):
        return self.items


class Canvas(IdentifiableEntity):
    pass
