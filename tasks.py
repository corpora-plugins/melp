import requests
import json
import traceback
from corpus import *
from bs4 import BeautifulSoup
from django.utils.text import slugify
from timeit import default_timer as timer
from .content import REGISTRY as MELP_CONTENT_TYPE_SCHEMA
from manager.utilities import _contains

REGISTRY = {
    "Import MELP Data from TEI Repo": {
        "version": "0.1",
        "jobsite_type": "HUEY",
        "track_provenance": True,
        "create_report": True,
        "content_type": "Corpus",
        "configuration": {
            "parameters": {
                "tei_repo": {
                    "value": "",
                    "type": "corpus_repo",
                    "label": "MELP TEI Repository",
                    "note": "Likely named me_tei"
                },
                "delete_existing": {
                    "value": "Yes",
                    "type": "choice",
                    "choices": ["Yes", "No"],
                    "label": "Delete existing content?",
                    "note": "Selecting 'Yes' will result in a full refresh of corpus data."
                }
            },
        },
        "module": 'plugins.melp.tasks',
        "functions": ['import_data']
    },
}


def import_data(job_id):
    time_start = timer()

    job = Job(job_id)
    corpus = job.corpus
    tei_repo_name = job.get_param_value('tei_repo')
    tei_repo = corpus.repos[tei_repo_name]
    delete_existing = job.get_param_value('delete_existing') == 'Yes'

    job.set_status('running')
    job.report('''Attempting MELP TEI ingestion using the following parameters:
TEI Repo:          {0}
Delete Existing:   {1}
    \n'''.format(
        tei_repo.name,
        delete_existing
    ))

    try:
        es_logger = logging.getLogger('elasticsearch')
        es_log_level = es_logger.getEffectiveLevel()
        es_logger.setLevel(logging.WARNING)

        # pull down latest commits to play repo
        job.report("Pulling down latest commits to TEI repo...")
        tei_repo.pull(corpus)

        # ensure content types exist
        for melp_content_type in MELP_CONTENT_TYPE_SCHEMA:
            if melp_content_type['name'] not in corpus.content_types:
                corpus.save_content_type(melp_content_type)

        # for keeping track of letters that should be featured even
        # after deleting and re-ingesting
        featured_letters = []

        # delete existing content
        if delete_existing:
            job.report("Deleting existing letters and entities...")
            letters = corpus.get_content('Letter', all=True)
            for letter in letters:
                if letter.featured:
                    featured_letters.append(letter.identifier)

                letter.delete()

            entities = corpus.get_content('Entity', all=True)
            for ent in entities:
                ent.delete()

        # ingest people from personography
        person_count = 0
        personography_path = tei_repo.path + '/People_Places_Works/Personography.xml'
        if os.path.exists(personography_path):
            tei = None
            with open(personography_path, 'r', encoding='utf-8') as tei_in:
                tei = BeautifulSoup(tei_in, 'xml')

            people = tei.find('text').body.listPerson.find_all('person')
            for person in people:
                xml_id = person['xml:id']
                entity = corpus.get_content('Entity', {'xml_id': xml_id}, single_result=True)
                if entity:
                    entity.uris = []
                else:
                    entity = corpus.get_content('Entity')
                    entity.xml_id = xml_id

                entity.entity_type = 'PERSON'
                entity.name = person.persName.get_text().strip()

                uris = person.find_all('idno')
                for uri in uris:
                    entity.uris.append(uri.get_text().strip())

                entity.save()
                person_count += 1
        job.report("{0} persons registered.".format(person_count))

        # ingest places from placeography
        place_count = 0
        placeography_path = tei_repo.path + '/People_Places_Works/Placeography.xml'
        if os.path.exists(placeography_path):
            tei = None
            with open(placeography_path, 'r', encoding='utf-8') as tei_in:
                tei = BeautifulSoup(tei_in, 'xml')

            places = tei.find('text').body.listPlace.find_all('place')
            for place in places:
                xml_id = place['xml:id']
                entity = corpus.get_content('Entity', {'xml_id': xml_id}, single_result=True)
                if entity:
                    entity.uris = []
                else:
                    entity = corpus.get_content('Entity')
                    entity.xml_id = xml_id

                entity.entity_type = 'PLACE'
                ent_name = place.placeName.get_text().strip()
                if place.country:
                    ent_country = place.country.get_text().strip()
                    if ent_country:
                        ent_name = ent_name + ', ' + ent_country

                entity.name = ent_name

                uris = place.find_all('idno')
                for uri in uris:
                    entity.uris.append(uri.get_text().strip())

                entity.save()
                place_count += 1
        job.report("{0} places registered.".format(place_count))

        # ingest works from workography
        work_count = 0
        workography_path = tei_repo.path + '/People_Places_Works/Workography.xml'
        if os.path.exists(workography_path):
            tei = None
            with open(workography_path, 'r', encoding='utf-8') as tei_in:
                tei = BeautifulSoup(tei_in, 'xml')

            works = tei.find('text').body.listBibl.find_all('bibl')
            for work in works:
                xml_id = work['xml:id']
                entity = corpus.get_content('Entity', {'xml_id': xml_id}, single_result=True)
                if entity:
                    entity.uris = []
                else:
                    entity = corpus.get_content('Entity')
                    entity.xml_id = xml_id

                entity.entity_type = 'WORK'
                ent_name = ""
                first_title = work.find('title')
                if first_title:
                    ent_name = first_title.get_text().strip()

                first_author = work.find('author')
                if first_author and hasattr(first_author, 'persName'):
                    first_author = first_author.persName.get_text().strip()
                    if first_author and ',' in first_author:
                        ent_name += " ({0})".format(first_author.split(',')[0].strip())

                entity.name = ent_name

                if hasattr(work, 'idno') and work.idno:
                    entity.uris.append(work.idno.get_text().strip())

                entity.save()
                work_count += 1

        job.report("{0} works registered.".format(work_count))

        # ingest letters
        job.set_status('running', percent_complete=10)
        letter_path = tei_repo.path + '/Encoded Letters'
        letter_files = [letter_path + '/' + filename for filename in os.listdir(letter_path)]

        for letter_index in range(0, len(letter_files)):
            letter_file = letter_files[letter_index]
            letter_identifier = os.path.basename(letter_file)
            letter = corpus.get_content('Letter', {'identifier': letter_identifier}, single_result=True)
            if letter:
                letter.images = []
                letter.entities_mentioned = []
            else:
                letter = corpus.get_content('Letter')
                letter.identifier = letter_identifier

            job.report("\n\n##### Parsing TEI for {0}:".format(os.path.basename(letter_file)))
            tei = None
            with open(letter_file, 'r', encoding='utf-8') as tei_in:
                tei = BeautifulSoup(tei_in, 'xml')

            if tei:
                file_desc = tei.teiHeader.fileDesc

                # --------------------------------- #
                # title                             #
                # --------------------------------- #
                title_tag = file_desc.titleStmt.find('title')
                if title_tag:
                    letter.title = title_tag.get_text()

                if not letter.title:
                    job.report("Unable to determine title of letter (tei -> fileDesc -> titleStmt -> title).")

                # --------------------------------- #
                # repository                        #
                # --------------------------------- #
                org_tag = file_desc.editionStmt.respStmt.find('orgName')
                repo_added = False
                if org_tag:
                    org_name = org_tag.get_text().strip()
                    if org_name:
                        if 'ref' in org_tag.attrs:
                            org_uri = org_tag['ref']

                        org = corpus.get_or_create_content('Entity', {'name': org_name, 'entity_type': 'ORG'})
                        if org_uri not in org.uris:
                            org.uris.append(org_uri)
                            org.save()

                        letter.repository = org.id
                        repo_added = True

                if not repo_added:
                    job.report("Unable to determine the repository for this letter (tei -> fileDesc -> editionStmt -> respStmt -> orgName).")

                # --------------------------------- #
                # author and recipient              #
                # --------------------------------- #
                interlocutors = file_desc.sourceDesc.find_all("persName")
                sender_id = None
                recip_id = None
                if len(interlocutors) == 2:
                    sender_uri = interlocutors[0].attrs.get('ref')
                    if sender_uri:
                        sender, log = register_entity(corpus, 'PERSON', sender_uri)
                        if sender:
                            sender_id = sender.id
                            if log == "found":
                                letter.author = corpus.get_content_dbref('Entity', sender_id)

                    recip_uri = interlocutors[1].attrs.get('ref')
                    if recip_uri:
                        recip, log = register_entity(corpus, 'PERSON', recip_uri)
                        if recip:
                            recip_id = recip.id
                            if log == "found":
                                letter.recipient = corpus.get_content_dbref('Entity', recip_id)

                if not letter.author:
                    job.report("Unable to determine author (tei -> fileDesc -> sourceDesc -> persName[1st]).")

                if not letter.recipient:
                    job.report("Unable to determine recipient (tei -> fileDesc -> sourceDesc -> persName[2nd]).")

                # --------------------------------- #
                # date of composition               #
                # --------------------------------- #
                date_tag = file_desc.sourceDesc.find("date")
                if date_tag and hasattr(date_tag, 'attrs') and 'when' in date_tag.attrs:
                    when = date_tag['when']
                    if 'xx' in when:
                        when = when.replace('xx', '01')
                        job.report(f"Date of composition regularized from {date_tag['when']} to {when}!")
                    letter.date_composed = parser.parse(when)

                if not letter.date_composed:
                    job.report("Unable to determine date of composition (tei -> fileDesc -> sourceDesc -> date).")

                # --------------------------------- #
                # letter body                       #
                # --------------------------------- #
                letter_body = tei.find('text').body

                # images
                images = letter_body.find_all('pb')
                for image in images:
                    if 'facs' in image.attrs:
                        letter.images.append(image['facs'])

                # parse letter body
                entities = []
                info = []
                letter.html = parse_letter_tei(corpus, letter_body, entities, info)

                # add log entries to report
                if info:
                    job.report("\n".join(info))

                # associate entities
                entities = list(set(entities))
                for ent_id in entities:
                    if not ent_id in [sender_id, recip_id]:
                        letter.entities_mentioned.append(corpus.get_content_dbref('Entity', ent_id))

                # check if letter is featured
                if letter.identifier in featured_letters:
                    letter.featured = True

                job.report("{0} entities now referenced by letter.".format(len(letter.entities_mentioned)))
                letter.save()

                job.set_status('running', percent_complete=int(((letter_index + 1) / len(letter_files)) * 100))


        # ENTITY CLEANUP
        job.report("\nCleaning up unreferenced entities...")
        entity_types = ['PERSON', 'PLACE', 'WORK']
        for entity_type in entity_types:
            entities = corpus.get_content('Entity', {'entity_type': entity_type})
            entities = [e for e in entities]
            for entity in entities:
                mentions = 0

                if entity_type == 'PERSON':
                    mentions += corpus.get_content('Letter', {'author': entity.id}).count()
                    mentions += corpus.get_content('Letter', {'recipient': entity.id}).count()

                mentions += corpus.get_content('Letter', {'entities_mentioned__contains': entity.id}).count()

                if mentions == 0:
                    entity.delete()

        time_stop = timer()
        job.report("\n\nMELP TEI ingestion completed in {0} seconds.".format(int(time_stop - time_start)))
        job.complete(status='complete')
        es_logger.setLevel(es_log_level)
    except:
        job.report("\n\nA major error prevented the ingestion of MELP TEI:\n{0}".format(
            traceback.format_exc()
        ))
        job.complete(status='error')


