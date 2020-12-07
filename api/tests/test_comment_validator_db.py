"""Tests for CommentValidatorDB."""
# pylint: disable-all
from unittest import TestCase
import pytest

from api.database.comment_validator_db import CommentValidatorDB
from api.tests.utils.utils import init_user, init_post, init_comment


@pytest.mark.usefixtures("init_user", "init_post", "init_comment")
class TestCommentValidatorDB(TestCase):
    """Test all functionality for comment validator object."""

    @pytest.fixture(autouse=True)
    def init_comment_db(self):
        self.validator = CommentValidatorDB()

    def test_validate_user(self):
        self.validator.validate_user(self.uid)

        with pytest.raises(ValueError):
            self.validator.validate_user(-1)

    def test_validate_post(self):
        self.validator.validate_post(self.pid)

        with pytest.raises(ValueError):
            self.validator.validate_post(-1)

    def test_validate_comment(self):
        self.validator.validate_comment(self.cid)

        with pytest.raises(ValueError):
            self.validator.validate_comment(-1)
