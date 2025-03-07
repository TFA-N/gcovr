# -*- coding:utf-8 -*-

#  ************************** Copyrights and license ***************************
#
# This file is part of gcovr 5.2, a parsing and reporting tool for gcov.
# https://gcovr.com/en/stable
#
# _____________________________________________________________________________
#
# Copyright (c) 2013-2022 the gcovr authors
# Copyright (c) 2013 Sandia Corporation.
# Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
# the U.S. Government retains certain rights in this software.
#
# This software is distributed under the 3-clause BSD License.
# For more information, see the README.rst file.
#
# ****************************************************************************

from ..__main__ import main
from ..version import __version__

import logging
import pytest
import os
import re
import sys


# The CaptureObject class holds the capture method result
class CaptureObject:
    def __init__(self, out, err, exception):
        self.out = out
        self.err = err
        self.exception = exception


def capture(capsys, args, other_ex=()):
    """The capture method calls the main method and captures its output/error
    streams and exit code."""
    e = None
    try:
        main(args)
        # Explicit SystemExit exception in case main() returns normally
        sys.exit(0)
    except SystemExit as exception:
        e = exception
    except other_ex as exception:
        e = exception
    out, err = capsys.readouterr()
    return CaptureObject(out, err, e)


# The LogCaptureObject class holds the capture method result
class LogCaptureObject:
    def __init__(self, record_tuples, exception):
        self.record_tuples = record_tuples
        self.exception = exception


def log_capture(caplog, args, other_ex=()):
    """The capture method calls the main method and captures its output/error
    streams and exit code."""
    e = None
    try:
        main(args)
        # Explicit SystemExit exception in case main() returns normally
        sys.exit(0)
    except SystemExit as exception:
        e = exception
    except other_ex as exception:
        e = exception
    return LogCaptureObject(caplog.record_tuples, e)


def test_version(capsys):
    c = capture(capsys, ["--version"])
    assert c.err == ""
    assert c.out.startswith(f"gcovr {__version__}")
    assert c.exception.code == 0


def test_help(capsys):
    c = capture(capsys, ["-h"])
    assert c.err == ""
    assert c.out.startswith("usage: gcovr [options]")
    assert c.exception.code == 0


def test_empty_root(capsys):
    c = capture(capsys, ["-r", ""])
    assert c.out == ""
    assert "argument -r/--root: Should not be set to an empty string." in c.err
    assert c.exception.code != 0


def test_empty_exclude(capsys):
    c = capture(capsys, ["--exclude", ""])
    assert c.out == ""
    assert "filter cannot be empty" in c.err
    assert c.exception.code != 0


def test_empty_exclude_directories(capsys):
    c = capture(capsys, ["--exclude-directories", ""])
    assert c.out == ""
    assert "filter cannot be empty" in c.err
    assert c.exception.code != 0


def test_empty_objdir(capsys):
    c = capture(capsys, ["--object-directory", ""])
    assert c.out == ""
    assert "argument --object-directory: Should not be set to an empty string." in c.err
    assert c.exception.code != 0


def test_invalid_objdir(caplog):
    c = log_capture(caplog, ["--object-directory", "not-existing-dir"])
    message = c.record_tuples[0]
    assert message[1] == logging.ERROR
    assert message[2].startswith("Bad --object-directory option.")
    assert c.exception.code == 1


def helper_test_non_existing_directory_output(capsys, option):
    c = capture(capsys, [option, "not-existing-dir/file.txt"])
    assert c.out == ""
    assert "Could not create output file 'not-existing-dir/file.txt': " in c.err
    assert c.exception.code != 0


def test_non_existing_directory_output(capsys):
    helper_test_non_existing_directory_output(capsys, "--output")


def test_non_existing_directory_txt(capsys):
    helper_test_non_existing_directory_output(capsys, "--txt")


def test_non_existing_directory_xml(capsys):
    helper_test_non_existing_directory_output(capsys, "--xml")


def test_non_existing_directory_html(capsys):
    helper_test_non_existing_directory_output(capsys, "--html")


def test_non_existing_directory_html_details(capsys):
    helper_test_non_existing_directory_output(capsys, "--html-details")


