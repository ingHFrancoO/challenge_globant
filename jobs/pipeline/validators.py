
_REQUIRED_FILES = {
    "departments.csv",
    "hired_employees.csv",
    "jobs.csv",
}

def validate_required_files(
    files: list[str],
) -> dict[str, str]:
    """
    Validates that all required files are present in the input list.

    Args:
        files: Full GCS paths (e.g. incoming/departments.csv)
        required_files: Expected file names without prefix

    Returns:
        Dict[str, str]: mapping {filename: full_path}

    Raises:
        ValueError: if any required file is missing
    """

    file_map = {
        f.split("/")[-1]: f
        for f in files
    }

    missing = _REQUIRED_FILES - file_map.keys()
    if missing:
        raise ValueError(
            f"Missing required input files: {sorted(missing)}"
        )

    return