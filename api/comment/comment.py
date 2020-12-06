"""Contains the definition of what a comment is."""


class Comment:
    """Comment datastructure."""

    def __init__(self, comment_id: int, post_id: int, user_id: int, content: str):

        self.comment_id = comment_id
        self.post_id = post_id
        self.user_id = user_id
        self.content = content
