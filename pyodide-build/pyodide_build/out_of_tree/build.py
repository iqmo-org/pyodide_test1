import os
from pathlib import Path
from typing import Any

from .. import common, pypabuild


def run(srcdir: Path, outdir: Path, exports: Any, args: list[str]) -> Path:
    outdir = outdir.resolve()
    cflags = common.get_make_flag("SIDE_MODULE_CFLAGS")
    cflags += f" {os.environ.get('CFLAGS', '')}"
    cxxflags = common.get_make_flag("SIDE_MODULE_CXXFLAGS")
    cxxflags += f" {os.environ.get('CXXFLAGS', '')}"
    ldflags = common.get_make_flag("SIDE_MODULE_LDFLAGS")
    ldflags += f" {os.environ.get('LDFLAGS', '')}"
    env = os.environ.copy()
    common.set_build_environment(env)

    build_env_ctx = pypabuild.get_build_env(
        env=env,
        pkgname="",
        cflags=cflags,
        cxxflags=cxxflags,
        ldflags=ldflags,
        target_install_dir="",
        exports=exports,
    )

    with build_env_ctx as env:
        built_wheel = pypabuild.build(srcdir, outdir, env, " ".join(args))
    return Path(built_wheel)
