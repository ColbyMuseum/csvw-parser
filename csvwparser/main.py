from StringIO import StringIO
import urllib2
import logging
import parser
from csvwparser import metadata
import metadata_extractor


__author__ = 'sebastian'

logging.basicConfig()
logger = logging.getLogger(__name__)


class CSVW:
    def __init__(self, url=None, path=None, metadata_url=None, metadata_path=None, date_parsing=False):
        if url:
            response = urllib2.urlopen(url)
            handle = StringIO(response.read())
            name = url
        elif path:
            handle = open(path, 'rb')
            name = path
        elif path and url:
            raise ValueError("only one argument of url and path allowed")
        else:
            raise ValueError("url or path argument required")

        metadata_handle = None
        if metadata_path and metadata_url:
            raise ValueError("only one argument of metadata_url and metadata_path allowed")
        elif metadata_url:
            response = urllib2.urlopen(metadata_url)
            metadata_handle = StringIO(response.read())
        elif metadata_path:
            metadata_handle = open(metadata_path, 'rb')

        self.table, embedded_metadata = parser.parse(handle, url)

        # TODO create settings using arguments or provided metadata
        sources = metadata_extractor.metadata_extraction(url, metadata_handle, embedded_metadata=embedded_metadata)
        self.metadata = metadata.merge(sources)

    def to_rdf(self):
        pass

    def to_json(self):
        pass
