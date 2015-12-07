from peewee import *

db = SqliteDatabase('eqd_posts.db')


class PostModel(Model):
    title = CharField()
    link = CharField()
    timestamp = DateTimeField()

    class Meta:
        database = db


class TagModel(Model):
    tag_name = CharField()
    tag_link = CharField()

    class Meta:
        database = db


class TagRelation(Model):
    post_id = ForeignKeyField(PostModel)
    tag_id = ForeignKeyField(TagModel)

    class Meta:
        database = db
