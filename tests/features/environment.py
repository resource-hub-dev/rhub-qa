import time
import os
import fixtures

from behave.fixture import use_fixture_by_tag
from selenium import webdriver

t = time.localtime()

fixture_registry = {
    "fixture.cli": fixtures.rhub_cli
}


def before_tag(context, tag):
    if tag.startswith('fixture.'):
        use_fixture_by_tag(tag, context, fixture_registry)


def before_scenario(context, scenario):

    vname = context.scenario.name + str(time.strftime("%H:%M:%S", t))

    if 'web' in context.tags:

        os.system(
            './../tools/cm selenoid update --browsers-json ./../tools/browsers.json'
        )
        os.system(
            './../tools/cm selenoid start --browsers-json ./../tools/browsers.json')
        os.system('./../tools/cm selenoid-ui start')

        time.sleep(5)

        capabilities = {
            "browserName": "chrome",
            "browserVersion": "latest",
            "acceptInsecureCerts": True,
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": True,
                "videoName": vname + ".mp4",
                "startMaximized": True
            }
        }

        context.browser = webdriver.Remote(
            command_executor="http://localhost:4444/wd/hub",
            desired_capabilities=capabilities)

        context.browser.implicitly_wait(10)


def after_scenario(context, scenario):
    if 'web' in context.tags:
        context.browser.quit()


def after_all(context):

    time.sleep(5)
    os.system('./../tools/cm selenoid stop')
    os.system('./../tools/cm selenoid-ui stop')
    os.system('cp ~/.aerokube/selenoid/video/*.mp4 ~/Videos/')

    print(" ")
    print("--------------------------------------------")
    print(" ")
    print("Tests results: ")
    print("    ")
