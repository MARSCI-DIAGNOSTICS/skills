"""Utility modules for duende-docs scripts."""

from .constants import (
    RUN_ID_LENGTH,
    PERCENTILE_P50,
    PERCENTILE_P90,
    PERCENTILE_P99,
    MS_PER_SECOND,
    SECONDS_PER_MINUTE,
    SECONDS_PER_HOUR,
)

from .common_paths import (
    find_repo_root,
    get_skill_dir,
    get_scripts_dir,
    get_config_dir,
    setup_python_path,
)

from .script_utils import (
    configure_utf8_output,
    ensure_yaml_installed,
    resolve_base_dir,
    format_duration,
    normalize_url_for_display,
    EXIT_SUCCESS,
    EXIT_NO_RESULTS,
    EXIT_BAD_ARGS,
    EXIT_INDEX_ERROR,
    EXIT_MISSING_DEPS,
    HTTP_STATUS_RATE_LIMITED,
)

from .dev_mode import (
    DEV_ROOT_ENV_VAR,
    is_dev_mode,
    get_effective_skill_dir,
    get_mode_info,
    print_mode_banner,
    format_shell_commands,
    ModeInfo,
)

from .path_config import (
    get_base_dir,
    get_index_path,
    get_temp_dir,
)

from .logging_utils import (
    ScriptLogger,
    ErrorCategory,
    LazyRotatingFileHandler,
    JSONFormatter,
)

from .http_utils import (
    DEFAULT_TIMEOUT,
    USER_AGENT,
    fetch_with_retry,
    get_response_with_timeout,
    read_file_with_retry,
    write_file_with_retry,
    is_retryable_error,
)

from .cli_utils import (
    add_base_dir_argument,
    resolve_base_dir_from_args,
    add_common_index_args,
    DEFAULT_CANONICAL_RELATIVE,
)

from .config_helpers import (
    get_config_value_safe,
    get_http_timeout,
    get_http_max_timeout,
    get_http_user_agent,
    get_http_max_retries,
    get_scraping_rate_limit,
    get_scraping_max_workers,
    get_output_dir_mapping,
    get_index_chunk_size,
    get_index_lock_timeout,
    get_domain_weight,
    get_query_stop_words,
    get_domain_stop_words,
    get_natural_language_stop_words,
    reload_configs,
)

from .search_constants import (
    TITLE,
    DESCRIPTION,
    KEYWORD,
    TAG,
    IDENTIFIER,
    PENALTIES,
    COVERAGE,
    SUBSECTION,
    POSITIONAL,
    TitleScores,
    DescriptionScores,
    KeywordScores,
    TagScores,
    IdentifierScores,
    GenericPenalties,
    CoverageMultipliers,
    SubsectionScores,
    PositionalScores,
)

from .metadata_utils import (
    normalize_keywords,
    normalize_tags,
)

from .cache_manager import (
    CacheManager,
    compute_file_hash,
    compute_plugin_fingerprint,
    CACHE_FORMAT_VERSION,
)

__all__ = [
    # Constants
    'RUN_ID_LENGTH',
    'PERCENTILE_P50',
    'PERCENTILE_P90',
    'PERCENTILE_P99',
    'MS_PER_SECOND',
    'SECONDS_PER_MINUTE',
    'SECONDS_PER_HOUR',
    # Common paths
    'find_repo_root',
    'get_skill_dir',
    'get_scripts_dir',
    'get_config_dir',
    'setup_python_path',
    # Script utils
    'configure_utf8_output',
    'ensure_yaml_installed',
    'resolve_base_dir',
    'format_duration',
    'normalize_url_for_display',
    'EXIT_SUCCESS',
    'EXIT_NO_RESULTS',
    'EXIT_BAD_ARGS',
    'EXIT_INDEX_ERROR',
    'EXIT_MISSING_DEPS',
    'HTTP_STATUS_RATE_LIMITED',
    # Dev mode
    'DEV_ROOT_ENV_VAR',
    'is_dev_mode',
    'get_effective_skill_dir',
    'get_mode_info',
    'print_mode_banner',
    'format_shell_commands',
    'ModeInfo',
    # Path config
    'get_base_dir',
    'get_index_path',
    'get_temp_dir',
    # Logging utils
    'ScriptLogger',
    'ErrorCategory',
    'LazyRotatingFileHandler',
    'JSONFormatter',
    # HTTP utils
    'DEFAULT_TIMEOUT',
    'USER_AGENT',
    'fetch_with_retry',
    'get_response_with_timeout',
    'read_file_with_retry',
    'write_file_with_retry',
    'is_retryable_error',
    # CLI utils
    'add_base_dir_argument',
    'resolve_base_dir_from_args',
    'add_common_index_args',
    'DEFAULT_CANONICAL_RELATIVE',
    # Config helpers
    'get_config_value_safe',
    'get_http_timeout',
    'get_http_max_timeout',
    'get_http_user_agent',
    'get_http_max_retries',
    'get_scraping_rate_limit',
    'get_scraping_max_workers',
    'get_output_dir_mapping',
    'get_index_chunk_size',
    'get_index_lock_timeout',
    'get_domain_weight',
    'get_query_stop_words',
    'get_domain_stop_words',
    'get_natural_language_stop_words',
    'reload_configs',
    # Search constants - instances
    'TITLE',
    'DESCRIPTION',
    'KEYWORD',
    'TAG',
    'IDENTIFIER',
    'PENALTIES',
    'COVERAGE',
    'SUBSECTION',
    'POSITIONAL',
    # Search constants - classes
    'TitleScores',
    'DescriptionScores',
    'KeywordScores',
    'TagScores',
    'IdentifierScores',
    'GenericPenalties',
    'CoverageMultipliers',
    'SubsectionScores',
    'PositionalScores',
    # Metadata utils
    'normalize_keywords',
    'normalize_tags',
    # Cache manager
    'CacheManager',
    'compute_file_hash',
    'compute_plugin_fingerprint',
    'CACHE_FORMAT_VERSION',
]