def register_entity(corpus, entity_type, uri):

    # REFERENCE TO CATALOGED PERSON OR PLACE
    if (entity_type == "PERSON" and 'Personography.xml' in uri) or \
            (entity_type == "PLACE" and 'Placeography.xml' in uri) or \
            (entity_type == "WORK" and 'Workography.xml' in uri):

        relevant_catalog = "Personography.xml"
        if 'Placeography.xml' in uri:
            relevant_catalog = "Placeography.xml"
        elif 'Workography.xml' in uri:
            relevant_catalog = "Workography"

        uri_parts = uri.split('#')
        if len(uri_parts) == 2:
            xml_id = uri_parts[1]
            entity = corpus.get_content('Entity', {'entity_type': entity_type, 'xml_id': xml_id}, single_result=True)
            if entity:
                return entity, "found"
            else:
                return None, "Error referencing {0} with URI {1}: XML ID {2} not found in {3}".format(
                    entity_type,
                    uri,
                    xml_id,
                    relevant_catalog
                )
        else:
            return None, "Error referencing {0} with URI {1}: {2} URI malformed".format(entity_type, uri, relevant_catalog)

    return None, "Error referencing {0} with URI {1}: Source for URI not recognized".format(entity_type, uri)


def log_tag(tag):
    log = ""
    if tag.name:
        log = "[{0}]".format(tag.name)
        if tag.attrs:
            log += " {"
            for attr in tag.attrs.keys():
                log += " {0}={1}".format(attr, tag.attrs[attr])
            log += " }"
    return log