def test_non_existing_directory_sonarqube(capsys):
    helper_test_non_existing_directory_output(capsys, "--sonarqube")


def test_non_existing_directory_json(capsys):
    helper_test_non_existing_directory_output(capsys, "--json")


def test_non_existing_directory_csv(capsys):
    helper_test_non_existing_directory_output(capsys, "--csv")


def helper_test_non_existing_directory_2_output(capsys, option):
    c = capture(capsys, [option, "not-existing-dir/subdir/"])
    assert c.out == ""
    assert "Could not create output directory 'not-existing-dir/subdir/': " in c.err
    assert c.exception.code != 0


def test_non_existing_directory_2_output(capsys):
    helper_test_non_existing_directory_2_output(capsys, "--output")


def test_non_existing_directory_2_txt(capsys):
    helper_test_non_existing_directory_2_output(capsys, "--txt")


def test_non_existing_directory_2_xml(capsys):
    helper_test_non_existing_directory_2_output(capsys, "--xml")


def test_non_existing_directory_2_html(capsys):
    helper_test_non_existing_directory_2_output(capsys, "--html")


def test_non_existing_directory_2_html_details(capsys):
    helper_test_non_existing_directory_2_output(capsys, "--html-details")


def test_non_existing_directory_2_sonarqube(capsys):
    helper_test_non_existing_directory_2_output(capsys, "--sonarqube")


def test_non_existing_directory_2_json(capsys):
    helper_test_non_existing_directory_2_output(capsys, "--json")


def test_non_existing_directory_2_csv(capsys):
    helper_test_non_existing_directory_2_output(capsys, "--csv")


def helper_test_non_writable_directory_output(capsys, option):  # pragma: no cover
    c = capture(capsys, [option, "/file.txt"])
    assert c.out == ""
    assert "Could not create output file '/file.txt': " in c.err
    assert c.exception.code != 0


@pytest.mark.skipif(
    not (os.getenv("GCOVR_ISOLATED_TEST") == "zkQEVaBpXF1i"), reason="Only for docker"
)
def test_non_writable_directory_output(capsys):  # pragma: no cover
    helper_test_non_writable_directory_output(capsys, "--output")


@pytest.mark.skipif(
    not (os.getenv("GCOVR_ISOLATED_TEST") == "zkQEVaBpXF1i"), reason="Only for docker"
)
def test_non_writable_directory_txt(capsys):  # pragma: no cover
    helper_test_non_writable_directory_output(capsys, "--txt")


@pytest.mark.skipif(
    not (os.getenv("GCOVR_ISOLATED_TEST") == "zkQEVaBpXF1i"), reason="Only for docker"
)
def test_non_writable_directory_xml(capsys):  # pragma: no cover
    helper_test_non_writable_directory_output(capsys, "--xml")


@pytest.mark.skipif(
    not (os.getenv("GCOVR_ISOLATED_TEST") == "zkQEVaBpXF1i"), reason="Only for docker"
)
def test_non_writable_directory_html(capsys):  # pragma: no cover
    helper_test_non_writable_directory_output(capsys, "--html")


@pytest.mark.skipif(
    not (os.getenv("GCOVR_ISOLATED_TEST") == "zkQEVaBpXF1i"), reason="Only for docker"
)
def test_non_writable_directory_html_details(capsys):  # pragma: no cover
    helper_test_non_writable_directory_output(capsys, "--html-details")


@pytest.mark.skipif(
    not (os.getenv("GCOVR_ISOLATED_TEST") == "zkQEVaBpXF1i"), reason="Only for docker"
)
def test_non_writable_directory_sonarqube(capsys):  # pragma: no cover
    helper_test_non_writable_directory_output(capsys, "--sonarqube")


@pytest.mark.skipif(
    not (os.getenv("GCOVR_ISOLATED_TEST") == "zkQEVaBpXF1i"), reason="Only for docker"
)
def test_non_writable_directory_json(capsys):  # pragma: no cover
    helper_test_non_writable_directory_output(capsys, "--json")


