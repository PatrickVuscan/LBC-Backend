"""Validation logic for comment model."""
import abc


class CommentValidatorInterface(metaclass=abc.ABCMeta):
    """Interface for required validation for comments."""

    @abc.abstractmethod
    def validate_user(self, user_id: int):
        """Validate User with `user_id`."""
        raise NotImplementedError

    @abc.abstractmethod
    def validate_post(self, post_id: int):
        """Validate Post with `post_id`."""
        raise NotImplementedError

    @abc.abstractmethod
    def validate_comment(self, comment_id: int):
        """Validate Comment with `comment_id`"""
        raise NotImplementedError
