from .relationship import RelationshipManager


class ZeroOrMore(RelationshipManager):
    pass


class ZeroOrOne(RelationshipManager):
    def single(self):
        nodes = super(ZeroOrOne, self).all()
        if not nodes:
            return
        if len(nodes) == 1:
            return nodes[0]
        if len(nodes) > 1:
            raise CardinalityViolation(
                    "Expected zero or one related nodes got " + len(nodes))

    def all(self):
        node = self.single()
        if node:
            return [node]
        else:
            return []

    def relate(self, obj):
        if self.origin._node.has_relationship(self.direction, self.relation_type):
            raise AttemptedCardinalityViolation("Node already has one relationship")
        else:
            return super(ZeroOrOne, self).relate(obj)


class OneOrMore(RelationshipManager):
    def single(self):
        nodes = super(OneOrMore, self).all()
        if nodes:
            return nodes[0]
        else:
            raise CardinalityViolation("Expected at least one relation with one or more")

    def all(self):
        return [self.single()]

    def unrelate(self, obj):
        if len(self.origin._node.get_related_nodes(self.direction, self.relation_type)) < 2:
            raise AttemptedCardinalityViolation("One or more expected")
        return super(OneOrMore, self).unrelate(obj)


class One(RelationshipManager):
    def single(self):
        nodes = super(One, self).all()
        if nodes:
            return nodes[0]
        else:
            raise CardinalityViolation("Expected at least one relation with one or more")

    def all(self):
        return [self.single()]

    def unrelate(self, obj):
        raise AttemptedCardinalityViolation("Cardinality one, cannot unrelate use rerelate")

    def relate(self, obj):
        if self.origin._node.has_relationship(self.direction, self.relation_type):
            raise AttemptedCardinalityViolation("Node already has one relationship")
        else:
            return super(One, self).relate(obj)


class AttemptedCardinalityViolation(Exception):
    pass


class CardinalityViolation(Exception):
    pass