def parse_letter_tei(corpus, tag, entities=[], info=[]):
    html = ""

    simple_conversions = {
        'hi': 'span',
        'opener': 'div:opener',
        'dateline': 'div:dateline',
        'date': 'span:date',
        'salute': 'span:salutation',
        'p': 'p',
        'lb': 'br/',
        'unclear': 'span:unclear',
        'del': 'span:deletion',
        'add': 'span:addition',
        'closer': 'div:closer',
        'postscript': 'div:postscript',
        'note': 'span:note',
        'address': 'span:address',
        'addrLine': 'br/',
        'quote': 'quote',
        'roleName': 'span:role',
        'abbr': 'span:abbreviation',
    }

    silent = [
        'body', 'div', 'orig', 'reg', 'name', 'forename', 'surname'
    ]

    if tag.name:
        if tag.name in silent:
            for child in tag.children:
                html += parse_letter_tei(corpus, child, entities, info)

        else:
            attributes = ""
            classes = []

            if 'rend' in tag.attrs:
                classes += ["rend-{0}".format(slugify(r)) for r in tag['rend'].split() if r]

            if tag.name == 'pb' and _contains(tag.attrs, ['n', 'facs']):
                html += '''<a name="page-break-{page}" class="page-break" data-page="{page}" data-image="{image}"><i class="fas fa-image"></i></a>'''.format(
                    page=tag['n'],
                    image=tag['facs']
                )

            elif tag.name == 'choice':
                original = tag.find('orig')
                if original:
                    original = original.get_text().strip().replace('"', '\"')
                else:
                    original = ""

                regularized = tag.find('reg')
                if regularized:
                    html += '''<span class="regularized" data-original="{0}">'''.format(original)
                    html += "".join([parse_letter_tei(corpus, child, entities, info) for child in regularized.children])
                    html += "</span>"

            elif tag.name in ['persName', 'placeName', 'title'] and 'ref' in tag.attrs:
                entity_type = 'PERSON'
                if tag.name == 'placeName':
                    entity_type = 'PLACE'
                elif tag.name == 'title':
                    entity_type = 'WORK'

                entity, log = register_entity(corpus, entity_type, tag['ref'])
                if entity:
                    html += '''<span class="entity" data-entity_type="{entity_type}" data-entity_uri="{uri}" data-entity_id="{id}">'''.format(
                        entity_type=entity_type,
                        uri=tag['ref'],
                        id=entity.xml_id
                    )

                html += "".join([parse_letter_tei(corpus, child, entities, info) for child in tag])

                if entity:
                    html += "</span>"
                    entities.append(entity.id)
                else:
                    info.append(log)

            elif tag.name in simple_conversions:
                html_tag = simple_conversions[tag.name]
                self_closing = html_tag.endswith('/')
                if self_closing:
                    html_tag = html_tag[:-1]

                if ':' in html_tag:
                    html_tag = html_tag.split(':')[0]
                    classes.append(simple_conversions[tag.name].split(':')[1])

                if classes:
                    attributes += ' class="{0}"'.format(" ".join(classes))
                    if self_closing:
                        attributes += ' /'

                html += "<{0}{1}>".format(
                    html_tag,
                    attributes
                )
                html += "".join([parse_letter_tei(corpus, child, entities, info) for child in tag])
                if not self_closing:
                    html += "</{0}>".format(html_tag)

            # tags to ignore (but keep content inside)
            elif tag.name in silent:
                html += "".join([parse_letter_tei(corpus, child, entities, info) for child in tag])

            else:
                info.append("Unhandled tag: {0}".format(log_tag(tag)))
                html += "".join([parse_letter_tei(corpus, child, entities, info) for child in tag])

    else:
        html += tag.get_text()

    return html
