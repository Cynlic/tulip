from tulip.symbol import Symbol, SymbolTable
from tulip.syntax import *
import tulip.parser as parser
from tulip.parser_gen import ParseError
from sys import stdin
from tulip.libedit import readline
from tulip.debug import debug
from rpython.rlib.objectmodel import we_are_translated
from tulip.lexer import ReaderLexer, Token, LexError
from tulip.reader import StringReader, FileReader

def entry_point(argv):
    if len(argv) >= 2:
        return run_file(argv[1])
    elif stdin.isatty:
        return run_repl()
    else:
        assert False, u'TODO: actually implement an arg parser'

def run_repl():
    print_logo()

    while True:
        try:
            line = readline(': ')
            print parser.expr.parse(Lexer(StringReader(u'<repl>', line))).dump()
        except LexError as e:
            print u'lex error: %d:%d' % (e.lexer.line, e.lexer.col)
            print u'head: <%s>' % e.lexer.head
        except ParseError as e:
            print e.dump()
        except EOFError:
            break

    return 0

def print_logo():
    print
    print u"    )`("
    print u"   (   ) tulip"
    print u"     |/"
    print

def run_file(fname):
    reader = FileReader(fname)
    try:
        print parser.module.parse(Lexer(reader)).dump()
    except LexError as e:
        print u'lex error: %d:%d' % (e.lexer.line, e.lexer.col)
        print u'head: <%s>' % e.lexer.head
    except ParseError as e:
        print e.dump()

    return 0

def target(*args):
    return (entry_point, None)

if __name__ == '__main__':
    from sys import argv
    entry_point(argv)