@pytest.mark.skipif(
    not (os.getenv("GCOVR_ISOLATED_TEST") == "zkQEVaBpXF1i"), reason="Only for docker"
)
def test_non_writable_directory_csv(capsys):  # pragma: no cover
    helper_test_non_writable_directory_output(capsys, "--csv")


def test_no_output_html_details(caplog):
    c = log_capture(caplog, ["--html-details"])
    message = c.record_tuples[0]
    assert message[1] == logging.ERROR
    assert (
        message[2]
        == "a named output must be given, if the option --html-details\nis used."
    )
    assert c.exception.code != 0


def test_branch_threshold_nan(capsys):
    c = capture(capsys, ["--fail-under-branch", "nan"])
    assert c.out == ""
    assert "not in range [0.0, 100.0]" in c.err
    assert c.exception.code != 0


def test_line_threshold_negative(capsys):
    c = capture(capsys, ["--fail-under-line", "-0.1"])
    assert c.out == ""
    assert "not in range [0.0, 100.0]" in c.err
    assert c.exception.code != 0


def test_line_threshold_100_1(capsys):
    c = capture(capsys, ["--fail-under-line", "100.1"])
    assert c.out == ""
    assert "not in range [0.0, 100.0]" in c.err
    assert c.exception.code != 0


def test_filter_backslashes_are_detected(caplog):
    # gcov-exclude all to prevent any coverage data from being found
    c = log_capture(
        caplog,
        args=["--filter", r"C:\\foo\moo", "--gcov-exclude", ""],
        other_ex=re.error,
    )
    message0 = c.record_tuples[0]
    assert message0[1] == logging.WARNING
    assert message0[2].startswith("filters must use forward slashes as path separators")
    message = c.record_tuples[1]
    assert message[1] == logging.WARNING
    assert message[2].startswith("your filter : C:\\\\foo\\moo")
    message = c.record_tuples[2]
    assert message[1] == logging.WARNING
    assert message[2].startswith("did you mean: C:/foo/moo")
    assert isinstance(c.exception, re.error) or c.exception.code == 0


def test_html_css_not_exists(capsys):
    c = capture(capsys, ["--html-css", "/File/does/not/\texist"])
    assert c.out == ""
    assert (
        re.search(
            r"Should be a file that already exists: '[/\\]+File[/\\]+does[/\\]+not[/\\]+\\texist'",
            c.err,
        )
        is not None
    )
    assert c.exception.code != 0


def test_html_title_empty_string(caplog):
    c = log_capture(caplog, ["--html-title", ""])
    message = c.record_tuples[0]
    assert message[1] == logging.ERROR
    assert message[2] == "an empty --html_title= is not allowed."
    assert c.exception.code != 0


def test_html_medium_threshold_nan(capsys):
    c = capture(capsys, ["--html-medium-threshold", "nan"])
    assert c.out == ""
    assert "--html-medium-threshold: nan not in range [0.0, 100.0]" in c.err
    assert c.exception.code != 0


def test_html_medium_threshold_negative(capsys):
    c = capture(capsys, ["--html-medium-threshold", "-0.1"])
    assert c.out == ""
    assert "not in range [0.0, 100.0]" in c.err
    assert c.exception.code != 0


def test_html_medium_threshold_zero(caplog):
    c = log_capture(caplog, ["--html-medium-threshold", "0.0"])
    message = c.record_tuples[0]
    assert message[1] == logging.ERROR
    assert message[2] == "value of --html-medium-threshold= should not be zero."
    assert c.exception.code != 0


def test_html_high_threshold_nan(capsys):
    c = capture(capsys, ["--html-high-threshold", "nan"])
    assert c.out == ""
    assert "not in range [0.0, 100.0]" in c.err
    assert c.exception.code != 0


def test_html_high_threshold_negative(capsys):
    c = capture(capsys, ["--html-high-threshold", "-0.1"])
    assert c.out == ""
    assert "not in range [0.0, 100.0]" in c.err
    assert c.exception.code != 0


def test_html_medium_threshold_gt_html_high_threshold(caplog):
    c = log_capture(
        caplog, ["--html-medium-threshold", "60", "--html-high-threshold", "50"]
    )
    message = c.record_tuples[0]
    assert message[1] == logging.ERROR
    assert (
        message[2]
        == "value of --html-medium-threshold=60.0 should be\nlower than or equal to the value of --html-high-threshold=50.0."
    )
    assert c.exception.code != 0


