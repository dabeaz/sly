Contributing to SLY
===================
SLY, like most projects related to parser generators, is a niche
project.  Although it appears to be a somewhat "new" project, it is
actually an outgrowth of the PLY project which has been around since
2001.  Contributions of most kinds that make it better are
welcome--this includes code, documentation, examples, and feature
requests.

There aren't too many formal guidelines.  If submitting a bug report,
any information that helps to reproduce the problem will be handy.  If
submitting a pull request, try to make sure that SLY's test suite
still passes. Even if that's not the case though, that's okay--a
failed test might be something very minor that can fixed up after a
merge.

Project Scope
-------------
It is not my goal to turn SLY into a gigantic parsing framework with
every possible feature.  What you see here is pretty much what it is--a
basic LALR(1) parser generator and tokenizer.  If you've built something
useful that uses SLY or builds upon it, it's probably better served by
its own repository. Feel free to submit a pull request to the SLY README
file that includes a link to your project.

The SLY "Community" (or lack thereof)
-------------------------------------
As noted, parser generator tools are a highly niche area.  It is
important to emphasize that SLY is a very much a side-project for
me. No funding is received for this work.  I also run a business and
have a family with kids.  These things have higher priority. As such,
there may be periods in which little activity is made on pull
requests, issues, and other development matters.  Sometimes you might
only see a flurry of activity around the times when I use SLY in
a compilers course that I teach.   Do not mistake "inaction" for
"disinterest."  I am definitely interested in improving SLY--it's
just not practical for me to give it my undivided attention. 

Important Note
--------------
As a general rule, pull requests related to third-party tooling (IDEs,
type-checkers, linters, code formatters, etc.) will not be accepted.
If you think something should be changed/improved in this regard,
please submit an issue instead.

