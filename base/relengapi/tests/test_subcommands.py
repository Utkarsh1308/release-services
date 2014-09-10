# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import logging
import sys

from cStringIO import StringIO
from nose.tools import eq_
from relengapi.lib import subcommands

logger = logging.getLogger(__name__)


class MySubcommand(subcommands.Subcommand):

    def make_parser(self, subparsers):
        parser = subparsers.add_parser('my-subcommand', help='test subcommand')
        parser.add_argument("--result", help='Set result')
        return parser

    def run(self, parser, args):
        print "subcommand tests - print output"
        logger.info("subcommand tests - info logging output")
        logger.warning("subcommand tests - warning logging output")
        MySubcommand.run_result = args.result


def run_main(args):
    old_out = sys.stdout
    sys.stdout = fake_stdout = StringIO()
    try:
        subcommands.main(args)
    except SystemExit:
        pass
    finally:
        old_out.write(sys.stdout.getvalue())
        sys.stdout = old_out
    return fake_stdout.getvalue()


def test_subcommand_help():
    assert 'my-subcommand' in run_main(['--help'])


def test_subcommand_runs():
    output = run_main(['my-subcommand', '--result=foo'])
    assert "print" in output
    assert "info" in output
    assert "warning" in output
    eq_(MySubcommand.run_result, 'foo')


def test_subcommand_quiet():
    output = run_main(['--quiet', 'my-subcommand', '--result=foo'])
    assert "print" in output
    assert "info" not in output
    assert "warning" in output
    eq_(MySubcommand.run_result, 'foo')
