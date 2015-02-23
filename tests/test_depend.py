# Run these tests with 'nosetests':
#   install the 'python-nose' package (Fedora/CentOS or Ubuntu)
#   run 'nosetests' in the root of the repository

import glob
import os
import sys
import unittest

import planex.spec
import planex.depend


class BasicTests(unittest.TestCase):
    def setUp(self):
        self.spec = planex.spec.Spec("tests/data/ocaml-cohttp.spec",
                                     dist=".el6", topdir=".")

    def test_build_srpm_from_spec(self):
        planex.depend.build_srpm_from_spec(self.spec)

        self.assertEqual(
            sys.stdout.getvalue(),
            "./SRPMS/ocaml-cohttp-0.9.8-1.el6.src.rpm: "
            "./SPECS/ocaml-cohttp.spec "
            "./SOURCES/ocaml-cohttp-0.9.8.tar.gz "
            "./SOURCES/ocaml-cohttp-extra-0.9.8.tar.gz "
            "./SOURCES/ocaml-cohttp-init\n")

    def test_download_rpm_sources(self):
        planex.depend.download_rpm_sources(self.spec, None)

        self.assertEqual(
            sys.stdout.getvalue(),
            "./SOURCES/ocaml-cohttp-0.9.8.tar.gz: ./SPECS/ocaml-cohttp.spec\n"
            "./SOURCES/ocaml-cohttp-extra-0.9.8.tar.gz: "
            "./SPECS/ocaml-cohttp.spec "
            "$(shell find /code/ocaml-cohttp-extra)\n"
            "	@echo [GIT] $@\n"
            "	@git --git-dir=/code/ocaml-cohttp-extra/.git archive "
            "--prefix ocaml-cohttp-extra-0.9.8/ -o $@ HEAD\n")

    def test_build_rpm_from_srpm(self):
        planex.depend.build_rpm_from_srpm(self.spec)

        self.assertEqual(
            sys.stdout.getvalue(),
            "./RPMS/x86_64/ocaml-cohttp-0.9.8-1.el6.x86_64.rpm: "
            "./SRPMS/ocaml-cohttp-0.9.8-1.el6.src.rpm\n")

    def test_buildrequires_for_rpm(self):
        # N.B. buildrequires_for_rpm only generates rules for other packages
        # defined by local spec files.   Even though ocaml-cohttp depends on
        # other packages, the test data directory contains only ocaml-uri and
        # ocaml-cstruct.
        spec_paths = glob.glob(os.path.join("tests/data", "ocaml-*.spec"))
        specs = [planex.spec.Spec(spec_path, dist='.el6')
                 for spec_path in spec_paths]

        planex.depend.buildrequires_for_rpm(
            self.spec, planex.depend.package_to_rpm_map(specs))

        self.assertEqual(
            sys.stdout.getvalue(),
            "./RPMS/x86_64/ocaml-cohttp-0.9.8-1.el6.x86_64.rpm: "
            "./RPMS/x86_64/ocaml-uri-1.6.0-1.el6.x86_64.rpm\n"
            "./RPMS/x86_64/ocaml-cohttp-0.9.8-1.el6.x86_64.rpm: "
            "./RPMS/x86_64/ocaml-cstruct-1.4.0-1.el6.x86_64.rpm\n")
