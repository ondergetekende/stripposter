from urllib.parse import urljoin

import requests

from .statefile import StateFile
from .reddit import post_comic


def discover(comic_model):

    session = requests.Session()
    doc = comic_model.retrieve_index(session)

    #
    if comic_model.css_selector:
        instances = doc.cssselect(comic_model.css_selector)
    else:
        instances = [doc]

    # Find the comics on the index page
    results = []
    for element in instances:
        result = comic_model(element)
        result.extract_comic()

        # make sure the paths are absolute
        if result.image_url:
            result.image_url = urljoin(comic_model.base_url, result.image_url)

        if result.page_url:
            result.page_url = urljoin(comic_model.base_url, result.page_url)

        results.append(result)

    return results


def get_new_comics(comic_model, posted_ids):

    comics = discover(comic_model)

    if not(posted_ids):
        # For the first run, only post the latest comic
        comics.sort(key=lambda c: c.date)
        post_comics = [comics[-1]]

        # Mark the other comics as previously posted
        posted_ids.update(c.id for c in comics[:-1])
    else:
        # Filter out the ones we've already seen
        post_comics = [c for c in comics if c.id not in posted_ids]

    return post_comics


def post_updates(*comic_sites):
    for comic_site in comic_sites:
        statefilename = 'state-%s.json' % comic_site.name.lower().replace(' ', '-')
        with StateFile(statefilename) as state:
            posted_ids = set(state.setdefault('posted_ids', []))
            comics = get_new_comics(comic_site, posted_ids)
            state['posted_ids'] = sorted(posted_ids)

            for comic in comics:
                print("posting %s" % (comic))
                post_comic(comic)
                posted_ids.add(comic.id)
                state['posted_ids'] = sorted(posted_ids)
