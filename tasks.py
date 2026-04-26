from invoke import task
from subprocess import call
from sys import platform

@task #käsky pelin käynnistämiseen
def start(ctx): 
    ctx.run("python3 src/index.py", pty=True)

@task #käsky testien ajamiseen
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src", pty=True)

@task(coverage) #käsky testien ajamiseen ja raportin luomiseen
def coverage_report(ctx):
    ctx.run("coverage html", pty=True)
    if platform != "win32":
        call(("xdg-open", "htmlcov/index.html"))

@task #käsky testien ajamiseen
def test(ctx):
    ctx.run("pytest src", pty=True)

@task #käsky koodin muotoiluun
def format(ctx):
    ctx.run("autopep8 --in-place --recursive src", pty=True)

@task #käsky koodin tarkistamiseen
def lint(ctx):
    ctx.run("pylint src", pty=True)