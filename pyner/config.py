"""
Configuration management for Pyner.

Handles NCBI API credentials and search parameters.
"""

import os
from typing import Optional
from pathlib import Path


class Config:
    """
    Configuration for Pyner data mining.

    Manages NCBI API access and default search parameters.

    Example:
        >>> config = Config(email="your.email@institution.edu")
        >>> config.set_api_key("your_api_key_here")
        >>> miner = DataMiner(config)
    """

    def __init__(
        self,
        email: Optional[str] = None,
        api_key: Optional[str] = None,
        batch_size: int = 1000,
        rate_limit: float = 0.34  # ~3 requests per second with API key
    ):
        """
        Initialize configuration.

        Args:
            email: Email for NCBI E-utilities (required by NCBI)
            api_key: NCBI API key (increases rate limit from 3 to 10 req/sec)
            batch_size: Number of records to fetch per API call
            rate_limit: Seconds to wait between API calls
        """
        self.email = email or os.getenv("NCBI_EMAIL")
        self.api_key = api_key or os.getenv("NCBI_API_KEY")
        self.batch_size = batch_size
        self.rate_limit = rate_limit

        # Adjust rate limit based on API key availability
        if self.api_key:
            self.rate_limit = 0.11  # ~9 requests per second with API key
        else:
            self.rate_limit = 0.34  # ~3 requests per second without API key

        if not self.email:
            raise ValueError(
                "Email is required for NCBI API access. "
                "Set via email parameter or NCBI_EMAIL environment variable."
            )

    def set_api_key(self, api_key: str):
        """
        Set NCBI API key and adjust rate limit.

        Args:
            api_key: NCBI API key
        """
        self.api_key = api_key
        self.rate_limit = 0.11  # Increase rate with API key

    @classmethod
    def from_env(cls) -> 'Config':
        """
        Create configuration from environment variables.

        Expected environment variables:
        - NCBI_EMAIL: Email address (required)
        - NCBI_API_KEY: API key (optional but recommended)

        Returns:
            Config instance
        """
        email = os.getenv("NCBI_EMAIL")
        api_key = os.getenv("NCBI_API_KEY")

        if not email:
            raise ValueError(
                "NCBI_EMAIL environment variable is required. "
                "Example: export NCBI_EMAIL='your.email@institution.edu'"
            )

        return cls(email=email, api_key=api_key)

    @classmethod
    def from_file(cls, config_path: Path) -> 'Config':
        """
        Load configuration from file.

        Config file format (Python):
        ```
        NCBI_EMAIL = "your.email@institution.edu"
        NCBI_API_KEY = "your_api_key_here"
        ```

        Args:
            config_path: Path to configuration file

        Returns:
            Config instance
        """
        config_vars = {}
        with open(config_path, 'r') as f:
            exec(f.read(), config_vars)

        return cls(
            email=config_vars.get("NCBI_EMAIL"),
            api_key=config_vars.get("NCBI_API_KEY")
        )

    def validate(self):
        """
        Validate configuration.

        Raises:
            ValueError: If configuration is invalid
        """
        if not self.email:
            raise ValueError("Email is required for NCBI API access")

        if '@' not in self.email:
            raise ValueError("Email must be a valid email address")

        if self.batch_size < 1 or self.batch_size > 10000:
            raise ValueError("batch_size must be between 1 and 10000")

        if self.rate_limit < 0:
            raise ValueError("rate_limit must be positive")

    def __repr__(self):
        """String representation (hides API key)."""
        api_key_display = "***" if self.api_key else "None"
        return (
            f"Config(email='{self.email}', "
            f"api_key={api_key_display}, "
            f"batch_size={self.batch_size}, "
            f"rate_limit={self.rate_limit})"
        )