def test_html_tab_size_zero(caplog):
    c = log_capture(caplog, ["--html-tab-size", "0"])
    message = c.record_tuples[0]
    assert message[1] == logging.ERROR
    assert message[2] == "value of --html-tab-size= should be greater 0."
    assert c.exception.code != 0


def test_multiple_output_formats_to_stdout(caplog):
    c = log_capture(
        caplog, ["--xml", "--html", "--sonarqube", "--coveralls", "--root", "gcovr"]
    )
    message = c.record_tuples[0]
    assert message[1] == logging.WARNING
    assert (
        message[2]
        == "HTML output skipped - consider providing an output file with `--html=OUTPUT`."
    )
    message = c.record_tuples[1]
    assert message[1] == logging.WARNING
    assert (
        message[2]
        == "Sonarqube output skipped - consider providing an output file with `--sonarqube=OUTPUT`."
    )
    message = c.record_tuples[2]
    assert message[1] == logging.WARNING
    assert (
        message[2]
        == "Coveralls output skipped - consider providing an output file with `--coveralls=OUTPUT`."
    )
    assert c.exception.code == 0


def test_multiple_output_formats_to_stdout_1(caplog):
    c = log_capture(
        caplog,
        ["--xml", "--html", "--sonarqube", "--coveralls", "-o", "-", "--root", "gcovr"],
    )
    message = c.record_tuples[0]
    assert message[1] == logging.WARNING
    assert (
        message[2]
        == "HTML output skipped - consider providing an output file with `--html=OUTPUT`."
    )
    message = c.record_tuples[1]
    assert message[1] == logging.WARNING
    assert (
        message[2]
        == "Sonarqube output skipped - consider providing an output file with `--sonarqube=OUTPUT`."
    )
    message = c.record_tuples[2]
    assert message[1] == logging.WARNING
    assert (
        message[2]
        == "Coveralls output skipped - consider providing an output file with `--coveralls=OUTPUT`."
    )
    assert c.exception.code == 0


def test_no_self_contained_without_file(caplog):
    c = log_capture(caplog, ["--no-html-self-contained", "--html"])
    message = c.record_tuples[0]
    assert message[1] == logging.ERROR
    assert (
        message[2]
        == "can only disable --html-self-contained when a named output is given."
    )
    assert c.exception.code != 0


def test_html_injection_via_json(capsys, tmp_path):
    import json
    import markupsafe

    script = '<script>alert("pwned")</script>'
    jsondata = {
        "gcovr/format_version": "0.3",
        "files": [
            {"file": script, "functions": [], "lines": []},
            {"file": "other", "functions": [], "lines": []},
        ],
    }

    tempfile = tmp_path / "injection.json"

    with tempfile.open("w+") as jsonfile:
        json.dump(jsondata, jsonfile)

    c = capture(capsys, ["-a", str(tempfile), "--html"])

    assert script not in c.out
    assert str(markupsafe.escape(script)) in c.out, "--- got:\n{}\n---".format(c.out)
    assert c.exception.code == 0


def test_exclude_lines_by_pattern(caplog):
    c = log_capture(caplog, ["--exclude-lines-by-pattern", "example.**"])
    message = c.record_tuples[0]
    assert message[1] == logging.ERROR
    assert message[2].startswith(
        "--exclude-lines-by-pattern: Invalid regular expression"
    )
    assert c.exception.code != 0


def test_exclude_branches_by_pattern(caplog):
    c = log_capture(caplog, ["--exclude-branches-by-pattern", "example.**"])
    message = c.record_tuples[0]
    assert message[1] == logging.ERROR
    assert message[2].startswith(
        "--exclude-branches-by-pattern: Invalid regular expression"
    )
    assert c.exception.code != 0


def test_invalid_timestamp(capsys):
    c = capture(capsys, ["--timestamp=foo"])
    assert c.out == ""
    assert "argument --timestamp: unknown timestamp format: 'foo'" in c.err
    assert c.exception.code != 0
