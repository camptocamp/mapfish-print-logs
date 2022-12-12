import os
import subprocess

import pytest
import skimage.io  # pylint: disable=import-error
from c2cwsgiutils.acceptance.image import check_image

REGENERATE = False


def test_should_not_commit():
    assert REGENERATE is False


@pytest.mark.parametrize(
    "url,expected_file_name,height,width",
    [
        pytest.param("http://api:8080/logs", "not-login", 300, 800, id="not-login"),
        pytest.param("http://api_test_user:8080/logs", "index", 600, 800, id="index"),
        pytest.param("http://api_test_user:8080/logs/source/simple", "source", 195, 1200, id="source"),
        pytest.param(
            "http://api_test_user:8080/logs/ref?source=simple&ref=latest",
            "ref",
            700,
            1400,
            id="ref",
        ),
    ],
)
def test_ui(url, expected_file_name, height, width):
    subprocess.run(
        [
            "node",
            "screenshot.js",
            f"--url={url}",
            f"--width={width}",
            f"--height={height}",
            f"--output=/tmp/{expected_file_name}.png",
        ],
        check=True,
    )
    check_image(
        "/results",
        skimage.io.imread(f"/tmp/{expected_file_name}.png")[:, :, :3],
        os.path.join(os.path.dirname(__file__), f"{expected_file_name}.expected.png"),
        generate_expected_image=REGENERATE,
    )
