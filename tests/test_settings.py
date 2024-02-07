"""Tests for the `Settings` class."""

from algobase.settings import Settings


class TestSettings:
    """Tests for the `Settings` class."""

    def test_settings(self) -> None:
        """Test that the settings are loaded correctly."""

        def callable(settings: Settings) -> bool:
            """Function to test that a settings object can be piped to a callable.

            Args:
                settings (Settings): The settings object.

            Returns:
                bool: True if the object passed is a settings object.
            """
            return isinstance(settings, Settings)

        settings = Settings()
        assert settings | callable
